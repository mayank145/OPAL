#!/bin/bash

# OPAL Complete Restart Script
# This script kills all processes and starts fresh

echo "======================================"
echo "  OPAL Complete Restart"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Step 1: Kill all processes
echo -e "${BLUE}Step 1: Killing all processes...${NC}"
killall node 2>/dev/null || true
killall python 2>/dev/null || true
killall python3 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 2
echo -e "${GREEN}✅ All processes killed${NC}"
echo ""

# Step 2: Clean caches
echo -e "${BLUE}Step 2: Cleaning caches...${NC}"
cd "$SCRIPT_DIR/frontend"
rm -rf node_modules/.cache build 2>/dev/null || true
cd "$SCRIPT_DIR/backend"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✅ Caches cleaned${NC}"
echo ""

# Step 3: Start backend
echo -e "${BLUE}Step 3: Starting backend...${NC}"
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/opal-backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Wait for backend to initialize
echo -e "${YELLOW}⏳ Waiting for backend to initialize...${NC}"
sleep 5

# Check backend health
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Backend health check failed (might still be starting)${NC}"
fi
echo ""

# Step 4: Start frontend
echo -e "${BLUE}Step 4: Starting frontend...${NC}"
cd "$SCRIPT_DIR/frontend"
BROWSER=none npm start > /tmp/opal-frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

# Wait for frontend to compile
echo -e "${YELLOW}⏳ Waiting for frontend to compile...${NC}"
sleep 10

# Final status
echo "======================================"
echo -e "${GREEN}✅ OPAL Restart Complete!${NC}"
echo "======================================"
echo ""
echo -e "${BLUE}Services:${NC}"
echo "  Backend:   http://localhost:8000"
echo "  Frontend:  http://localhost:3000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo -e "${BLUE}Process IDs:${NC}"
echo "  Backend:   $BACKEND_PID"
echo "  Frontend:  $FRONTEND_PID"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo "  Backend:   tail -f /tmp/opal-backend.log"
echo "  Frontend:  tail -f /tmp/opal-frontend.log"
echo ""
echo -e "${YELLOW}To stop:${NC}"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo "  Or run: killall node python"
echo ""
echo -e "${GREEN}Opening browser in 3 seconds...${NC}"
sleep 3

# Open browser (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:3000
fi

echo ""
echo -e "${GREEN}Ready! Check http://localhost:3000${NC}"
echo ""

