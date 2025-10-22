#!/bin/bash
# Scare Box Launcher

set -e

# Colors for output
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${ORANGE}"
echo "🎃 ============================================ 🎃"
echo "    SCARE BOX - Halloween Control System"
echo "🎃 ============================================ 🎃"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}Error: Must run from scare-box directory${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo -e "${ORANGE}Creating Python virtual environment...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    cd ..
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${ORANGE}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
fi

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${ORANGE}Shutting down Scare Box...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}Goodbye! 👻${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${ORANGE}Starting backend server...${NC}"
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/scarebox-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo -e "${ORANGE}Waiting for backend to initialize...${NC}"
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Backend failed to start. Check /tmp/scarebox-backend.log${NC}"
    cat /tmp/scarebox-backend.log
    exit 1
fi

echo -e "${GREEN}✓ Backend running (PID: $BACKEND_PID)${NC}"

# Start frontend
echo -e "${ORANGE}Starting frontend...${NC}"
cd frontend
npm run dev > /tmp/scarebox-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Frontend failed to start. Check /tmp/scarebox-frontend.log${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo -e "${GREEN}✓ Frontend running (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}🎃 Scare Box is ready! 🎃${NC}"
echo ""
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "  Logs:"
echo "    Backend:  /tmp/scarebox-backend.log"
echo "    Frontend: /tmp/scarebox-frontend.log"
echo ""
echo -e "${ORANGE}Press Ctrl+C to stop${NC}"
echo ""

# Keep script running and show backend logs
tail -f /tmp/scarebox-backend.log
