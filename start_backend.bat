@echo off
REM Start Backend Server Script

cd /d "D:\Synthesis- Ai Research Paper Generator"
set PYTHONPATH=D:\Synthesis- Ai Research Paper Generator

echo Starting backend server on http://localhost:8000...
python -m uvicorn backend.main:app --reload --port 8000 --host 0.0.0.0

pause
