@echo off
REM Start Real AI Demo
REM This script starts both AI engine and UI demo with real AI

echo ========================================
echo STARTING REAL AI DEMO
echo ========================================
echo.
echo This requires:
echo   1. Ollama installed and running
echo   2. llama3.2 model downloaded
echo.

REM Check Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama not running!
    echo.
    echo Please:
    echo   1. Install Ollama from ollama.ai
    echo   2. Run: ollama pull llama3.2
    echo   3. Start Ollama service
    echo.
    pause
    exit /b 1
)

echo Ollama detected!
echo.

echo [1/2] Starting AI Engine in background...
start "AI Engine" cmd /k "uvicorn ai_engine.api_service:app --reload"

echo Waiting for AI Engine to start...
timeout /t 5 /nobreak >nul

echo [2/2] Starting UI Demo with Real AI...
echo.
echo ========================================
echo REAL AI DEMO RUNNING
echo ========================================
echo.

python demo_integration.py --real-ai

echo.
echo Demo complete!
echo.
echo The AI Engine window is still running.
echo Close it manually or press Ctrl+C in that window.
echo.
pause
