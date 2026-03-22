@echo off
echo.
echo ========================================
echo   33-Agent System Activation
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Check for J:/K:/ drives
echo Checking drive mappings...
if exist J:\ (
    echo ✓ J: Drive found (Execution Engine)
) else (
    echo ⚠ J: Drive not found - some features may be limited
)

if exist K:\ (
    echo ✓ K: Drive found (Logic DNA)
) else (
    echo ⚠ K: Drive not found - some features may be limited
)

if exist L:\ (
    echo ✓ L: Drive found (Swarm Memory)
) else (
    echo ⚠ L: Drive not found - some features may be limited
)

echo.
echo ========================================
echo   Starting 33-Agent System...
echo ========================================
echo.

REM Start the boot sequence
python boot_sequence.py

REM If boot sequence exits, keep virtual environment active
echo.
echo System has stopped.
echo Virtual environment is still active.
echo Type 'deactivate' to exit virtual environment.
pause