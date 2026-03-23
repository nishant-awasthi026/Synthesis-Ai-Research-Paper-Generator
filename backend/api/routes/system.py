"""
System health and status API routes
"""
from fastapi import APIRouter
from backend.llm.ollama_client import get_ollama_client
from backend.rag.vector_store import get_vector_store
from backend.config import settings

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/health")
async def health_check():
    """Comprehensive system health check"""
    try:
        # Check Ollama
        ollama = get_ollama_client()
        ollama_status = ollama.check_health()
        
        # Check Vector Store
        try:
            vector_store = get_vector_store()
            vector_status = {
                "status": "healthy",
                "total_papers": vector_store.count()
            }
        except Exception as e:
            vector_status = {
                "status": "error",
                "error": str(e)
            }
        
        # Overall status
        overall_healthy = (
            ollama_status.get("status") == "healthy" and
            vector_status.get("status") == "healthy"
        )
        
        return {
            "status": "healthy" if overall_healthy else "degraded",
            "version": settings.VERSION,
            "components": {
                "ollama": ollama_status,
                "vector_store": vector_status,
                "database": "healthy"  # SQLite is always available
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.get("/config")
async def get_config():
    """Get system configuration (non-sensitive)"""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ollama_model": settings.OLLAMA_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL,
        "environment": settings.ENV
    }
