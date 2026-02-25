@echo off
REM Quick Start Script for Always-On AI Keyboard Demo
REM Windows Batch Script

echo ========================================
echo ALWAYS-ON AI KEYBOARD - QUICK START
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo.
    echo PyQt5 not found. Installing dependencies...
    echo This may take a few minutes...
    pip install -r requirements_ui.txt
    echo.
)

echo [2/4] Testing AI Engine...
python -c "from ai_engine import api_service; print('AI Engine OK')"
if errorlevel 1 (
    echo ERROR: AI Engine not working
    pause
    exit /b 1
)

echo [3/4] Testing UI Module...
python -c "from ui_module import interface; print('UI Module OK')"
if errorlevel 1 (
    echo ERROR: UI Module not working
    pause
    exit /b 1
)

echo [4/4] Starting demo...
echo.
echo ========================================
echo RUNNING INTEGRATION DEMO (MOCK MODE)
echo ========================================
echo.
echo This demo shows:
echo   - Ghost text suggestions
echo   - Accept/Reject with Tab/Esc
echo   - Voice input simulation
echo   - AI confidence visualization
echo.
echo Close the window when done!
echo ========================================
echo.

python demo_integration.py

echo.
echo ========================================
echo Demo complete!
echo.
echo Next steps:
echo   1. Run real AI: start_real_ai_demo.bat
echo   2. Interactive test: python demo_interactive.py
echo   3. Read docs: ui_module\README.md
echo ========================================
pause
