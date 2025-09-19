@echo off
SETLOCAL

REM ================================
REM Darkstar Environment Installer
REM ================================

SET INSTALL_DIR=%~dp0venv
SET API_KEY_FILE=%~dp0api_key.txt

echo 🔄 Creating virtual environment in %INSTALL_DIR%...
python -m venv "%INSTALL_DIR%"

call "%INSTALL_DIR%\Scripts\activate.bat"

python -m pip install --upgrade pip

echo 📦 Installing dependencies...
pip install requests mysql-connector-python pynput

echo.
echo =========================================
echo 🔑 Enter your Darkstar API key below:
echo =========================================
set /p APIKEY=API Key: 

REM Save API key to file
echo %APIKEY%> "%API_KEY_FILE%"
echo ✅ API key saved to %API_KEY_FILE%

echo.
echo ✅ Environment setup complete.
echo To start monitoring, run:
echo    run.bat   (visible mode)
echo    run_silent.bat   (background mode)

ENDLOCAL
pause
