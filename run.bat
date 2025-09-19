@echo off
SETLOCAL

REM ================================
REM Darkstar Activity Monitor Runner
REM ================================

SET VENV_DIR=%~dp0venv
call "%VENV_DIR%\Scripts\activate.bat"

REM Start KMActivity in its own window
start "KMActivity" cmd /k python "%~dp0KMActivity.py"

REM Start extract_activity in its own window
start "ExtractActivity" cmd /k python "%~dp0extract_activity_v3.py"

echo ✅ Darkstar Activity Monitor started.
echo Close this window to terminate all processes.
pause
ENDLOCAL
