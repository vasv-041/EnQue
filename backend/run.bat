@echo off
rem Simple script to run EnQue backend in development mode
rem Activate virtual environment (created by setup_env.bat)
if exist "venv\Scripts\activate" (
    call venv\Scripts\activate
) else (
    echo Virtual environment not found. Run setup_env.bat first.
    exit /b 1
)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

