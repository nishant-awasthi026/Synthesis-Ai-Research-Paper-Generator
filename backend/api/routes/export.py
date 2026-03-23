from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from backend.config import settings

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.post("/zip")
async def export_zip(paper_data: dict):
    """
    Export the generated research and base papers as a zip archive.
    Expects standard paper output including latex code.
    """
    title = paper_data.get("title", "Research_Paper").replace(" ", "_")
    
    # Create an in-memory or temp zip
    temp_zip = NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(temp_zip.name, 'w') as zf:
        # Write LaTeX file
        latex_content = paper_data.get("latex_code", "% Default LaTeX template")
        zf.writestr(f"{title}/main.tex", latex_content)
        
        # Write Colab notebook
        colab_code = paper_data.get("colab_code", "# Google Colab ML/DL training code\n")
        
        # simple ipynb format
        ipynb_content = f'{{"cells": [{{"cell_type": "code", "execution_count": null, "metadata": {{}}, "outputs": [], "source": {repr(colab_code.splitlines(True))}}}], "metadata": {{"kernelspec": {{"display_name": "Python 3", "language": "python", "name": "python3"}}}}, "nbformat": 4, "nbformat_minor": 4}}'
        zf.writestr(f"{title}/code/model_training.ipynb", ipynb_content)

        # Write Survey & Methodology Text
        survey = paper_data.get("literature_survey", "No survey provided.")
        methodology = paper_data.get("methodology", "No methodology provided.")
        zf.writestr(f"{title}/sections/01_Literature_Survey.md", survey)
        zf.writestr(f"{title}/sections/02_Methodology.md", methodology)
        
        # Ideally, we would copy base PDFs here if they were stored in UPLOADS_DIR
        base_papers = paper_data.get("base_papers", [])
        for bp in base_papers:
            bp_title = bp.get("title", "Unknown_Paper").replace(" ", "_")
            zf.writestr(f"{title}/base_papers/{bp_title}.txt", bp.get("abstract", ""))

    return FileResponse(
        temp_zip.name,
        media_type="application/x-zip-compressed",
        filename=f"{title}_package.zip",
        background=None
    )
