@echo off
REM Quick start for VS Code-style Ghost Suggestion Test
echo ================================================
echo VS CODE-STYLE GHOST SUGGESTION TEST
echo ================================================
echo.
echo This will launch an interactive demo window to test
echo the VS Code-style inline ghost suggestions.
echo.
echo Features demonstrated:
echo   - Inline rendering at caret position
echo   - Light gray, italic text (VS Code style)
echo   - Auto-dismiss on typing and cursor movement
echo   - Tab to accept, Esc to reject
echo   - Always-on-top, click-through overlay
echo.
echo ================================================
echo.

python test_vscode_ghost.py

pause
