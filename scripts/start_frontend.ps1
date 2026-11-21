# SignBridge AI - Start Frontend Development Server
# Run in PowerShell: powershell -ExecutionPolicy Bypass -File scripts\start_frontend.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
$FrontendDir = Join-Path $RootDir "frontend"

Set-Location $FrontendDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  SignBridge AI — Frontend Vite Server Launcher" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check node_modules
if (-not (Test-Path (Join-Path $FrontendDir "node_modules"))) {
    Write-Host "[Info] Node modules not found. Running npm install..." -ForegroundColor Yellow
    npm.cmd install
}

# 2. Launch Vite Dev Server
Write-Host "[Vite] Launching Frontend at http://localhost:5173..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray

npm.cmd run dev -- --host

