@echo off
echo ====================================
echo F9 Voice Selection Test (REAL WHISPER)
echo ====================================
echo.
echo Checking dependencies first...
echo.

python check_voice_setup.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ====================================
    echo Please install missing dependencies!
    echo ====================================
    pause
    exit /b 1
)

echo.
echo ====================================
echo All dependencies OK!
echo ====================================
echo.
echo This will test the new F9 workflow:
echo 1. Select text
echo 2. Press F9 to start recording
echo 3. SPEAK into your microphone
echo 4. Press F9 again to transcribe and replace
echo.
echo Press any key to start...
pause >nul

python test_f9_voice.py
