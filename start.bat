@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo === S-Art: Docker startup ===
echo.

where docker >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker is not installed or is unavailable in PATH.
    echo Install and start Docker Desktop, then run start.bat again.
    pause
    exit /b 1
)

docker info >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker Desktop is not running.
    echo Start Docker Desktop, wait until it is ready, then run start.bat again.
    pause
    exit /b 1
)

echo [1/2] Building and starting PostgreSQL, Redis, backend and frontend...
docker compose up -d --build
if errorlevel 1 (
    echo ERROR: Failed to start Docker services.
    pause
    exit /b 1
)

echo [2/2] Checking services...
docker compose ps

echo.
echo ========================================
echo   S-Art is ready
echo   Application: http://localhost:5173/
echo   API:         http://localhost:8000/
echo ========================================
echo.
echo Do not run "npm run dev" at the same time:
echo Vite would move to ports 5174, 5175, and so on.
echo.
pause
endlocal
