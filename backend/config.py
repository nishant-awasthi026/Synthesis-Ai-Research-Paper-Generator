"""
Configuration settings for Synthesis AI Research Paper Generator
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Synthesis AI Research Paper Generator"
    VERSION: str = "1.0.0"
    ENV: str = "development"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CHROMADB_DIR: Path = DATA_DIR / "chromadb"
    SQLITE_DIR: Path = DATA_DIR / "sqlite"
    UPLOADS_DIR: Path = DATA_DIR / "uploads"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{SQLITE_DIR}/synthesis.db"
    
    # Ollama LLM
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    OLLAMA_TEMPERATURE: float = 0.7
    OLLAMA_MAX_TOKENS: int = 2000
    
    # Embeddings
    EMBEDDING_MODEL: str = "all-mpnet-base-v2"
    EMBEDDING_DIMENSION: int = 768  # all-mpnet-base-v2
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    # ChromaDB
    CHROMADB_PERSIST_DIR: str = str(CHROMADB_DIR)
    COLLECTION_NAME: str = "research_papers"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Ingestion
    DAILY_INGESTION_TIME: str = "02:00"
    PAPERS_PER_NICHE: int = 40
    MIN_PAPERS_TOTAL: int = 2000
    MAX_RESULTS_PER_API: int = 100
    
    # API Keys (Optional)
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    CORE_API_KEY: str = ""
    ENTREZ_EMAIL: str = "research@example.com"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # RAG
    RETRIEVAL_TOP_K: int = 10
    SIMILARITY_THRESHOLD: float = 0.5
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'CORS_ORIGINS':
                return [x.strip() for x in raw_val.split(',')]
            return raw_val

# Create settings instance
settings = Settings()

# Ensure directories exist
settings.CHROMADB_DIR.mkdir(parents=True, exist_ok=True)
settings.SQLITE_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
