#!/bin/bash

set -e

echo "🚀 Setting up Kiros Triage..."

# ===== Docker =====
echo "🐳 Starting Docker services..."
docker-compose up -d
sleep 5  # Chờ PostgreSQL ready

# ===== Backend =====
echo "📦 Setting up Backend..."
cd backend

[ ! -f .env ] && cp .env.example .env && echo "✓ Created backend/.env"
source .venv/bin/activate
poetry install
poetry run python cli.py dbcreate local
poetry run python cli.py dbmigrate local
cd ..

# ===== Frontend =====
echo "📦 Setting up Frontend..."
cd frontend

[ ! -f .env.local ] && cp .env.example .env.local && echo "✓ Created frontend/.env.local"

npm install

cd ..

echo "✅ Setup complete!"
