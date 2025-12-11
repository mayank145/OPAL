#!/bin/bash

# OPAL Local Database Setup Script
# This script sets up a local MySQL database for development

echo "======================================"
echo "  OPAL Local Database Setup"
echo "======================================"
echo ""

# Check MySQL is running
if ! lsof -ti:3306 > /dev/null 2>&1; then
    echo "❌ MySQL is not running!"
    echo "Start MySQL first:"
    echo "  brew services start mysql"
    exit 1
fi

echo "✅ MySQL is running"
echo ""

# Create database and user
echo "Creating database and user..."
echo "Enter your MySQL root password when prompted:"
mysql -u root -p << 'EOF'
CREATE DATABASE IF NOT EXISTS opal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'opal'@'localhost' IDENTIFIED BY 'opal';
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';
FLUSH PRIVILEGES;
SELECT 'Database and user created!' as Status;
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database setup complete"
else
    echo "❌ Database setup failed"
    exit 1
fi

echo ""
echo "======================================"
echo "Importing data from VM..."
echo "======================================"
echo ""

# Import data from VM
ssh root@opalfailover "mysqldump -u opal -popal opal --single-transaction --quick" > /tmp/opal_backup.sql

if [ $? -eq 0 ]; then
    echo "✅ Data exported from VM"
    
    # Import to local database
    mysql -u opal -popal opal < /tmp/opal_backup.sql
    
    if [ $? -eq 0 ]; then
        echo "✅ Data imported to local database"
        rm /tmp/opal_backup.sql
    else
        echo "❌ Failed to import data"
        exit 1
    fi
else
    echo "❌ Failed to export data from VM"
    exit 1
fi

echo ""
echo "======================================"
echo "Verifying database..."
echo "======================================"
echo ""

# Verify
mysql -u opal -popal -e "USE opal; SELECT COUNT(*) as total_faults FROM fault; SHOW TABLES;"

echo ""
echo "======================================"
echo "✅ LOCAL DATABASE READY!"
echo "======================================"
echo ""
echo "Database: opal"
echo "Username: opal"
echo "Password: opal"
echo "Host: localhost"
echo ""
echo "Next step: Update backend .env file"
echo ""

