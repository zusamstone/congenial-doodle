@echo off
title AI Studio - Update
color 0E
echo ============================================================
echo                    AI Studio - Update
echo ============================================================
echo.

:: Store current directory
set "ROOT_DIR=%~dp0"

:: Check Python version
echo [1/5] Checking Python version...
python --version
echo       Python check complete.
echo.

:: Check Node.js version
echo [2/5] Checking Node.js version...
node --version
echo       Node.js check complete.
echo.

:: Update Python dependencies
echo [3/5] Updating Python dependencies...
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo [ERROR] Failed to update Python dependencies.
    cd "%ROOT_DIR%"
    pause
    exit /b 1
)
echo       Python dependencies updated.
cd "%ROOT_DIR%"
echo.

:: Install/verify Node.js dependencies (root workspace)
echo [4/5] Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to update root Node.js dependencies.
    pause
    exit /b 1
)

:: Update frontend dependencies
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to update frontend dependencies.
    cd "%ROOT_DIR%"
    pause
    exit /b 1
)
cd "%ROOT_DIR%"

:: Update electron dependencies
cd electron
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to update Electron dependencies.
    cd "%ROOT_DIR%"
    pause
    exit /b 1
)
cd "%ROOT_DIR%"
echo       Node.js dependencies updated.
echo.

:: Version check / pull latest (optional - requires git)
echo [5/5] Checking for updates...
git --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Git not found. Skipping version check.
) else (
    echo Current branch:
    git branch --show-current
    echo.
    echo Fetching latest changes...
    git fetch origin
    echo.
    echo Status:
    git status -s
)
echo.

echo ============================================================
echo                    Update Complete!
echo ============================================================
echo.
echo You can now run start.bat to launch the application.
echo.
pause
