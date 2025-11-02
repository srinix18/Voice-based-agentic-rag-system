import os
import sys
from pathlib import Path
import pytest

# Ensure project package path is on sys.path so tests can import local modules
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import torch
except Exception:
    torch = None

from tools.financial_rag_search import FinancialRAGRetriever


@pytest.mark.skipif(torch is None or not getattr(torch, 'cuda', None) or not torch.cuda.is_available(),
                    reason="CUDA not available on this system")
def test_rag_uses_cuda(tmp_path, monkeypatch):
    """Ensure the FinancialRAGRetriever activates CUDA when requested via RAG_DEVICE env var."""
    # Force the retriever to pick CUDA via env var
    monkeypatch.setenv('RAG_DEVICE', 'cuda')

    # Use a temporary (non-existing) pdf directory to avoid heavy index builds during the test
    pdf_dir = tmp_path / "no_pdfs_here"
    index_cache = tmp_path / "faiss_test.pkl"

    retriever = FinancialRAGRetriever(str(pdf_dir), index_cache_path=str(index_cache))

    # The retriever should report device starting with 'cuda'
    assert retriever.device is not None
    assert str(retriever.device).startswith('cuda')

    # If the SentenceTransformer exposes a device attribute, ensure it refers to cuda as well
    model_device = getattr(retriever.embedding_model, 'device', None)
    if model_device is not None:
        assert 'cuda' in str(model_device)
