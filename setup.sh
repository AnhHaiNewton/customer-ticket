#!/bin/bash

set -e

echo "🚀 Setting up Kiros Triage..."

# ===== Backend =====
echo "📦 Setting up Backend..."
cd backend

[ ! -f .env ] && cp .env.example .env && echo "✓ Created backend/.env"

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

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next: Edit backend/.env → Add GEMINI_API_KEY"
echo "Then: ./start.sh"