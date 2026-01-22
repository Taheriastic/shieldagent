#!/bin/bash

# ShieldAgent Startup Script
# Run this script to start both backend and frontend servers

echo "🛡️  Starting ShieldAgent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Kill any existing processes on the ports
echo -e "${YELLOW}Clearing ports 8000 and 5173...${NC}"
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null
sleep 1

# Check Docker containers
echo -e "${YELLOW}Checking Docker containers...${NC}"
if ! docker ps | grep -q "shieldagent-db"; then
    echo -e "${RED}PostgreSQL container not running! Starting...${NC}"
    docker start shieldagent-db 2>/dev/null || echo "Container doesn't exist"
fi

if ! docker ps | grep -q "shieldagent-redis"; then
    echo -e "${RED}Redis container not running! Starting...${NC}"
    docker start shieldagent-redis 2>/dev/null || echo "Container doesn't exist"
fi

# Start Backend
echo -e "${YELLOW}Starting Backend on port 8000...${NC}"
cd "$SCRIPT_DIR/backend"
nohup "$SCRIPT_DIR/backend/venv/bin/python" -m uvicorn main:app --reload --port 8000 > /tmp/shieldagent-backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}✗ Backend failed to start. Check /tmp/shieldagent-backend.log${NC}"
fi

# Start Frontend
echo -e "${YELLOW}Starting Frontend on port 5173...${NC}"
cd "$SCRIPT_DIR/frontend"

# Load NVM and start frontend
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

nohup npm run dev > /tmp/shieldagent-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 3

# Check if frontend is running
if lsof -i:5173 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend failed to start. Check /tmp/shieldagent-frontend.log${NC}"
fi

echo ""
echo -e "${GREEN}🚀 ShieldAgent is ready!${NC}"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  /tmp/shieldagent-backend.log"
echo "  Frontend: /tmp/shieldagent-frontend.log"
echo ""
echo "To stop: ./stop.sh"
