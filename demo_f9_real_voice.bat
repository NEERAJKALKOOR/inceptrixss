@echo off
REM F9 Real Voice Demo - Complete workflow test
echo ====================================
echo F9 VOICE DEMO - REAL WHISPER
echo ====================================
echo.

REM Check dependencies
echo Checking setup...
python check_voice_setup.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Please run setup_f9_voice.bat first!
    pause
    exit /b 1
)

echo.
echo ====================================
echo Starting demo...
echo ====================================
echo.

python demo_f9_real_voice.py
