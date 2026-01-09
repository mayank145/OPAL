#!/bin/bash
# Manual Deployment Test Script
# Run this on your production server to test deployment manually

echo "=== OPAL Deployment Test ==="
echo ""

# Test 1: Find project directory
echo "Test 1: Finding project directory..."
if [ -d "/opt/OPAL/OPAL" ]; then
    PROJECT_DIR="/opt/OPAL/OPAL"
    echo "✅ Found at: /opt/OPAL/OPAL"
elif [ -d "/opt/OPAL/opal-unified" ]; then
    PROJECT_DIR="/opt/OPAL/opal-unified"
    echo "✅ Found at: /opt/OPAL/opal-unified"
elif [ -d "/opt/OPAL" ]; then
    echo "⚠️ Found /opt/OPAL, listing contents:"
    ls -la /opt/OPAL/
    PROJECT_DIR="/opt/OPAL"
else
    echo "❌ /opt/OPAL does not exist"
    echo "Current directory: $(pwd)"
    echo "Listing /opt/:"
    ls -la /opt/ 2>/dev/null || echo "Cannot access /opt/"
    exit 1
fi
echo ""

# Test 2: Check Git
echo "Test 2: Checking Git..."
cd "$PROJECT_DIR" || exit 1
if git status &>/dev/null; then
    echo "✅ Git repository found"
    echo "Current branch: $(git branch --show-current)"
    echo "Latest commit: $(git log -1 --oneline)"
else
    echo "❌ Not a git repository"
    exit 1
fi
echo ""

# Test 3: Check Backend
echo "Test 3: Checking Backend..."
if [ -d "backend" ]; then
    echo "✅ Backend directory exists"
    if [ -f "backend/venv/bin/activate" ]; then
        echo "✅ Virtual environment exists"
    else
        echo "⚠️ No virtual environment found"
    fi
    if [ -f "backend/requirements.txt" ]; then
        echo "✅ requirements.txt exists"
    else
        echo "❌ requirements.txt not found"
    fi
else
    echo "❌ Backend directory not found"
fi
echo ""

# Test 4: Check Frontend
echo "Test 4: Checking Frontend..."
if [ -d "frontend" ]; then
    echo "✅ Frontend directory exists"
    if [ -f "frontend/package.json" ]; then
        echo "✅ package.json exists"
    else
        echo "❌ package.json not found"
    fi
    if command -v npm &> /dev/null; then
        echo "✅ npm is installed: $(npm --version)"
    else
        echo "❌ npm not found"
    fi
else
    echo "❌ Frontend directory not found"
fi
echo ""

# Test 5: Check Services
echo "Test 5: Checking Services..."
if systemctl is-active --quiet opal-backend; then
    echo "✅ opal-backend service is running"
else
    echo "⚠️ opal-backend service not running"
fi

if systemctl is-active --quiet httpd; then
    echo "✅ httpd service is running"
elif systemctl is-active --quiet apache2; then
    echo "✅ apache2 service is running"
else
    echo "⚠️ Web server not running"
fi
echo ""

# Test 6: Check ports
echo "Test 6: Checking Ports..."
if curl -f http://localhost:8000/health &>/dev/null; then
    echo "✅ Backend responding on port 8000"
else
    echo "⚠️ Backend not responding on port 8000"
fi

if curl -f http://localhost/ &>/dev/null; then
    echo "✅ Frontend responding on port 80"
else
    echo "⚠️ Frontend not responding on port 80"
fi
echo ""

echo "=== Test Complete ==="
echo ""
echo "Summary:"
echo "Project Directory: $PROJECT_DIR"
echo ""
echo "Next steps:"
echo "1. If all tests pass, deployment should work"
echo "2. If any test fails, fix that issue first"
echo "3. Share the output with your developer"


