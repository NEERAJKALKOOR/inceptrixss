@echo off
REM Start AI Keyboard with Real F9 Voice (Whisper)
echo ====================================
echo AI Keyboard - F9 Voice (Real Whisper)
echo ====================================
echo.

REM Quick dependency check
python -c "import whisper; import pyaudio; import PyQt5" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Missing dependencies detected!
    echo.
    echo Please run: setup_f9_voice.bat
    echo Or manually: pip install -r requirements_ui.txt
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies OK
echo.
echo Starting AI Keyboard...
echo - Press F9 to record and replace selected text
echo - Press Ctrl+Esc to exit
echo.

python unified_ai_keyboard.py
