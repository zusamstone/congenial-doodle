@echo off
title AI Studio - First Install
color 0B
echo ============================================================
echo                 AI Studio - First Install
echo ============================================================
echo.
echo This script will set up all dependencies for AI Studio.
echo.

:: Store current directory
set "ROOT_DIR=%~dp0"

:: Check prerequisites
echo [1/6] Checking prerequisites...
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.11+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
echo       [OK] Python found:
python --version
echo.

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed.
    echo Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)
echo       [OK] Node.js found:
node --version
echo.

:: Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed.
    pause
    exit /b 1
)
echo       [OK] npm found:
npm --version
echo.

:: Upgrade pip
echo [2/6] Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install Python dependencies
echo [3/6] Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies.
    cd "%ROOT_DIR%"
    pause
    exit /b 1
)
echo       Python dependencies installed.
cd "%ROOT_DIR%"
echo.

:: Create .env file if it doesn't exist
echo [4/6] Setting up environment configuration...
cd backend
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo       Created .env file from template.
        echo       [IMPORTANT] Please edit backend\.env to configure your settings.
    ) else (
        echo       [WARNING] No .env.example found. The application will use default settings. You can create a backend\.env file later to customize configuration.
    )
) else (
    echo       .env file already exists.
)
cd "%ROOT_DIR%"
echo.

:: Install root Node.js dependencies
echo [5/6] Installing Node.js dependencies (this may take a while)...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install root dependencies.
    pause
    exit /b 1
)
echo.

:: Install workspace dependencies
echo [6/6] Installing workspace dependencies...

cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies.
    cd "%ROOT_DIR%"
    pause
    exit /b 1
)
cd "%ROOT_DIR%"

cd electron
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install Electron dependencies.
    cd "%ROOT_DIR%"
    pause
    exit /b 1
)
cd "%ROOT_DIR%"
echo       All Node.js dependencies installed.
echo.

echo ============================================================
echo              First Install Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Configure backend\.env with your API keys (if needed)
echo   2. Run start.bat to launch the application
echo.
echo For development, you can also use:
echo   - npm run dev          (runs all services concurrently)
echo   - npm run dev:frontend (frontend only)
echo   - npm run dev:backend  (backend only)
echo   - npm run dev:electron (electron only)
echo.
pause
