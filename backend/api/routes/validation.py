"""
Validation API Routes
Integrates validation systems for results, plagiarism, AI content, and ethics
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime

from backend.database.database import get_db
from backend.database.models import ResearchPaper, ValidationResult, ExperimentNotebook
from backend.validation.results_validator import ResultsValidator, validate_notebook_results, validate_csv_results
from backend.validation.ethics_checker import PlagiarismChecker, AIContentDetector, EthicsChecker

router = APIRouter(prefix="/api/papers", tags=["validation"])


@router.post("/{paper_id}/validate/results")
async def validate_paper_results(
    paper_id: str,
    run_statistical_checks: bool = True,
    verify_reproducibility: bool = False,
    db: Session = Depends(get_db)
):
    """
    Validate experimental results for scientific integrity
    
    Checks:
    - Statistical red flags
    - Reproducibility indicators
    - Data completeness
    - Plausibility
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Get experiments for this paper
    experiments = db.query(ExperimentNotebook).filter(
        ExperimentNotebook.paper_id == paper_id
    ).all()
    
    if not experiments:
        raise HTTPException(
            status_code=400,
            detail="No experimental results uploaded. Please upload results first."
        )
    
    # Validate each experiment
    validator = ResultsValidator()
    all_results = []
    
    for exp in experiments:
        if exp.parsed_results:
            result = validator.validate_results(exp.parsed_results)
            result['experiment_id'] = exp.id
            result['file_type'] = exp.file_type
            all_results.append(result)
    
    # Aggregate results
    if not all_results:
        raise HTTPException(
            status_code=400,
            detail="No parsed results available for validation"
        )
    
    # Calculate overall score (average of all experiments)
    avg_score = sum(r['score'] for r in all_results) / len(all_results)
    
    # Aggregate warnings
    all_warnings = []
    for r in all_results:
        all_warnings.extend(r.get('warnings', []))
    
    # Determine status
    if avg_score >= 0.8:
        status = "passed"
    elif avg_score >= 0.5:
        status = "warnings"
    else:
        status = "failed"
    
    # Create validation record
    validation = ValidationResult(
        paper_id=paper_id,
        validation_type="results",
        status=status,
        score=avg_score,
        warnings=all_warnings,
        recommendations=all_results[0].get('recommendations', []),
        details={
            'individual_results': all_results,
            'experiments_validated': len(all_results)
        }
    )
    
    db.add(validation)
    db.commit()
    db.refresh(validation)
    
    return {
        "validation_id": validation.id,
        "status": status,
        "score": avg_score,
        "warnings": all_warnings,
        "recommendations": validation.recommendations,
        "details": validation.details,
        "message": f"Validated {len(all_results)} experimental results"
    }


@router.post("/{paper_id}/validate/plagiarism")
async def check_plagiarism(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Check paper for plagiarism against RAG database
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Get paper text
    paper_data = paper.paper_data or {}
    sections = ['abstract', 'introduction', 'methodology', 'results', 'conclusion']
    paper_text = '\n\n'.join([
        paper_data.get(section, '') for section in sections
    ])
    
    if not paper_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Paper has no content to check"
        )
    
    # Run plagiarism check
    checker = PlagiarismChecker()
    result = checker.check_paper(paper_text)
    
    # Create validation record
    validation = ValidationResult(
        paper_id=paper_id,
        validation_type="plagiarism",
        status=result['status'],
        score=1.0 - result['max_similarity'],  # Invert: higher score = less plagiarism
        warnings=result.get('warnings', []),
        recommendations=[result['recommendation']],
        details=result
    )
    
    db.add(validation)
    db.commit()
    db.refresh(validation)
    
    # Update paper's plagiarism score
    paper.plagiarism_score = result['max_similarity']
    db.commit()
    
    return {
        "validation_id": validation.id,
        "status": result['status'],
        "max_similarity": result['max_similarity'],
        "suspicious_paragraphs": result['suspicious_paragraphs'],
        "recommendation": result['recommendation'],
        "message": f"Checked {result['paragraphs_checked']} paragraphs"
    }


@router.post("/{paper_id}/validate/ai-content")
async def detect_ai_content(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Detect AI-generated content in paper
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Get paper text
    paper_data = paper.paper_data or {}
    sections = ['abstract', 'introduction', 'methodology', 'results', 'conclusion']
    paper_text = '\n\n'.join([
        paper_data.get(section, '') for section in sections
    ])
    
    if not paper_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Paper has no content to check"
        )
    
    # Run AI detection
    detector = AIContentDetector()
    result = detector.detect(paper_text)
    
    # Create validation record
    validation = ValidationResult(
        paper_id=paper_id,
        validation_type="ai_content",
        status=result['status'],
        score=1.0 - result['ai_probability'],  # Higher score = less AI
        warnings=result.get('warnings', []),
        recommendations=[result['recommendation']],
        details=result
    )
    
    db.add(validation)
    db.commit()
    db.refresh(validation)
    
    return {
        "validation_id": validation.id,
        "status": result['status'],
        "ai_probability": result['ai_probability'],
        "indicators_found": result['indicators_found'],
        "recommendation": result['recommendation']
    }


@router.post("/{paper_id}/validate/ethics")
async def check_ethics(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Check paper against ethical research standards
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Get citations count
    citations_count = len(paper.citations)
    
    # Get experiments count
    experiments_count = db.query(ExperimentNotebook).filter(
        ExperimentNotebook.paper_id == paper_id
    ).count()
    
    # Prepare paper data for checker
    checker_data = {
        'paper_data': paper.paper_data or {},
        'citations': paper.citations,
        'citations_count': citations_count,
        'experiments_count': experiments_count
    }
    
    # Run ethics check
    checker = EthicsChecker()
    result = checker.check_paper(checker_data)
    
    # Calculate score (percentage of checks passed)
    checks = result['checks']
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    score = passed / total if total > 0 else 0
    
    # Create validation record
    validation = ValidationResult(
        paper_id=paper_id,
        validation_type="ethics",
        status=result['status'],
        score=score,
        warnings=result.get('issues', []),
        recommendations=[result['recommendation']],
        details=result
    )
    
    db.add(validation)
    db.commit()
    db.refresh(validation)
    
    return {
        "validation_id": validation.id,
        "status": result['status'],
        "score": score,
        "checks": result['checks'],
        "issues": result['issues'],
        "recommendation": result['recommendation']
    }


@router.post("/{paper_id}/validate/all")
async def run_all_validations(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Run all validation checks
    """
    results = {}
    
    # Results validation
    try:
        results['results'] = await validate_paper_results(paper_id, db=db)
    except HTTPException as e:
        results['results'] = {
            "status": "skipped",
            "message": str(e.detail)
        }
    
    # Plagiarism check
    try:
        results['plagiarism'] = await check_plagiarism(paper_id, db=db)
    except HTTPException as e:
        results['plagiarism'] = {
            "status": "skipped",
            "message": str(e.detail)
        }
    
    # AI content detection
    try:
        results['ai_content'] = await detect_ai_content(paper_id, db=db)
    except HTTPException as e:
        results['ai_content'] = {
            "status": "skipped",
            "message": str(e.detail)
        }
    
    # Ethics check
    try:
        results['ethics'] = await check_ethics(paper_id, db=db)
    except HTTPException as e:
        results['ethics'] = {
            "status": "skipped",
            "message": str(e.detail)
        }
    
    return {
        "paper_id": paper_id,
        "validations": results,
        "message": "All validation checks completed"
    }


@router.post("/{paper_id}/pre-export-check")
async def pre_export_validation(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Comprehensive pre-export validation
    Blocks export if critical issues found
    """
    # Run all validations
    validations = await run_all_validations(paper_id, db=db)
    
    # Determine if export should be blocked
    blockers = []
    warnings_list = []
    
    # Check results validation
    results_val = validations['validations'].get('results', {})
    if results_val.get('status') == 'skipped':
        blockers.append("No experimental results uploaded")
    elif results_val.get('status') == 'failed':
        blockers.append("Results validation failed - suspicious data detected")
    
    # Check plagiarism
    plag_val = validations['validations'].get('plagiarism', {})
    if plag_val.get('max_similarity', 0) > 0.7:
        blockers.append("High plagiarism score detected")
    elif plag_val.get('max_similarity', 0) > 0.5:
        warnings_list.append("Moderate plagiarism similarity detected")
    
    # Check AI content
    ai_val = validations['validations'].get('ai_content', {})
    if ai_val.get('ai_probability', 0) > 0.7:
        warnings_list.append("High probability of AI-generated content")
    
    # Check ethics
    ethics_val = validations['validations'].get('ethics', {})
    if ethics_val.get('status') == 'failed':
        blockers.append("Ethics checklist failed - missing critical sections")
    elif ethics_val.get('status') == 'warnings':
        warnings_list.append("Some ethics checks not passed")
    
    # Determine overall status
    if blockers:
        overall_status = "blocked"
        message = "Export blocked due to critical issues"
    elif warnings_list:
        overall_status = "warnings"
        message = "Export allowed with warnings"
    else:
        overall_status = "ready"
        message = "Paper ready for export"
    
    return {
        "paper_id": paper_id,
        "status": overall_status,
        "blockers": blockers,
        "warnings": warnings_list,
        "validations": validations['validations'],
        "message": message,
        "can_export": len(blockers) == 0
    }


@router.get("/{paper_id}/validations")
async def get_validation_history(
    paper_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all validation results for a paper
    """
    # Verify paper exists
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Get all validations
    validations = db.query(ValidationResult).filter(
        ValidationResult.paper_id == paper_id
    ).order_by(ValidationResult.created_at.desc()).all()
    
    results = []
    for val in validations:
        results.append({
            "id": val.id,
            "validation_type": val.validation_type,
            "status": val.status,
            "score": val.score,
            "warnings": val.warnings,
            "recommendations": val.recommendations,
            "created_at": val.created_at.isoformat() if val.created_at else None
        })
    
    return {
        "paper_id": paper_id,
        "total_validations": len(results),
        "validations": results
    }
