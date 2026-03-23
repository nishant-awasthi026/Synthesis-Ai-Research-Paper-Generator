"""
Citations API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from backend.database.database import get_db
from backend.database.models import Citation, CitationFormat
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/citations", tags=["citations"])

class CitationCreate(BaseModel):
    paper_id: str
    citation_text: str
    format: str = "APA"
    doi: Optional[str] = None
    url: Optional[str] = None

@router.post("/create")
async def create_citation(citation: CitationCreate, db: Session = Depends(get_db)):
    """Create a new citation"""
    try:
        new_citation = Citation(
            paper_id=citation.paper_id,
            citation_text=citation.citation_text,
            citation_format=CitationFormat(citation.format),
            doi=citation.doi,
            url=citation.url
        )
        db.add(new_citation)
        db.commit()
        db.refresh(new_citation)
        
        return {
            "status": "success",
            "citation_id": new_citation.id,
            "formatted": new_citation.citation_text
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paper/{paper_id}")
async def get_paper_citations(paper_id: str, db: Session = Depends(get_db)):
    """Get all citations for a paper"""
    try:
        citations = db.query(Citation).filter(Citation.paper_id == paper_id).all()
        
        return {
            "paper_id": paper_id,
            "count": len(citations),
            "citations": [
                {
                    "id": c.id,
                    "text": c.citation_text,
                    "format": c.citation_format.value if c.citation_format else "APA",
                    "doi": c.doi,
                    "url": c.url
                }
                for c in citations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/formats")
async def get_citation_formats():
    """Get available citation formats"""
    return {
        "formats": ["APA", "IEEE", "MLA", "Chicago"],
        "default": "APA"
    }
