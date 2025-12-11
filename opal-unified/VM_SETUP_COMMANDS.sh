#!/bin/bash
# VM Setup Commands - Run these on your VM
# Copy and paste these commands one by one on your VM

echo "=== FATS System VM Setup ==="
echo ""

# Step 1: Verify Database
echo "Step 1: Verifying database..."
mysql -u opal -p -e "USE opal; SHOW TABLES;"
mysql -u opal -p -e "USE opal; SELECT COUNT(*) as total_faults FROM fault;"
echo ""

# Step 2: Configure Backend
echo "Step 2: Configuring backend..."
cd /opt/OPAL/opal-unified/backend
cp .env.production.example .env
echo "✅ .env file created. Now edit it with: nano .env"
echo "   Update: DATABASE_URL, SECRET_KEY, ALLOWED_ORIGINS"
echo ""

# Step 3: Generate Secret Key
echo "Step 3: Generating secret key..."
source venv/bin/activate
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
echo "Your SECRET_KEY: $SECRET_KEY"
echo "Copy this to .env file"
echo ""

# Step 4: Get VM IP
echo "Step 4: Getting VM IP..."
VM_IP=$(hostname -I | awk '{print $1}')
echo "Your VM IP: $VM_IP"
echo "Use this in ALLOWED_ORIGINS: http://$VM_IP"
echo ""

# Step 5: Create Directories
echo "Step 5: Creating directories..."
mkdir -p uploads/fats logs
chmod 755 uploads uploads/fats logs
echo "✅ Directories created"
echo ""

# Step 6: Test Backend
echo "Step 6: Testing backend..."
source venv/bin/activate
python3 -c "from app.main import app; print('✅ Backend imports OK')" || echo "❌ Backend import failed"
echo ""

echo "=== Next Steps ==="
echo "1. Edit .env file: nano /opt/OPAL/opal-unified/backend/.env"
echo "2. Set up systemd service (see VM_NEXT_STEPS_AFTER_DB.md)"
echo "3. Configure frontend"
echo "4. Configure Apache"



