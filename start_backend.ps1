# Start Backend Server Script (PowerShell)

$env:PYTHONPATH="D:\Synthesis- Ai Research Paper Generator"
$env:PYTHONUTF8="1"
$env:OPENBLAS_NUM_THREADS="1"
$env:OMP_NUM_THREADS="1"
Set-Location "D:\Synthesis- Ai Research Paper Generator"

Write-Host "Starting backend server on http://localhost:8000..." -ForegroundColor Green
python -m uvicorn backend.main:app --port 8000 --host 0.0.0.0
