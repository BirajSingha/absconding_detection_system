@echo off
echo Starting n8n service...
docker-compose up -d

echo Starting Backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && python run.py"

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo All services started.
