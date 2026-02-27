@echo off
REM ========================================================
REM Cross-Application AI Text Rewriter Launcher
REM ========================================================
REM 
REM This starts the global AI text rewriting system.
REM Press Ctrl+Space in ANY app to improve selected text.
REM ========================================================

echo.
echo ====================================================
echo   Cross-Application AI Text Rewriter
echo ====================================================
echo.
echo Checking dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -q -r requirements_cross_app.txt

if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install
    echo Attempting to continue anyway...
    echo.
)

echo.
echo ====================================================
echo   Starting Cross-App AI Rewriter...
echo ====================================================
echo.
echo Instructions:
echo   1. Select text in any app (browser, Word, etc.)
echo   2. Press Ctrl + Space
echo   3. AI improves your text automatically!
echo.
echo   Press Ctrl + Esc to exit
echo.
echo ====================================================
echo.

REM Run the cross-app rewriter
python cross_app_ai_rewrite.py

if errorlevel 1 (
    echo.
    echo ====================================================
    echo   ERROR: Program exited with an error
    echo ====================================================
    echo.
    pause
)
