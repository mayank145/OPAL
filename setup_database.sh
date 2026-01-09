#!/bin/bash
# OPAL Database Setup Script
# This script sets up the database and user for the OPAL application

set -e

echo "🗄️  Setting up OPAL Database..."
echo ""

# Run the SQL setup script
echo "Creating database and user..."
sudo mysql -u root < setup_database.sql

echo ""
echo "✅ Database setup complete!"
echo ""

# Test connection
echo "🧪 Testing database connection..."
if mysql -u opal -popal_password -h localhost -e "SELECT 'Connection successful!' as status;" opal 2>/dev/null; then
    echo "✅ Database connection test successful!"
else
    echo "❌ Database connection test failed!"
    echo "Please check your MySQL/MariaDB configuration."
    exit 1
fi

echo ""
echo "📊 Checking for existing tables..."
TABLE_COUNT=$(mysql -u opal -popal_password -h localhost -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'opal';" -s -N)

if [ "$TABLE_COUNT" -eq "0" ]; then
    echo "⚠️  No tables found in the database."
    echo ""
    if [ -f "opal_database_backup.sql" ]; then
        echo "📥 Found backup file. Importing database schema and data..."
        mysql -u opal -popal_password opal < opal_database_backup.sql
        echo "✅ Database imported successfully!"
    else
        echo "ℹ️  No backup file found (opal_database_backup.sql)."
        echo "   The application will create tables automatically on first run."
    fi
else
    echo "✅ Found $TABLE_COUNT tables in the database."
fi

echo ""
echo "🎉 Setup complete! Your application should now be able to connect to the database."
echo ""
echo "📝 Database credentials:"
echo "   Host: localhost"
echo "   Port: 3306"
echo "   Database: opal"
echo "   User: opal"
echo "   Password: opal_password"
echo ""
echo "🚀 You can now restart your backend server."

