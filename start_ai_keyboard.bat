@echo off
echo ======================================================================
echo AI KEYBOARD - QUICK START
echo ======================================================================
echo.
echo This will start:
echo   1. AI Engine server (background)
echo   2. Full AI Keyboard system
echo.
echo Prerequisites:
echo   - All dependencies installed (requirements*.txt)
echo   - Ollama running with llama3.2 model
echo   - Whisper models downloaded
echo.
echo ======================================================================
echo.

REM Start AI engine in background
start "AI Engine" cmd /c "uvicorn ai_engine.api_service:app --reload"

REM Wait for server to start
timeout /t 3 /nobreak > nul

REM Start keyboard service
python run_ai_keyboard.py

echo.
echo ======================================================================
echo Service stopped!
echo ======================================================================
pause
