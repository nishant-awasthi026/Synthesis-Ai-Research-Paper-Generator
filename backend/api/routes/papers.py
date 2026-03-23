"""
Paper Management API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.database.database import get_db
from backend.database.models import ResearchPaper, PaperStatus
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/papers", tags=["papers"])

class PaperCreate(BaseModel):
    title: str
    domain: Optional[str] = ""
    paper_data: Optional[Dict[str, Any]] = {}

class GenerateCodeRequest(BaseModel):
    title: str
    problem_description: Optional[str] = "Data Analysis"
    
class GenerateSectionRequest(BaseModel):
    section: str
    context: str

class PaperUpdate(BaseModel):
    title: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    paper_data: Optional[Dict[str, Any]] = None

class PaperResponse(BaseModel):
    id: str
    title: str
    domain: Optional[str]
    status: str
    novelty_score: Optional[float]
    created_at: datetime
    updated_at: datetime

@router.post("/create")
async def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    """Create a new research paper"""
    try:
        new_paper = ResearchPaper(
            user_id="default_user",  # TODO: Get from auth
            title=paper.title,
            domain=paper.domain,
            paper_data=paper.paper_data,
            status=PaperStatus.DRAFT
        )
        db.add(new_paper)
        db.commit()
        db.refresh(new_paper)
        
        return {
            "status": "success",
            "paper_id": new_paper.id,
            "message": "Paper created successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_papers(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all papers with pagination"""
    try:
        query = db.query(ResearchPaper)
        
        if status:
            query = query.filter(ResearchPaper.status == status)
        
        total = query.count()
        papers = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "papers": [
                {
                    "id": p.id,
                    "title": p.title,
                    "domain": p.domain,
                    "status": p.status.value if p.status else "draft",
                    "created_at": p.created_at.isoformat(),
                    "updated_at": p.updated_at.isoformat()
                }
                for p in papers
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{paper_id}")
async def get_paper(paper_id: str, db: Session = Depends(get_db)):
    """Get a specific paper by ID"""
    try:
        paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
        
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        return {
            "id": paper.id,
            "title": paper.title,
            "domain": paper.domain,
            "status": paper.status.value if paper.status else "draft",
            "novelty_score": paper.novelty_score,
            "paper_data": paper.paper_data,
            "created_at": paper.created_at.isoformat(),
            "updated_at": paper.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{paper_id}")
async def update_paper(
    paper_id: str,
    updates: PaperUpdate,
    db: Session = Depends(get_db)
):
    """Update a paper"""
    try:
        paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
        
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        if updates.title:
            paper.title = updates.title
        if updates.domain:
            paper.domain = updates.domain
        if updates.status:
            paper.status = PaperStatus(updates.status)
        if updates.paper_data:
            paper.paper_data = updates.paper_data
        
        paper.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "status": "success",
            "message": "Paper updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{paper_id}")
async def delete_paper(paper_id: str, db: Session = Depends(get_db)):
    """Delete a paper"""
    try:
        paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
        
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        db.delete(paper)
        db.commit()
        
        return {
            "status": "success",
            "message": "Paper deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/code")
async def generate_code(request: GenerateCodeRequest):
    """Generate Python code using Qwen"""
    try:
        from backend.llm.chat_agent import ChatAgent, Intent, IntentType
        agent = ChatAgent()
        
        prompt = f"Write a complete Python script for {request.title}. Focus on {request.problem_description}. Include imports, mock data creation, and model training. Return ONLY code."
        
        # We reuse the internal generation logic
        # For simplicity, we create a direct prompt
        import requests
        from backend.config import settings
        
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload)
        if response.status_code == 200:
            code = response.json().get("response", "")
            # Clean up markdown code blocks if present
            code = code.replace("```python", "").replace("```", "")
            return {"status": "success", "code": code}
        else:
            return {"status": "error", "code": "# Failed to generate code from LLM"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/section")
async def generate_section(request: GenerateSectionRequest):
    """Generate a paper section"""
    try:
        import requests
        from backend.config import settings
        
        prompt = f"Write the {request.section} section for a research paper. Context: {request.context}. Write academically."
        
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload)
        if response.status_code == 200:
            return {"status": "success", "content": response.json().get("response", "")}
        else:
            return {"status": "error", "content": "Failed to generate"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
