"""
Bulk paper ingestion script for initial RAG database population
Target: 2000+ papers from multiple sources
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.rag.vector_store import get_vector_store
from backend.database.database import SessionLocal
from backend.database.models import ExternalPaper, IngestionLog
from backend.config import settings
import requests
from datetime import datetime
import time

class BulkIngester:
    """Bulk ingestion from multiple free APIs"""
    
    def __init__(self):
        self.vector_store = get_vector_store()
        self.db = SessionLocal()
        self.papers_collected = []
        
    def fetch_from_arxiv(self, query: str, max_results: int = 100):
        """Fetch papers from arXiv"""
        print(f"\n📚 Fetching from arXiv: {query}")
        
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": query,
                "start": 0,
                "max_results": max_results,
                "sortBy": "relevance"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                # Parse XML response (simplified)
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                count = 0
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    try:
                        title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                        summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                        published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                        id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                        
                        if title_elem is not None and summary_elem is not None:
                            paper = {
                                "id": f"arxiv_{id_elem.text.split('/')[-1] if id_elem is not None else count}",
                                "title": title_elem.text.strip(),
                                "abstract": summary_elem.text.strip(),
                                "authors": [a.find('{http://www.w3.org/2005/Atom}name').text 
                                           for a in entry.findall('{http://www.w3.org/2005/Atom}author')],
                                "year": published_elem.text[:4] if published_elem is not None else "2024",
                                "source": "arxiv",
                                "niches": [query],
                                "doi": "",
                                "url": id_elem.text if id_elem is not None else ""
                            }
                            self.papers_collected.append(paper)
                            count += 1
                    except Exception as e:
                        continue
                
                print(f"   ✅ Collected {count} papers from arXiv")
                return count
        except Exception as e:
            print(f"   ❌ arXiv error: {e}")
            return 0
    
    def run_bulk_ingestion(self, total_target: int = 2000):
        """Run bulk ingestion to reach target"""
        print("="*60)
        print("🚀 BULK RESEARCH PAPER INGESTION")
        print("="*60)
        print(f"\nTarget: {total_target} papers")
        print(f"Sources: arXiv (free API)\n")
        
        # Define research domains to diversify
        domains = [
            "machine learning",
            "deep learning",
            "natural language processing",
            "computer vision",
            "reinforcement learning",
            "neural networks",
            "artificial intelligence",
            "data science",
            "robotics",
            "quantum computing"
        ]
        
        papers_per_domain = total_target // len(domains)
        
        start_time = time.time()
        
        for domain in domains:
            if len(self.papers_collected) >= total_target:
                break
            
            remaining = total_target - len(self.papers_collected)
            fetch_count = min(papers_per_domain, remaining, 100)  # arXiv limit
            
            self.fetch_from_arxiv(domain, fetch_count)
            time.sleep(3)  # Rate limiting
        
        # Add to vector store
        print(f"\n📦 Adding {len(self.papers_collected)} papers to vector store...")
        
        try:
            added = self.vector_store.add_papers(self.papers_collected)
            print(f"   ✅ Successfully added {added} papers")
            
            # Log to database
            log = IngestionLog(
                papers_added=added,
                sources=["arxiv"],
                status="success",
                meta_data={"domains": domains, "target": total_target}
            )
            self.db.add(log)
            self.db.commit()
            
        except Exception as e:
            print(f"   ❌ Error adding papers: {e}")
            log = IngestionLog(
                papers_added=0,
                sources=["arxiv"],
                status="error",
                error_message=str(e)
            )
            self.db.add(log)
            self.db.commit()
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("📊 INGESTION COMPLETE")
        print("="*60)
        print(f"Papers collected: {len(self.papers_collected)}")
        print(f"Papers added: {added if 'added' in locals() else 0}")
        print(f"Time elapsed: {elapsed:.1f}s")
        print(f"Rate: {len(self.papers_collected)/elapsed:.1f} papers/sec")
        print(f"\nTotal in database: {self.vector_store.count()}")
        print("="*60)
        
        self.db.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bulk ingest research papers")
    parser.add_argument("--total-target", type=int, default=2000,
                       help="Total number of papers to collect")
    args = parser.parse_args()
    
    ingester = BulkIngester()
    ingester.run_bulk_ingestion(args.total_target)

if __name__ == "__main__":
    main()
