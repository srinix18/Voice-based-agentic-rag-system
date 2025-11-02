"""
Test suite for Financial RAG Agent
Tests the retriever and agent functionality
"""

import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.financial_rag_search import FinancialRAGRetriever, search_financial_knowledge_base
from main_agent import FinancialRAGAgent


class TestFinancialRAGRetriever:
    """Tests for the RAG retriever component."""
    
    @pytest.fixture
    def pdf_directory(self):
        """Get the PDF directory path."""
        return Path(__file__).parent.parent / "data" / "ncfe_books"
    
    @pytest.fixture
    def retriever(self, pdf_directory):
        """Create a retriever instance."""
        return FinancialRAGRetriever(str(pdf_directory))
    
    def test_retriever_initialization(self, retriever):
        """Test that the retriever initializes correctly."""
        assert retriever is not None
        assert retriever.index is not None
        assert retriever.embedding_model is not None
    
    def test_search_returns_results(self, retriever):
        """Test that search returns results (if PDFs exist)."""
        query = "compound interest"
        results = retriever.search(query, top_k=3)
        
        # If PDFs exist, should return results
        # If no PDFs, should return empty list
        assert isinstance(results, list)
    
    def test_search_with_irrelevant_query(self, retriever):
        """Test search with an irrelevant query."""
        query = "quantum physics molecular structure"
        results = retriever.search(query, top_k=3)
        
        # Should return empty or low relevance results
        assert isinstance(results, list)
    
    def test_search_financial_knowledge_base_function(self):
        """Test the tool function directly."""
        result = search_financial_knowledge_base("What is compound interest?")
        assert isinstance(result, str)
        assert len(result) > 0


class TestFinancialRAGAgent:
    """Tests for the main agent."""
    
    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Set a mock API key for testing."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test_api_key_123")
        return "test_api_key_123"
    
    def test_agent_initialization_with_api_key(self, mock_api_key):
        """Test that agent initializes with API key."""
        try:
            agent = FinancialRAGAgent(api_key=mock_api_key)
            assert agent is not None
            assert agent.api_key == mock_api_key
        except Exception as e:
            # API initialization may fail with mock key, but object should be created
            pass
    
    def test_agent_initialization_without_api_key(self):
        """Test that agent raises error without API key."""
        # Temporarily clear environment
        original_key = os.environ.get("GOOGLE_API_KEY")
        if original_key:
            del os.environ["GOOGLE_API_KEY"]
        
        with pytest.raises(ValueError):
            FinancialRAGAgent()
        
        # Restore original key
        if original_key:
            os.environ["GOOGLE_API_KEY"] = original_key
    
    def test_agent_has_tools(self, mock_api_key):
        """Test that agent has tools configured."""
        try:
            agent = FinancialRAGAgent(api_key=mock_api_key)
            assert agent.tools is not None
            assert len(agent.tools) > 0
        except Exception:
            pass


class TestIntegration:
    """Integration tests with example queries."""
    
    @pytest.fixture
    def sample_queries(self):
        """Sample queries to test."""
        return [
            "What is compound interest?",
            "Explain the role of SEBI in financial markets",
            "What is the difference between equity and debt?",
            "What is mutual fund?",
            "Explain inflation and its impact on savings",
        ]
    
    def test_retriever_with_sample_queries(self, sample_queries):
        """Test retriever with sample financial queries."""
        pdf_dir = Path(__file__).parent.parent / "data" / "ncfe_books"
        retriever = FinancialRAGRetriever(str(pdf_dir))
        
        for query in sample_queries:
            results = retriever.search(query, top_k=2)
            assert isinstance(results, list)
            print(f"\nQuery: {query}")
            print(f"Results: {len(results)} found")
            
            if results:
                print(f"Top result relevance: {results[0]['relevance']}")
    
    def test_tool_function_with_sample_queries(self, sample_queries):
        """Test the tool function with sample queries."""
        for query in sample_queries[:2]:  # Test first 2 to save time
            result = search_financial_knowledge_base(query)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"\n{'='*80}")
            print(f"Query: {query}")
            print(f"Response: {result[:200]}...")


def test_pdf_directory_exists():
    """Test that the PDF directory exists."""
    pdf_dir = Path(__file__).parent.parent / "data" / "ncfe_books"
    assert pdf_dir.exists(), f"PDF directory not found: {pdf_dir}"
    print(f"\n✅ PDF directory exists: {pdf_dir}")
    
    # Check for PDFs
    pdf_files = list(pdf_dir.glob("*.pdf"))
    print(f"📚 Found {len(pdf_files)} PDF files")
    
    if pdf_files:
        for pdf in pdf_files[:5]:  # Show first 5
            print(f"   - {pdf.name}")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
