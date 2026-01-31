#!/bin/bash

echo "🛑 Stopping..."

lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
docker-compose down

echo "✅ Stopped!"