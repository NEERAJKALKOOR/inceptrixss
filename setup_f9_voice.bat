@echo off
echo ====================================
echo F9 VOICE - QUICK SETUP
echo ====================================
echo.
echo This will install all dependencies for real voice transcription
echo.
pause

echo.
echo 1/3 Installing Python packages...
pip install -r requirements_ui.txt

echo.
echo 2/3 Checking ffmpeg...
where ffmpeg >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ ffmpeg is already installed!
) else (
    echo.
    echo ⚠️  ffmpeg not found on system PATH
    echo.
    echo Please install ffmpeg manually:
    echo   - Windows: choco install ffmpeg
    echo   - Or download from: https://ffmpeg.org/download.html
    echo.
    echo After installing, restart this script.
    pause
    exit /b 1
)

echo.
echo 3/3 Verifying setup...
python check_voice_setup.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo ✅ SETUP COMPLETE!
    echo ====================================
    echo.
    echo You can now run:
    echo   python unified_ai_keyboard.py
    echo.
    echo Or test with:
    echo   test_f9_voice.bat
    echo.
) else (
    echo.
    echo ====================================
    echo ⚠️  Setup incomplete - see errors above
    echo ====================================
)

pause
