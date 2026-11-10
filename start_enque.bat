@echo off
echo ========================================================
echo Starting EnQue Platform (Backend + Frontend)
echo ========================================================

set PYTHONPATH=%~dp0

start "EnQue Backend (FastAPI)" cmd /k "cd /d %~dp0 && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

start "EnQue Frontend (React+Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================================
echo EnQue is launching!
echo Backend API Docs: http://localhost:8000/docs
echo Frontend Web App: http://localhost:5173
echo ========================================================

