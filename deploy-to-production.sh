#!/bin/bash

# OPAL Production Deployment Script
# This script deploys the latest changes to the production server

set -e  # Exit on any error

echo "════════════════════════════════════════════════════════"
echo "  🚀 OPAL Production Deployment"
echo "════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SERVER="root@opalfailover.subaru.nao.ac.jp"
PROJECT_DIR="/opt/OPAL/OPAL"

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo "   Server: $SERVER"
echo "   Directory: $PROJECT_DIR"
echo ""

# Check if we can reach the server
echo -e "${BLUE}🔍 Step 1: Checking server connectivity...${NC}"
if ssh -o ConnectTimeout=10 "$SERVER" "echo 'Connection successful'" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Server is reachable${NC}"
else
    echo -e "${RED}❌ Cannot connect to server${NC}"
    echo "   Please check your SSH connection and try again."
    exit 1
fi
echo ""

# Deploy
echo -e "${BLUE}🚀 Step 2: Deploying to production...${NC}"
ssh "$SERVER" << 'ENDSSH'
set -e

echo "📂 Navigating to project directory..."
cd /opt/OPAL/OPAL || cd /opt/OPAL/opal-unified || { echo "❌ Project directory not found"; exit 1; }

echo "📥 Pulling latest changes from GitHub..."
git fetch origin
CURRENT_COMMIT=$(git rev-parse HEAD)
git pull origin main

NEW_COMMIT=$(git rev-parse HEAD)
if [ "$CURRENT_COMMIT" = "$NEW_COMMIT" ]; then
    echo "ℹ️  Already up to date (no new commits)"
else
    echo "✅ Pulled new commits: $CURRENT_COMMIT → $NEW_COMMIT"
fi

echo ""
echo "🔧 Updating backend..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "📦 Installing Python dependencies..."
    pip install -q -r requirements.txt
    echo "✅ Backend dependencies updated"
else
    echo "⚠️  Backend venv not found, skipping"
fi
cd ..

echo ""
echo "🎨 Building frontend..."
cd frontend
echo "📦 Installing Node dependencies..."
npm install --silent
echo "🏗️  Building production bundle..."
npm run build
echo "✅ Frontend built successfully"
cd ..

echo ""
echo "🔄 Restarting services..."

# Restart backend
if systemctl is-active --quiet opal-backend; then
    systemctl restart opal-backend
    echo "✅ Restarted opal-backend"
    sleep 2
else
    echo "⚠️  opal-backend not running, attempting to start..."
    systemctl start opal-backend || echo "❌ Could not start opal-backend"
fi

# Restart web server
if systemctl is-active --quiet httpd; then
    systemctl restart httpd
    echo "✅ Restarted httpd (Apache)"
elif systemctl is-active --quiet apache2; then
    systemctl restart apache2
    echo "✅ Restarted apache2"
else
    echo "⚠️  Web server not found"
fi

echo ""
echo "🔍 Verifying deployment..."
sleep 5

# Check backend health
if curl -f -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is responding"
else
    echo "❌ Backend health check failed"
fi

# Check frontend
if curl -f -s http://localhost/ > /dev/null; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend not accessible"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ Deployment Complete!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🌐 Access the application at:"
echo "   http://opalfailover.subaru.nao.ac.jp"
echo ""
echo "📦 New Features Deployed:"
echo "   • 🏷️  Internal fault links with hashtag button"
echo "   • 🔗 Copy Link button for easy sharing"
echo "   • 🌐 URL hash navigation for shared links"
echo "   • 🎨 RED styling for internal fault links"
echo ""
ENDSSH

# Deployment complete
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}🧪 Next Steps:${NC}"
echo "1. Open http://opalfailover.subaru.nao.ac.jp in your browser"
echo "2. Test the internal fault links feature:"
echo "   • Edit a fault"
echo "   • Click the 🏷️ button"
echo "   • Add a link to another fault"
echo "   • Save and click the link"
echo "   • It should open the linked fault (not home page!)"
echo "3. Test the Copy Link button:"
echo "   • Open any fault"
echo "   • Click 'Copy Link'"
echo "   • Share the link with a colleague"
echo ""


