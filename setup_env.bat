@echo off
rem ---------------------------------------------------------------------------
rem Setup script for EnQue backend development environment (Windows).
rem Creates a Python virtual environment, installs required packages, and prepares
rem a .env file with placeholders.
rem ---------------------------------------------------------------------------

set "PROJECT_ROOT=%~dp0"
set "VENV_DIR=%PROJECT_ROOT%venv"

rem If a virtual environment already exists, skip creation.
if exist "%VENV_DIR%\Scripts\python.exe" (
    echo Virtual environment already exists at %VENV_DIR%
) else (
    echo Creating virtual environment ...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Ensure Python is installed and on PATH.
        exit /b 1
    )
)

rem Activate the virtual environment
call "%VENV_DIR%\Scripts\activate"

rem Upgrade pip and install requirements
python -m pip install --upgrade pip
if not exist "%PROJECT_ROOT%backend\requirements.txt" (
    echo requirements.txt not found. Check project structure.
    exit /b 1
)
pip install -r "%PROJECT_ROOT%backend\requirements.txt"

rem Create a .env file with placeholder values if it does not exist
if not exist "%PROJECT_ROOT%\.env" (
    echo Creating .env template ...
    (echo # EnQue backend environment variables
    echo DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/enge
    echo HINDSIGHT_BASE_URL=YOUR_HINDSIGHT_BASE_URL
    echo HINDSIGHT_API_KEY=YOUR_HINDSIGHT_API_KEY) > "%PROJECT_ROOT%\.env"
    echo .env created. Edit the values as needed.
) else (
    echo .env already exists. Skipping creation.
)

echo Setup complete. You can now run the backend with run.bat.

