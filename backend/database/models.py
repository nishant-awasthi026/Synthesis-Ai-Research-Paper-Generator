"""
Database models for Synthesis AI Research Paper Generator
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class UserRole(str, enum.Enum):
    STUDENT = "student"
    RESEARCHER = "researcher"
    PROFESSOR = "professor"
    INDUSTRY = "industry"

class PaperStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class CitationFormat(str, enum.Enum):
    APA = "APA"
    IEEE = "IEEE"
    MLA = "MLA"
    CHICAGO = "Chicago"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    academic_role = Column(SQLEnum(UserRole), default=UserRole.STUDENT)
    research_interests = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    papers = relationship("ResearchPaper", back_populates="user", cascade="all, delete-orphan")

class ResearchPaper(Base):
    __tablename__ = "research_papers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    domain = Column(String)
    status = Column(SQLEnum(PaperStatus), default=PaperStatus.DRAFT)
    novelty_score = Column(Float)
    plagiarism_score = Column(Float)
    paper_data = Column(JSON, default=dict)  # Stores sections
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="papers")
    citations = relationship("Citation", back_populates="paper", cascade="all, delete-orphan")
    experiments = relationship("ExperimentNotebook", back_populates="paper", cascade="all, delete-orphan")
    validations = relationship("ValidationResult", back_populates="paper", cascade="all, delete-orphan")

class Citation(Base):
    __tablename__ = "citations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    paper_id = Column(String, ForeignKey("research_papers.id"), nullable=False)
    citation_text = Column(Text)
    citation_format = Column(SQLEnum(CitationFormat), default=CitationFormat.APA)
    doi = Column(String)
    url = Column(String)
    meta_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    paper = relationship("ResearchPaper", back_populates="citations")

class ExternalPaper(Base):
    __tablename__ = "external_papers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    abstract = Column(Text)
    authors = Column(JSON, default=list)
    doi = Column(String)
    publication_year = Column(Integer)
    embedding_id = Column(String)  # Reference to vector DB
    source = Column(String)  # arxiv, pubmed, etc.
    niches = Column(JSON, default=list)
    meta_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExperimentNotebook(Base):
    __tablename__ = "experiment_notebooks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    paper_id = Column(String, ForeignKey("research_papers.id"), nullable=False)
    notebook_url = Column(String)
    file_path = Column(String)  # Local file path for uploaded files
    file_type = Column(String)  # txt, csv, json, ipynb, colab
    execution_status = Column(String, default="pending")
    results_data = Column(JSON, default=dict)
    parsed_results = Column(JSON, default=dict)  # Processed results summary
    validation_status = Column(String)  # Validation status from ResultsValidator
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    paper = relationship("ResearchPaper", back_populates="experiments")

class ValidationResult(Base):
    __tablename__ = "validation_results"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    paper_id = Column(String, ForeignKey("research_papers.id"), nullable=False)
    validation_type = Column(String, nullable=False)  # results, plagiarism, ai_content, ethics
    status = Column(String, nullable=False)  # passed, warnings, failed
    score = Column(Float)
    warnings = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    paper = relationship("ResearchPaper", back_populates="validations")

class IngestionLog(Base):
    __tablename__ = "ingestion_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    date = Column(DateTime, default=datetime.utcnow)
    papers_added = Column(Integer, default=0)
    sources = Column(JSON, default=list)
    status = Column(String, default="success")
    error_message = Column(Text)
    meta_data = Column(JSON, default=dict)
