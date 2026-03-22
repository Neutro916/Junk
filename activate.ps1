Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   33-Agent System Activation" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check for J:/K:/ drives
Write-Host "Checking drive mappings..." -ForegroundColor Yellow
if (Test-Path "J:\") {
    Write-Host "✓ J: Drive found (Execution Engine)" -ForegroundColor Green
} else {
    Write-Host "⚠ J: Drive not found - some features may be limited" -ForegroundColor Yellow
}

if (Test-Path "K:\") {
    Write-Host "✓ K: Drive found (Logic DNA)" -ForegroundColor Green
} else {
    Write-Host "⚠ K: Drive not found - some features may be limited" -ForegroundColor Yellow
}

if (Test-Path "L:\") {
    Write-Host "✓ L: Drive found (Swarm Memory)" -ForegroundColor Green
} else {
    Write-Host "⚠ L: Drive not found - some features may be limited" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting 33-Agent System..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the boot sequence
python boot_sequence.py

# If boot sequence exits
Write-Host ""
Write-Host "System has stopped." -ForegroundColor Yellow
Write-Host "Virtual environment is still active." -ForegroundColor Gray
Write-Host "Type 'deactivate' to exit virtual environment." -ForegroundColor Gray
Read-Host "Press Enter to continue"