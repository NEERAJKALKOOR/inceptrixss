@echo off
echo ====================================
echo F9 Voice Selection Test
echo ====================================
echo.
echo This will test the new F9 workflow:
echo 1. Select text
echo 2. Press F9 to record
echo 3. Press F9 again to transcribe and replace
echo.
echo Press any key to start...
pause >nul

python test_f9_voice.py
