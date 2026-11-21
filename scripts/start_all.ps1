# SignBridge AI - Launch Complete Application (Backend + Frontend)
# Run in PowerShell: powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  SignBridge AI — Unified Development Environment" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Starting Backend and Frontend services..." -ForegroundColor Green

# Start Backend in a new window
$BackendScript = Join-Path $ScriptDir "start_backend.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$BackendScript`""

Start-Sleep -Seconds 2

# Start Frontend in a new window
$FrontendScript = Join-Path $ScriptDir "start_frontend.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$FrontendScript`""

Write-Host ""
Write-Host "Services launched successfully in separate consoles:" -ForegroundColor Green
Write-Host "  - Backend API:    http://127.0.0.1:8000 (Docs: http://127.0.0.1:8000/docs)" -ForegroundColor Yellow
Write-Host "  - Frontend App:   http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open http://localhost:5173 in your browser to start using SignBridge AI!" -ForegroundColor Cyan

