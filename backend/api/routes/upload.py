"""
File Upload API Routes
Handles experimental results uploads
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil
from pathlib import Path
from datetime import datetime

from backend.database.database import get_db
from backend.database.models import ResearchPaper, ExperimentNotebook
from backend.utils.parsers import ResultsParser, ColabNotebookHandler
from backend.config import settings

router = APIRouter(prefix="/api/papers", tags=["uploads"])


class ColabLinkRequest(BaseModel):
    colab_url: str
    description: Optional[str] = None

# File size limits (bytes)
MAX_NOTEBOOK_SIZE = 10 * 1024 * 1024  # 10MB
MAX_DATA_FILE_SIZE = 5 * 1024 * 1024   # 5MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'ipynb'}

def get_file_extension(filename: str) -> str:
    """Extract file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def validate_file_size(file_size: int, file_type: str) -> bool:
    """Validate file size based on type"""
    if file_type == 'ipynb':
        return file_size <= MAX_NOTEBOOK_SIZE
    else:
        return file_size <= MAX_DATA_FILE_SIZE


@router.post("/{paper_id}/upload/results")
async def upload_results(
    paper_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Upload experimental results file
    
    Supported formats: txt, csv, json, ipynb
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Validate file extension
    file_ext = get_file_extension(file.filename)
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    if not validate_file_size(file_size, file_ext):
        max_size = MAX_NOTEBOOK_SIZE if file_ext == 'ipynb' else MAX_DATA_FILE_SIZE
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {max_size / (1024*1024):.1f}MB"
        )
    
    # Create upload directory
    upload_dir = Path(settings.DATA_DIR) / "uploads" / paper_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = upload_dir / file.filename
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Parse file
    parser = ResultsParser()
    try:
        parsed_data = parser.parse_file(str(file_path), file_ext)
    except Exception as e:
        # Clean up file on parse error
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse file: {str(e)}"
        )
    
    # Create database record
    experiment = ExperimentNotebook(
        paper_id=paper_id,
        notebook_url=str(file_path),
        file_path=str(file_path),
        file_type=file_ext,
        execution_status="parsed",
        results_data=parsed_data,
        parsed_results=parsed_data
    )
    
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    
    return {
        "success": True,
        "experiment_id": experiment.id,
        "file_name": file.filename,
        "file_type": file_ext,
        "file_size": file_size,
        "parsed_data": parsed_data,
        "message": "Results uploaded and parsed successfully"
    }


@router.post("/{paper_id}/upload/notebook")
async def upload_notebook(
    paper_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Upload Jupyter notebook (.ipynb)
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Validate file is notebook
    if not file.filename.endswith('.ipynb'):
        raise HTTPException(
            status_code=400,
            detail="File must be a Jupyter notebook (.ipynb)"
        )
    
    # Read file
    content = await file.read()
    file_size = len(content)
    
    # Validate size
    if file_size > MAX_NOTEBOOK_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Notebook too large. Maximum: {MAX_NOTEBOOK_SIZE / (1024*1024):.1f}MB"
        )
    
    # Create directory
    upload_dir = Path(settings.DATA_DIR) / "uploads" / paper_id / "notebooks"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save notebook
    file_path = upload_dir / file.filename
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Parse notebook
    parser = ResultsParser()
    try:
        parsed_data = parser.parse_notebook(str(file_path))
        results_summary = parser.extract_notebook_results(parsed_data)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse notebook: {str(e)}"
        )
    
    # Create record
    experiment = ExperimentNotebook(
        paper_id=paper_id,
        notebook_url=str(file_path),
        file_path=str(file_path),
        file_type='ipynb',
        execution_status="uploaded",
        results_data=parsed_data,
        parsed_results=results_summary
    )
    
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    
    return {
        "success": True,
        "experiment_id": experiment.id,
        "file_name": file.filename,
        "notebook_summary": results_summary,
        "parsed_data": parsed_data,
        "message": "Notebook uploaded and analyzed successfully"
    }


@router.post("/{paper_id}/upload/colab")
async def link_colab_notebook(
    paper_id: str,
    request: ColabLinkRequest,
    db: Session = Depends(get_db)
):
    """
    Link Google Colab notebook
    
    Note: Actual download requires authentication
    This endpoint stores the URL for manual review
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Parse Colab URL
    colab_info = ColabNotebookHandler.parse_colab_url(request.colab_url)
    
    if not colab_info['valid']:
        raise HTTPException(
            status_code=400,
            detail="Invalid Colab URL"
        )
    
    # Create record
    experiment = ExperimentNotebook(
        paper_id=paper_id,
        notebook_url=request.colab_url,
        file_path=None,
        file_type='colab',
        execution_status="linked",
        results_data={
            'colab_info': colab_info,
            'linked_at': datetime.utcnow().isoformat()
        },
        parsed_results={}
    )
    
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    
    return {
        "success": True,
        "experiment_id": experiment.id,
        "colab_url": request.colab_url,
        "colab_info": colab_info,
        "message": "Colab notebook linked successfully",
        "note": "Please ensure notebook is publicly accessible"
    }


@router.get("/{paper_id}/results")
async def get_paper_results(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all uploaded results for a paper
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Get all experiments
    experiments = db.query(ExperimentNotebook).filter(
        ExperimentNotebook.paper_id == paper_id
    ).all()
    
    results = []
    for exp in experiments:
        results.append({
            "id": exp.id,
            "file_type": exp.file_type,
            "file_path": exp.file_path,
            "notebook_url": exp.notebook_url,
            "execution_status": exp.execution_status,
            "parsed_results": exp.parsed_results,
            "created_at": exp.created_at.isoformat() if exp.created_at else None,
            "updated_at": exp.updated_at.isoformat() if exp.updated_at else None
        })
    
    return {
        "paper_id": paper_id,
        "total_results": len(results),
        "results": results
    }


@router.delete("/{paper_id}/results/{experiment_id}")
async def delete_result(
    paper_id: str,
    experiment_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete uploaded result
    """
    # Get experiment
    experiment = db.query(ExperimentNotebook).filter(
        ExperimentNotebook.id == experiment_id,
        ExperimentNotebook.paper_id == paper_id
    ).first()
    
    if not experiment:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Delete file if exists
    if experiment.file_path and os.path.exists(experiment.file_path):
        try:
            os.remove(experiment.file_path)
        except Exception as e:
            print(f"Warning: Could not delete file: {e}")
    
    # Delete from database
    db.delete(experiment)
    db.commit()
    
    return {
        "success": True,
        "message": "Result deleted successfully"
    }
