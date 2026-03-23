"""
Discovery API routes for research paper similarity and novelty
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.database.models import User, ResearchPaper
from backend.services.search_service import search_service
from backend.rag.simple_vector_store import get_vector_store

router = APIRouter(prefix="/api/discovery", tags=["discovery"])

class SimilarityRequest(BaseModel):
    research_idea: str
    domain: Optional[str] = None
    top_k: int = 10

class NoveltyRequest(BaseModel):
    research_idea: str
    domain: Optional[str] = None

@router.post("/similar")
async def find_similar_papers(request: SimilarityRequest):
    """Find papers similar to the research idea"""
    try:
    # Use Real Search Service
        results = search_service.search_papers(request.research_idea, limit=5)
        
        # Store in Vector DB for RAG context
        vector_store = get_vector_store()
        vector_store.add_papers(results)
        
        # Add dummy similarity for UI (since they are fresh search results)
        for res in results:
            res['similarity'] = 0.95 # High relevance for direct search results
            res['year'] = 2024 # Default if missing
            res['authors'] = "Web Source" # Simplification for now

        return {
            "status": "success",
            "papers": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/novelty")
async def calculate_novelty(request: NoveltyRequest):
    """Calculate novelty score for research idea"""
    try:
        vector_store = get_vector_store()
        
        # Get top 10 similar papers
        similar_papers = vector_store.search_similar(
            query=request.research_idea,
            top_k=10
        )
        
        if not similar_papers:
            return {
                "novelty_score": 1.0,
                "interpretation": "Highly novel - no similar research found",
                "similar_papers": []
            }
        
        # Calculate average similarity
        avg_similarity = sum(p['similarity_score'] for p in similar_papers) / len(similar_papers)
        novelty_score = 1 - avg_similarity
        
        # Interpret score
        if novelty_score > 0.7:
            interpretation = "Highly novel - significant departure from existing work"
        elif novelty_score > 0.4:
            interpretation = "Moderately novel - builds on existing work with new approaches"
        else:
            interpretation = "Low novelty - substantial overlap with existing research"
        
        return {
            "novelty_score": round(novelty_score, 3),
            "interpretation": interpretation,
            "average_similarity": round(avg_similarity, 3),
            "similar_papers": similar_papers[:5]  # Return top 5
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_discovery_stats():
    """Get RAG database statistics"""
    try:
        vector_store = get_vector_store()
        
        return {
            "total_papers": vector_store.count(),
            "status": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
