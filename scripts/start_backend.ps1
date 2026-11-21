# SignBridge AI - Start Backend Server
# Run in PowerShell: powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  SignBridge AI — Backend Service Launcher" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Virtual Environment Verification
$VenvPython = Join-Path $RootDir "backend\venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "[Info] Python virtual environment not detected. Creating backend\venv..." -ForegroundColor Yellow
    python -m venv (Join-Path $RootDir "backend\venv")
    & $VenvPython -m pip install --upgrade pip
    & $VenvPython -m pip install -r (Join-Path $RootDir "backend\requirements.txt")
}

# 2. Database Initialization and Seeding
Write-Host "[Database] Verifying database tables and authentic ISL seed data..." -ForegroundColor Green
& $VenvPython -m backend.app.database.seed

# 3. Launch FastAPI Server
Write-Host "[Server] Launching FastAPI at http://127.0.0.1:8000..." -ForegroundColor Green
Write-Host "[Docs] Interactive Swagger API Docs at http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to terminate." -ForegroundColor DarkGray

& $VenvPython -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

