@echo off
where python >nul 2>nul

if %ERRORLEVEL% neq 0 (
    echo Python is not installed!
    echo Opening the official Python download page...
    start https://www.python.org/downloads/
    pause
    exit /b
)

echo Python is installed.
echo Installing required packages...
python -m pip install --upgrade pip
pip install deep-translator pyperclip
echo Installation completed.
pause
