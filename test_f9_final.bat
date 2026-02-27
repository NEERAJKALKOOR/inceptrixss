@echo off
echo ====================================
echo F9 VOICE - FINAL TEST
echo ====================================
echo.
echo Status check...
python check_voice_status.py
echo.
echo ====================================
echo.
echo Starting AI Keyboard...
echo.
echo WORKFLOW TO TEST:
echo 1. Open Notepad (will auto-launch)
echo 2. Type: "test text"
echo 3. SELECT the text
echo 4. Press F9 - start recording
echo 5. SPEAK: "hello world"
echo 6. Press F9 - transcribe and replace
echo.
echo Press any key to start...
pause >nul

REM Launch Notepad
start notepad.exe
timeout /t 2 >nul

echo.
echo Starting AI Keyboard...
python unified_ai_keyboard.py
