#!/bin/bash
set -e
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== S-Art ==="
echo ""

echo "[1/4] Installing backend dependencies..."
cd "$SCRIPT_DIR/backend"
python -m pip install -r requirements.txt

echo "[2/4] Installing frontend dependencies..."
cd "$SCRIPT_DIR/frontend"
npm install

cd "$SCRIPT_DIR"

echo "[3/4] Starting backend on http://localhost:8000 ..."
cd "$SCRIPT_DIR/backend"
python main.py &
BACKEND_PID=$!

echo "[4/4] Starting frontend on http://localhost:5173 ..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

cd "$SCRIPT_DIR"

echo ""
echo "========================================"
echo "  Both servers are running!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
