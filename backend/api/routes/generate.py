"""
Paper generation API routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from backend.llm.generator import get_generator

router = APIRouter(prefix="/api/generate", tags=["generation"])

class SectionRequest(BaseModel):
    section_type: str  # abstract, introduction, lit_review, etc.
    title: str
    domain: Optional[str] = ""
    problem: Optional[str] = ""
    methodology: Optional[str] = ""
    results: Optional[str] = ""
    approach: Optional[str] = ""
    focus: Optional[str] = ""
    use_rag: bool = True
    rag_top_k: int = 5

class TopicRequest(BaseModel):
    domain: str
    keywords: List[str]
    user_interest: str

@router.post("/section")
async def generate_section(request: SectionRequest):
    """Generate a research paper section"""
    try:
        generator = get_generator()
        
        # Prepare user input
        user_input = {
            'title': request.title,
            'domain': request.domain,
            'problem': request.problem,
            'methodology': request.methodology,
            'results': request.results,
            'approach': request.approach,
            'focus': request.focus,
            'abstract': '',  # Can be filled if available
            'contributions': '',
            'results_summary': '',
            'experimental_results': ''
        }
        
        # Generate section
        result = generator.generate_section(
            section_type=request.section_type,
            user_input=user_input,
            use_rag=request.use_rag,
            rag_top_k=request.rag_top_k
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            **result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics")
async def generate_topics(request: TopicRequest):
    """Generate research topic ideas"""
    try:
        generator = get_generator()
        
        result = generator.generate_topic_ideas(
            domain=request.domain,
            keywords=request.keywords,
            user_interest=request.user_interest
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sections")
async def list_sections():
    """List available section types"""
    return {
        "sections": [
            "topic_generation",
            "abstract",
            "introduction",
            "lit_review",
            "methodology",
            "results",
            "discussion",
            "conclusion"
        ]
    }
