"""
Vector Store for RAG System
Now redirecting to the BM25 Vectorless Store
"""
import sys
from pathlib import Path

# Add project root to path if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.rag.vectorless_store import get_vector_store

# Re-export
__all__ = ["get_vector_store"]
