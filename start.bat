@echo off
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
echo === S-Art ===
echo.

echo [1/4] Installing backend dependencies...
cd /d "%~dp0backend"
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
cd /d "%~dp0"

echo [2/4] Installing frontend dependencies...
cd /d "%~dp0frontend"
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
cd /d "%~dp0"

echo [3/4] Starting backend on http://localhost:8000 ...
start "S-Art Backend" cmd /k "chcp 65001 >nul && cd /d "%~dp0backend" && set PYTHONUTF8=1 && set PYTHONIOENCODING=utf-8 && python main.py"

echo [4/4] Starting frontend on http://localhost:5173 ...
start "S-Art Frontend" cmd /k "chcp 65001 >nul && cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo   Both servers are starting!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
pause
