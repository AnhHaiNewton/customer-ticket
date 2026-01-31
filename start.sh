#!/bin/bash

echo "🚀 Starting Kiros Triage..."

# Start Docker
docker-compose up -d
sleep 3

# Start all services in background
cd backend
source .venv/bin/activate
python cli.py server local &
python cli.py worker local &
cd ..

cd frontend
npm run dev &
cd ..

echo ""
echo "✅ Running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"

wait