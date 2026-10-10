@echo off
title OmniTracker - Local-First Development Launcher
echo ========================================================
echo               OmniTracker Launcher (2026)
echo ========================================================
echo.

cd /d "%~dp0\.."

echo [*] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "OmniTracker Backend" cmd /k "backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --port 8000 --reload"

echo [*] Starting Vite Frontend on http://localhost:5173 ...
start "OmniTracker Frontend" cmd /k "cd frontend && npm.cmd run dev"

echo [*] Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak >nul

echo [*] Opening OmniTracker in default browser...
start http://localhost:5173

echo.
echo OmniTracker is now running!
echo Backend API Docs: http://127.0.0.1:8000/docs
echo Web Application:  http://localhost:5173
echo.
