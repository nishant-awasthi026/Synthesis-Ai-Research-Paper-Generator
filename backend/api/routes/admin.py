"""
Admin Dashboard API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from backend.database.database import get_db
from backend.database.models import ResearchPaper, ExternalPaper, IngestionLog
from backend.rag.vector_store import get_vector_store
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    """Get comprehensive admin statistics"""
    try:
        # Paper stats
        total_papers = db.query(ResearchPaper).count()
        draft_papers = db.query(ResearchPaper).filter(
            ResearchPaper.status == "draft"
        ).count()
        completed_papers = db.query(ResearchPaper).filter(
            ResearchPaper.status == "completed"
        ).count()
        
        # External papers (RAG database)
        external_papers = db.query(ExternalPaper).count()
        
        # Vector store stats
        try:
            vs = get_vector_store()
            vector_count = vs.count()
        except:
            vector_count = 0
        
        # Recent ingestion logs
        recent_logs = db.query(IngestionLog).order_by(
            IngestionLog.date.desc()
        ).limit(5).all()
        
        # Papers created in last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_papers = db.query(ResearchPaper).filter(
            ResearchPaper.created_at >= week_ago
        ).count()
        
        return {
            "user_papers": {
                "total": total_papers,
                "draft": draft_papers,
                "in_progress": total_papers - draft_papers - completed_papers,
                "completed": completed_papers,
                "recent_7_days": recent_papers
            },
            "rag_database": {
                "external_papers": external_papers,
                "vector_embeddings": vector_count,
                "last_updated": recent_logs[0].date.isoformat() if recent_logs else None
            },
            "ingestion": {
                "total_runs": db.query(IngestionLog).count(),
                "successful_runs": db.query(IngestionLog).filter(
                    IngestionLog.status == "success"
                ).count(),
                "recent_logs": [
                    {
                        "date": log.date.isoformat(),
                        "papers_added": log.papers_added,
                        "status": log.status,
                        "sources": log.sources
                    }
                    for log in recent_logs
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/papers/stats")
async def get_paper_stats(db: Session = Depends(get_db)):
    """Get detailed paper statistics"""
    try:
        # Papers by domain
        domain_stats = db.query(
            ResearchPaper.domain,
            func.count(ResearchPaper.id).label('count')
        ).group_by(ResearchPaper.domain).all()
        
        # Papers by status
        status_stats = db.query(
            ResearchPaper.status,
            func.count(ResearchPaper.id).label('count')
        ).group_by(ResearchPaper.status).all()
        
        return {
            "by_domain": [
                {"domain": d[0] or "Unspecified", "count": d[1]}
                for d in domain_stats
            ],
            "by_status": [
                {"status": s[0].value if s[0] else "unknown", "count": s[1]}
                for s in status_stats
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ingestion/logs")
async def get_ingestion_logs(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get ingestion logs with pagination"""
    try:
        total = db.query(IngestionLog).count()
        logs = db.query(IngestionLog).order_by(
            IngestionLog.date.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "logs": [
                {
                    "id": log.id,
                    "date": log.date.isoformat(),
                    "papers_added": log.papers_added,
                    "sources": log.sources,
                    "status": log.status,
                    "error_message": log.error_message
                }
                for log in logs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
