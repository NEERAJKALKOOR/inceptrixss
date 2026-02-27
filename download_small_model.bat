@echo off
echo ====================================
echo Download Whisper SMALL Model
echo ====================================
echo.
echo This will download the SMALL model (~470MB)
echo - Better accuracy than base
echo - Still fast transcription
echo.
echo Requires internet connection
echo.
pause

python download_small_model.py

echo.
pause
