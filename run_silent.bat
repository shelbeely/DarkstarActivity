@echo off
SETLOCAL

REM ================================
REM Darkstar Activity Monitor (Silent)
REM ================================

SET VENV_DIR=%~dp0venv
call "%VENV_DIR%\Scripts\activate.bat"

REM Run both scripts silently with pythonw.exe
start "" "%VENV_DIR%\Scripts\pythonw.exe" "%~dp0KMActivity.py"
start "" "%VENV_DIR%\Scripts\pythonw.exe" "%~dp0extract_activity.py"

ENDLOCAL
