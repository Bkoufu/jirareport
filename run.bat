@echo off
setlocal

:: Detect the current working directory and set it as the root directory
set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

:: Activate the virtual environment
call .\myenv\Scripts\activate

:: Start the app
start powershell.exe -NoExit -Command "python app.py"

endlocal
