@echo off
echo ====================================
echo Download Whisper MEDIUM Model
echo ====================================
echo.
echo This will download the MEDIUM model (~1.5GB)
echo - HIGH accuracy
echo - Best for production use
echo - Downloads once, works offline forever
echo.
echo ⚠️  Requires: Internet connection and 1.5GB free space
echo ⏳ Download time: 5-15 minutes (depending on internet)
echo.
echo Press any key to start download...
pause >nul

python download_medium_model.py

echo.
echo ====================================
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Model downloaded! 
    echo.
    echo Now run: python unified_ai_keyboard.py
    echo.
) else (
    echo ⚠️  Download failed or cancelled
)
pause
