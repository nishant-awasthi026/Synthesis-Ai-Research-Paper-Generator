"""
Main FastAPI application for Synthesis AI Research Paper Generator
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database.database import init_db

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered Research Paper Generator with RAG system"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    init_db()
    print(f"✅ Application ready at http://{settings.API_HOST}:{settings.API_PORT}")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Synthesis AI Research Paper Generator API",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "operational"
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": "connected",
        "ollama": "checking..."
    }

# Import and include routers
from backend.api.routes import discovery, generate, system, papers, citations, admin, export, upload, validation, auth, chat

app.include_router(auth.router)
app.include_router(discovery.router)
app.include_router(generate.router)
app.include_router(system.router)
app.include_router(papers.router)
app.include_router(citations.router)
app.include_router(admin.router)
app.include_router(export.router)
app.include_router(upload.router)
app.include_router(validation.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
