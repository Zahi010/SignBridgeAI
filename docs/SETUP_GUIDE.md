# SignBridge AI — Windows Local Setup Guide

This guide walks through configuring and launching SignBridge AI on a Windows workstation from scratch.

---

## 1. System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit)
- **Python:** Python 3.11, 3.12, or 3.13 (Python 3.13.3 tested)
- **Node.js:** Node v18+ (Node v24.17.0 tested)
- **Shell:** Windows PowerShell 5.1 or PowerShell Core 7+

---

## 2. Automated 1-Click Launch

The simplest way to run both backend and frontend simultaneously:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1
```

This will launch two separate console windows:
1. **Backend Server Console:** Runs FastAPI with auto-reload on `http://127.0.0.1:8000`.
2. **Frontend Console:** Runs Vite dev server on `http://localhost:5173`.

---

## 3. Step-by-Step Manual Installation

If you prefer to configure each component manually:

### Step A: Configure Python Virtual Environment & Backend
Open PowerShell in the workspace root (`e:\SignBridgeAi`):

```powershell
# 1. Create Python virtual environment
python -m venv backend\venv

# 2. Upgrade pip and install backend packages
backend\venv\Scripts\python.exe -m pip install --upgrade pip
backend\venv\Scripts\pip.exe install -r backend\requirements.txt

# 3. Initialize and seed SQLite database
backend\venv\Scripts\python.exe -m backend.app.database.seed

# 4. Start the FastAPI development server
backend\venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify backend health in your browser:
- Health check: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
- Swagger API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Step B: Configure Node.js & Frontend
Open a second PowerShell window in the workspace root:

```powershell
# 1. Install frontend packages using npm.cmd
npm.cmd install --prefix frontend

# 2. Start Vite development server
npm.cmd run dev --prefix frontend
```

Open the application in your browser:
- Application UI: [http://localhost:5173](http://localhost:5173)

---

## 4. Running the Test Suite

Run the full automated backend test suite:

```powershell
backend\venv\Scripts\pytest.exe -o pythonpath=. backend\tests -v
```

Verify the frontend production build:

```powershell
npm.cmd run build --prefix frontend
```

---

## 5. Troubleshooting Windows-Specific Issues

### Issue 1: PowerShell Script Execution Policy Error
**Symptom:** `npm : File ... npm.ps1 cannot be loaded because running scripts is disabled on this system.`  
**Fix:** Always use `npm.cmd` instead of `npm`, or execute PowerShell scripts with `-ExecutionPolicy Bypass`:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1
```

### Issue 2: Port Already in Use (8000 or 5173)
**Symptom:** `error: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`  
**Fix:** Find and terminate the process holding the port:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Issue 3: Corrupt or Missing Database
**Symptom:** `sqlite3.OperationalError: no such table: concepts`  
**Fix:** Re-run the database seeder to recreate all tables and data:
```powershell
backend\venv\Scripts\python.exe -m backend.app.database.seed
```

