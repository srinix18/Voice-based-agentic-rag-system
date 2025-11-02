"""
Financial RAG Search Tool for NCFE e-Library
Loads PDFs, extracts text, creates embeddings, and performs semantic search.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import pickle

import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
try:
    import torch
except Exception:
    torch = None

logger = logging.getLogger(__name__)


class FinancialRAGRetriever:
    """
    RAG retriever for NCFE e-Library financial content.
    Loads PDFs, chunks text, creates FAISS index for semantic search.
    """
    
    def __init__(self, pdf_directory: str, index_cache_path: str = None, device: str = None):
        """
        Initialize the RAG retriever.
        
        Args:
            pdf_directory: Path to directory containing PDF files
            index_cache_path: Optional path to cache the FAISS index
        """
        self.pdf_directory = Path(pdf_directory)
        self.index_cache_path = index_cache_path or str(self.pdf_directory.parent / "faiss_index.pkl")
        # Determine device: explicit param > RAG_DEVICE env var > torch.cuda availability > cpu
        env_device = os.getenv('RAG_DEVICE') if os.getenv('RAG_DEVICE') else None
        if device:
            self.device = device
        elif env_device:
            self.device = env_device
        else:
            try:
                self.device = 'cuda' if (torch is not None and torch.cuda.is_available()) else 'cpu'
            except Exception:
                self.device = 'cpu'

        logger.info(f"Using embedding device: {self.device}")

        # Initialize the SentenceTransformer on the chosen device
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
        self.chunks = []
        self.metadata = []
        self.index = None
        
        # Load or create index
        if os.path.exists(self.index_cache_path):
            logger.info(f"Loading cached index from {self.index_cache_path}")
            self._load_index()
        else:
            logger.info("Creating new index from PDFs")
            self._build_index()
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num} from {pdf_path.name}: {e}")
                        continue
                return text
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Number of words per chunk
            overlap: Number of words to overlap between chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 50:  # Only keep substantial chunks
                chunks.append(chunk)
        
        return chunks
    
    def _build_index(self):
        """Build FAISS index from all PDFs in the directory."""
        logger.info(f"Loading PDFs from {self.pdf_directory}")
        
        # Check if directory exists and has PDFs
        if not self.pdf_directory.exists():
            logger.error(f"PDF directory does not exist: {self.pdf_directory}")
            # Create empty index
            self.index = faiss.IndexFlatL2(384)  # Dimension for all-MiniLM-L6-v2
            return
        
        pdf_files = list(self.pdf_directory.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.pdf_directory}")
            # Create empty index
            self.index = faiss.IndexFlatL2(384)
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        # Extract text from all PDFs
        all_chunks = []
        all_metadata = []
        
        for pdf_path in pdf_files:
            logger.info(f"Processing {pdf_path.name}")
            text = self._extract_text_from_pdf(pdf_path)
            
            if not text.strip():
                logger.warning(f"No text extracted from {pdf_path.name}")
                continue
            
            chunks = self._chunk_text(text)
            logger.info(f"Created {len(chunks)} chunks from {pdf_path.name}")
            
            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadata.append({
                    "source": pdf_path.name,
                    "path": str(pdf_path)
                })
        
        if not all_chunks:
            logger.error("No text chunks created from PDFs")
            self.index = faiss.IndexFlatL2(384)
            return
        
        logger.info(f"Total chunks: {len(all_chunks)}")
        self.chunks = all_chunks
        self.metadata = all_metadata
        
        # Create embeddings
        logger.info("Creating embeddings...")
        embeddings = self.embedding_model.encode(all_chunks, show_progress_bar=True)

        # Create FAISS index on CPU first
        dimension = embeddings.shape[1]
        cpu_index = faiss.IndexFlatL2(dimension)
        cpu_index.add(np.array(embeddings).astype('float32'))

        # If device is GPU and FAISS GPU bindings exist, move index to GPU
        if str(self.device).startswith('cuda'):
            try:
                if hasattr(faiss, 'StandardGpuResources') and hasattr(faiss, 'index_cpu_to_gpu'):
                    logger.info('FAISS GPU bindings detected - attempting to move index to GPU')
                    # Create GPU resources and move index (GPU id 0)
                    gpu_res = faiss.StandardGpuResources()
                    gpu_index = faiss.index_cpu_to_gpu(gpu_res, 0, cpu_index)
                    self.index = gpu_index
                    logger.info('Moved FAISS index to GPU')
                else:
                    logger.info('FAISS GPU bindings not available, using CPU index (embeddings computed on GPU)')
                    self.index = cpu_index
            except Exception as e:
                logger.warning(f'Could not move FAISS index to GPU: {e}. Falling back to CPU index.')
                self.index = cpu_index
        else:
            self.index = cpu_index
        
        logger.info(f"FAISS index created with {self.index.ntotal} vectors")
        
        # Cache the index
        self._save_index()
    
    def _save_index(self):
        """Save the FAISS index and metadata to disk."""
        try:
            cache_data = {
                'index': faiss.serialize_index(self.index),
                'chunks': self.chunks,
                'metadata': self.metadata
            }
            with open(self.index_cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
            logger.info(f"Index cached to {self.index_cache_path}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def _load_index(self):
        """Load the FAISS index and metadata from disk."""
        try:
            with open(self.index_cache_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            cpu_index = faiss.deserialize_index(cache_data['index'])
            # If running with GPU device, attempt to move the loaded CPU index to GPU
            if str(self.device).startswith('cuda'):
                try:
                    if hasattr(faiss, 'StandardGpuResources') and hasattr(faiss, 'index_cpu_to_gpu'):
                        logger.info('Moving loaded FAISS index to GPU')
                        gpu_res = faiss.StandardGpuResources()
                        gpu_index = faiss.index_cpu_to_gpu(gpu_res, 0, cpu_index)
                        self.index = gpu_index
                    else:
                        logger.info('FAISS GPU bindings not available; using CPU index from cache')
                        self.index = cpu_index
                except Exception as e:
                    logger.warning(f'Could not move cached FAISS index to GPU: {e}. Using CPU index.')
                    self.index = cpu_index
            else:
                self.index = cpu_index
            self.chunks = cache_data['chunks']
            self.metadata = cache_data['metadata']
            
            logger.info(f"Loaded index with {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            logger.info("Building new index...")
            self._build_index()
    
    def search(self, query: str, top_k: int = 3, score_threshold: float = 1.5) -> List[Dict[str, Any]]:
        """
        Search for relevant passages given a query.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            score_threshold: Maximum distance threshold (lower is better)
        
        Returns:
            List of dictionaries with 'text', 'source', and 'score' keys
        """
        if self.index is None or self.index.ntotal == 0:
            logger.warning("Index is empty. No results to return.")
            return []
        
        # Create query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            min(top_k, self.index.ntotal)
        )
        
        # Format results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunks) and dist <= score_threshold:
                results.append({
                    'text': self.chunks[idx],
                    'source': self.metadata[idx]['source'],
                    'score': float(dist),
                    'relevance': 'high' if dist < 0.8 else 'medium' if dist < 1.2 else 'low'
                })
        
        logger.info(f"Found {len(results)} results for query: {query}")
        return results
    
    def rebuild_index(self):
        """Force rebuild of the index from PDFs."""
        logger.info("Forcing index rebuild...")
        if os.path.exists(self.index_cache_path):
            os.remove(self.index_cache_path)
        self._build_index()


# Tool function for ADK
def search_financial_knowledge_base(query: str) -> str:
    """
    Search the NCFE e-Library financial knowledge base for information.
    
    Args:
        query: The question or topic to search for
    
    Returns:
        Relevant passages from the financial knowledge base, or a message
        indicating no information was found.
    """
    # Get the PDF directory path
    current_dir = Path(__file__).parent.parent
    pdf_dir = current_dir / "data" / "ncfe_books"
    
    # Initialize retriever (will use cached index if available)
    retriever = FinancialRAGRetriever(str(pdf_dir))
    
    # Search for relevant passages
    results = retriever.search(query, top_k=3)
    
    if not results:
        return "I don't have that information in my knowledge base."
    
    # Format response
    response_parts = []
    response_parts.append("Based on the NCFE e-Library content:\n")
    
    for i, result in enumerate(results, 1):
        response_parts.append(f"\n[Source {i}: {result['source']}]")
        response_parts.append(f"{result['text']}\n")
    
    return "\n".join(response_parts)


if __name__ == "__main__":
    # Test the retriever
    logging.basicConfig(level=logging.INFO)
    
    # Test with example query
    print("Testing Financial RAG Retriever...")
    print("-" * 80)
    
    result = search_financial_knowledge_base("What is compound interest?")
    print(result)
    
    print("-" * 80)
    result = search_financial_knowledge_base("Explain the role of SEBI")
    print(result)
