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

echo [1/2] Starting PostgreSQL, Redis, backend and frontend from local images...
docker compose up -d --no-build
if errorlevel 1 (
    echo.
    echo ERROR: Local S-Art images are missing or damaged.
    echo The application cannot be built while Docker Hub DNS is unavailable.
    echo When Internet access is restored, run:
    echo   docker compose up -d --build
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
start "" "http://localhost:5173/?build=classic-stable"
pause
endlocal
