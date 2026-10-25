# ==============================================================================
# SIH26035: Automated OIML R-76 Guided NAWI Testing Suite
# PowerShell Runner for Windows
# Run with: powershell -ExecutionPolicy Bypass -File .\run_workbench.ps1
# ==============================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   🇮🇳 SMART INDIA HACKATHON (SIH26035) — LEGAL METROLOGY WORKBENCH" -ForegroundColor Yellow
Write-Host "   Automated OIML R-76 Guided Testing, PDF/A-3, PTB DCC v3.2.1 & Ed25519" -ForegroundColor White
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Find Python
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} else {
    Write-Host "[ERROR] Python was not found in your system PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Ensure 'Add Python to PATH' is checked during installation."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[*] Detected Python command: $pythonCmd" -ForegroundColor Green

# Create Virtual Environment if not exists
if (-not (Test-Path ".venv")) {
    Write-Host "[+] Creating virtual environment in .venv..." -ForegroundColor Yellow
    & $pythonCmd -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# Determine venv python path
$venvPython = ".\.venv\Scripts\python.exe"
$venvPip = ".\.venv\Scripts\pip.exe"

# Activate environment in current PowerShell session
$activateScript = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
}

# Check if required modules are installed
$checkMod = & $venvPython -c "import fastapi, uvicorn, pydantic, cryptography, qrcode" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[+] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    & $venvPip install --upgrade pip
    & $venvPip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[✓] Environment verified and dependencies ready!" -ForegroundColor Green
Write-Host "[+] Launching Metrology Workbench on http://127.0.0.1:8000..." -ForegroundColor Cyan

# Open browser after 2 seconds in background
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:8000"
} | Out-Null

# Start FastAPI server
& $venvPython -m uvicorn api.main:app --app-dir src --host 127.0.0.1 --port 8000 --reload
