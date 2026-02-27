@echo off
REM Install context detection dependencies and start AI keyboard
echo.
echo ========================================
echo Installing Context Features...
echo ========================================
echo.

REM Install dependencies
pip install pywin32 psutil

echo.
echo ========================================
echo Testing Context Detection...
echo ========================================
echo.

python test_context_features.py

echo.
echo ========================================
echo Starting AI Keyboard with New Features
echo ========================================
echo.

python unified_ai_keyboard.py

pause
