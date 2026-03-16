@echo off
echo Starting Fund Arbitrage System...

echo Starting Backend API...
start "Backend API" cmd /k "cd backend && venv\Scripts\activate && python api.py"

echo Starting Scheduler...
start "Scheduler" cmd /k "cd backend && venv\Scripts\activate && python run_scheduler.py"

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo System started!
echo Frontend will be available at http://localhost:5173 (check console for actual port)
echo Backend is running at http://localhost:5001
pause
