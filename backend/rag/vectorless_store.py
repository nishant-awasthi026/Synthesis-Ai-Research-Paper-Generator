"""
Vectorless RAG implementation using BM25
"""
import json
import re
from typing import List, Dict, Any
from pathlib import Path
from backend.config import settings

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    print("[WARN] rank_bm25 not available.")

class VectorlessStore:
    def __init__(self):
        """Initialize BM25 vectorless store"""
        self.papers = []
        self.bm25 = None
        self.storage_file = Path(settings.DATA_DIR) / "vectorless_store.json"
        
        if not BM25_AVAILABLE:
            print("⚠️ rank_bm25 not installed, please install it: pip install rank_bm25")
            
        self._load()
        print(f"✅ Vectorless store initialized: {settings.COLLECTION_NAME}")

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization for BM25"""
        if not text:
            return []
        text = text.lower()
        # Remove punctuation and extract alphanumeric words
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
    
    def _build_index(self):
        if not BM25_AVAILABLE or not self.papers:
            self.bm25 = None
            return
            
        tokenized_corpus = []
        for paper in self.papers:
            text = f"{paper.get('title', '')} {paper.get('abstract', '')} {paper.get('authors', '')}"
            tokenized_corpus.append(self._tokenize(text))
            
        self.bm25 = BM25Okapi(tokenized_corpus)
        
    def add_papers(self, papers: List[Dict[str, Any]]) -> int:
        """
        Add papers to vectorless store
        """
        if not papers:
            return 0
            
        for i, paper in enumerate(papers):
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
            
            paper_data = {
                'id': paper.get('id', f"paper_{len(self.papers)}_{hash(text) % 100000}"),
                'title': paper.get('title', ''),
                'authors': str(paper.get('authors', [])),
                'year': paper.get('year', ''),
                'abstract': paper.get('abstract', ''),
                'source': paper.get('source', ''),
                'niches': str(paper.get('niches', [])),
                'doi': paper.get('doi', ''),
                'url': paper.get('url', '')
            }
            # Avoid duplicate insertion by ID
            if not any(p['id'] == paper_data['id'] for p in self.papers):
                self.papers.append(paper_data)
        
        self._build_index()
        self._save()
        return len(papers)
    
    def search_similar(self, query: str, top_k: int = 10, filters: Dict = None) -> List[Dict]:
        """
        Search for similar papers using BM25
        """
        if not self.bm25 or not self.papers:
            return []
            
        tokenized_query = self._tokenize(query)
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # Sort scores descending
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
        
        results = []
        max_score = max(doc_scores) if doc_scores.any() else 1.0
        if max_score == 0:
            max_score = 1.0
            
        for idx in top_indices:
            score = doc_scores[idx]
            if score <= 0:
                continue # Skip zero-match documents
                
            paper = self.papers[idx].copy()
            # Normalize score loosely to 0-1 for compatibility
            paper['similarity_score'] = float(score / max_score)
            results.append(paper)
            
        return results
    
    def count(self) -> int:
        """Get total number of papers in vectorless store"""
        return len(self.papers)
    
    def count_by_niche(self) -> Dict[str, int]:
        return {"total": self.count()}
    
    def delete_collection(self):
        self.papers = []
        self.bm25 = None
        if self.storage_file.exists():
            self.storage_file.unlink()
        print(f"[WARN] Deleted collection: {settings.COLLECTION_NAME}")

    def _save(self):
        """Save to disk"""
        try:
            data = {'papers': self.papers}
            with open(self.storage_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Warning: Could not save vectorless store: {e}")
    
    def _load(self):
        """Load from disk"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                self.papers = data.get('papers', [])
                self._build_index()
                print(f"   Loaded {len(self.papers)} papers into Vectorless Store")
        except Exception as e:
            print(f"   Starting with empty Vectorless Store")

_vector_store = None

def get_vector_store():
    """Get vector store singleton"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorlessStore()
    return _vector_store
