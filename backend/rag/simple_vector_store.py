"""
Simplified vector store that works without ChromaDB compilation issues.
Uses sentence-transformers when available; otherwise falls back to a lightweight
hash-based embedding to avoid heavy scipy/sklearn runtime requirements.
"""
from typing import List, Dict, Any
import numpy as np
from backend.config import settings
import json
from pathlib import Path

class SimpleVectorStore:
    """Simple in-memory vector store (fallback when ChromaDB fails to install)"""
    
    def __init__(self):
        """Initialize simple vector store"""
        self.papers = []
        self.embeddings = []
        self.embedding_model = None
        self.using_lightweight_embeddings = False
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        except Exception as e:
            self.using_lightweight_embeddings = True
            print(f"⚠️  sentence-transformers unavailable, using lightweight embeddings: {e}")
        self.storage_file = Path(settings.DATA_DIR) / "simple_vector_store.json"
        self._load()
        print(f"✅ Simple vector store initialized (in-memory fallback)")

    def _encode_text(self, text: str):
        """Encode text using model if available, else a lightweight hash embedding."""
        if self.embedding_model is not None:
            return self.embedding_model.encode(text)

        # Lightweight deterministic embedding fallback (no external heavy deps).
        dim = 256
        vec = np.zeros(dim, dtype=np.float32)
        tokens = [t for t in text.lower().split() if t]
        for token in tokens:
            vec[hash(token) % dim] += 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec
    
    def add_papers(self, papers: List[Dict[str, Any]]) -> int:
        """Add papers to vector store"""
        if not papers:
            return 0
        
        for paper in papers:
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
            embedding = self._encode_text(text)
            
            paper_data = {
                'id': paper.get('id', f"paper_{len(self.papers)}"),
                'title': paper.get('title', ''),
                'authors': paper.get('authors', []),
                'year': paper.get('year', ''),
                'abstract': text[:500],
                'source': paper.get('source', ''),
                'niches': paper.get('niches', []),
                'doi': paper.get('doi', ''),
                'url': paper.get('url', '')
            }
            
            self.papers.append(paper_data)
            self.embeddings.append(embedding)
        
        self._save()
        return len(papers)
    
    def search_similar(self, query: str, top_k: int = 10, filters: Dict = None) -> List[Dict]:
        """Search for similar papers"""
        if not self.papers:
            return []
        
        # Generate query embedding
        query_embedding = self._encode_text(query)
        
        # Calculate cosine similarities
        similarities = []
        for i, emb in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append((i, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k results
        results = []
        for idx, sim in similarities[:top_k]:
            paper = self.papers[idx].copy()
            paper['similarity_score'] = float(sim)
            results.append(paper)
        
        return results
    
    def count(self) -> int:
        """Get total number of papers"""
        return len(self.papers)
    
    def _save(self):
        """Save to disk"""
        try:
            data = {
                'papers': self.papers,
                'embeddings': [emb.tolist() for emb in self.embeddings]
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Warning: Could not save vector store: {e}")
    
    def _load(self):
        """Load from disk"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                self.papers = data.get('papers', [])
                self.embeddings = [np.array(emb) for emb in data.get('embeddings', [])]
                print(f"   Loaded {len(self.papers)} papers from storage")
        except Exception as e:
            print(f"   Starting with empty store")

# Try ChromaDB first, fallback to simple store
_vector_store = None

def get_vector_store():
    """Get vector store (ChromaDB or simple fallback)"""
    global _vector_store
    if _vector_store is None:
        try:
            # Try importing ChromaDB
            import chromadb
            from backend.rag.vector_store import VectorStore
            _vector_store = VectorStore()
            print("   Using ChromaDB (recommended)")
        except ImportError:
            # Fallback to simple store
            _vector_store = SimpleVectorStore()
            print("   Using simple vector store (ChromaDB not available)")
    return _vector_store
