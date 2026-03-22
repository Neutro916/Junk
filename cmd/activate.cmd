@echo off
echo.
echo [33-Agent System] Activation Command
echo.

REM Change to Junk directory
set JUNK_DIR=%~dp0..
cd /d "%JUNK_DIR%"

REM Check if Python files exist
if not exist "boot_sequence.py" (
    echo ERROR: boot_sequence.py not found in %JUNK_DIR%
    pause
    exit /b 1
)

REM Run the Python activation script
python cmd\activate.py

pause