# Database Migration Guide: Local to VM

This guide shows you how to export your local database and import it to the VM.

## Prerequisites

- Local database running (MariaDB/MySQL)
- Database credentials (username, password, database name)
- SSH access to VM
- `mysqldump` installed locally
- `mysql` client installed on VM

## Step 1: Export Database from Local Machine

### 1.1 Identify Your Local Database Details

On your local machine, check your database configuration:
```bash
# Check your local .env file
cat opal-unified/backend/.env | grep DATABASE_URL

# Or check directly in MySQL
mysql -u opal -p -e "SELECT DATABASE();"
```

You should see something like:
- Database name: `opal`
- Username: `opal`
- Host: `localhost`
- Port: `3306`

### 1.2 Export Database (Full Dump)

```bash
# On your LOCAL machine
cd ~/Desktop/Subaru_Telescope/OPAL

# Export entire database
mysqldump -u opal -p opal > opal_database_backup.sql

# You'll be prompted for the database password
```

### 1.3 Export Only Data (if schema already exists on VM)

If you only need the data (not the schema):
```bash
# Export data only (no CREATE TABLE statements)
mysqldump -u opal -p --no-create-info opal > opal_data_only.sql

# Or export specific tables
mysqldump -u opal -p opal fault fcomments fsection fstaff > opal_tables.sql
```

### 1.4 Export with Compression (for large databases)

```bash
# Compress during export (saves space)
mysqldump -u opal -p opal | gzip > opal_database_backup.sql.gz
```

### 1.5 Verify Export

```bash
# Check file was created
ls -lh opal_database_backup.sql

# Check file size (should not be empty)
wc -l opal_database_backup.sql

# Preview first few lines
head -20 opal_database_backup.sql
```

## Step 2: Transfer Database File to VM

### Option A: Using SCP (Recommended)

```bash
# From your LOCAL machine
# Replace VM_IP with your actual VM IP address
scp opal_database_backup.sql root@VM_IP:/tmp/

# If using compression:
scp opal_database_backup.sql.gz root@VM_IP:/tmp/
```

### Option B: Using rsync

```bash
# From your LOCAL machine
rsync -avz opal_database_backup.sql root@VM_IP:/tmp/
```

### Option C: Using SFTP

```bash
# From your LOCAL machine
sftp root@VM_IP
put opal_database_backup.sql /tmp/
exit
```

### Option D: Manual Upload (if SCP not available)

1. Copy file to a location accessible via web browser
2. Use `wget` or `curl` on VM to download
3. Or use a file sharing service

## Step 3: Prepare VM Database

### 3.1 SSH into VM

```bash
ssh root@VM_IP
```

### 3.2 Create Database and User (if not already done)

```bash
# Login to MariaDB
sudo mysql -u root -p

# In MySQL prompt:
CREATE DATABASE IF NOT EXISTS opal;
CREATE USER IF NOT EXISTS 'opal'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3.3 Verify Database is Empty (or backup existing)

```bash
# Check current tables
mysql -u opal -p -e "USE opal; SHOW TABLES;"

# If you have existing data, backup it first:
mysqldump -u opal -p opal > /tmp/opal_backup_before_import_$(date +%Y%m%d).sql
```

## Step 4: Import Database to VM

### 4.1 Navigate to Backup Location

```bash
# On VM
cd /tmp
ls -lh opal_database_backup.sql
```

### 4.2 Import Database

```bash
# Import full database (schema + data)
mysql -u opal -p opal < opal_database_backup.sql

# If compressed:
gunzip < opal_database_backup.sql.gz | mysql -u opal -p opal
```

### 4.3 Verify Import

```bash
# Check tables were created
mysql -u opal -p -e "USE opal; SHOW TABLES;"

# Check record counts
mysql -u opal -p -e "USE opal; SELECT COUNT(*) as total_faults FROM fault;"
mysql -u opal -p -e "USE opal; SELECT COUNT(*) as total_comments FROM fcomments;"

# Check a few sample records
mysql -u opal -p -e "USE opal; SELECT idno, issue, status FROM fault LIMIT 5;"
```

## Step 5: Verify Data Integrity

### 5.1 Compare Record Counts

**On Local Machine:**
```bash
mysql -u opal -p -e "USE opal; SELECT 
    (SELECT COUNT(*) FROM fault) as faults,
    (SELECT COUNT(*) FROM fcomments) as comments,
    (SELECT COUNT(*) FROM fsection) as sections,
    (SELECT COUNT(*) FROM fstaff) as staff;"
```

**On VM:**
```bash
mysql -u opal -p -e "USE opal; SELECT 
    (SELECT COUNT(*) FROM fault) as faults,
    (SELECT COUNT(*) FROM fcomments) as comments,
    (SELECT COUNT(*) FROM fsection) as sections,
    (SELECT COUNT(*) FROM fstaff) as staff;"
```

The counts should match!

### 5.2 Test Backend Connection

```bash
# On VM
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate

# Test database connection
python3 -c "
from app.db.session import engine
import asyncio
async def test():
    async with engine.connect() as conn:
        result = await conn.execute('SELECT COUNT(*) as count FROM fault')
        row = result.fetchone()
        print(f'✅ Database connected! Found {row[0]} fault records')
asyncio.run(test())
"
```

## Step 6: Clean Up

### 6.1 Remove Backup File from VM (after verification)

```bash
# On VM
rm /tmp/opal_database_backup.sql

# Or keep it for safety:
mv /tmp/opal_database_backup.sql /opt/OPAL/backups/
```

### 6.2 Keep Local Backup (recommended)

```bash
# On LOCAL machine
mkdir -p ~/backups
mv opal_database_backup.sql ~/backups/opal_backup_$(date +%Y%m%d).sql
```

## Troubleshooting

### Error: "Access denied for user"

**Solution:**
```bash
# Check user exists and has permissions
mysql -u root -p -e "SELECT User, Host FROM mysql.user WHERE User='opal';"
mysql -u root -p -e "SHOW GRANTS FOR 'opal'@'localhost';"

# If user doesn't exist, create it:
mysql -u root -p -e "CREATE USER 'opal'@'localhost' IDENTIFIED BY 'password';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"
```

### Error: "Unknown database 'opal'"

**Solution:**
```bash
# Create database first
mysql -u root -p -e "CREATE DATABASE opal;"
```

### Error: "Table already exists"

**Solution:**
```bash
# Option 1: Drop and recreate (WARNING: Deletes existing data)
mysql -u opal -p -e "USE opal; DROP TABLE IF EXISTS fault, fcomments, fsection, fstaff;"
mysql -u opal -p opal < opal_database_backup.sql

# Option 2: Import only data (if schema exists)
mysql -u opal -p opal < opal_data_only.sql
```

### Import is Very Slow

**Solution:**
```bash
# Disable foreign key checks during import
mysql -u opal -p opal << EOF
SET FOREIGN_KEY_CHECKS=0;
SOURCE /tmp/opal_database_backup.sql;
SET FOREIGN_KEY_CHECKS=1;
EOF

# Or use command line:
mysql -u opal -p opal -e "SET FOREIGN_KEY_CHECKS=0;" && \
mysql -u opal -p opal < opal_database_backup.sql && \
mysql -u opal -p opal -e "SET FOREIGN_KEY_CHECKS=1;"
```

### File Too Large for SCP

**Solution:**
```bash
# Compress before transfer
gzip opal_database_backup.sql
scp opal_database_backup.sql.gz root@VM_IP:/tmp/

# On VM, decompress and import
gunzip /tmp/opal_database_backup.sql.gz
mysql -u opal -p opal < /tmp/opal_database_backup.sql
```

## Quick Reference Commands

### Complete Migration (One-liner)

**On Local Machine:**
```bash
mysqldump -u opal -p opal | gzip | ssh root@VM_IP "gunzip | mysql -u opal -p opal"
```

This exports, compresses, transfers, and imports in one command!

### Export Specific Tables Only

```bash
# Export only main tables
mysqldump -u opal -p opal fault fcomments fsection fstaff > opal_main_tables.sql
```

### Export with Timestamp

```bash
# Include timestamp in filename
mysqldump -u opal -p opal > opal_backup_$(date +%Y%m%d_%H%M%S).sql
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit database dumps to Git** - They contain sensitive data
2. **Use secure transfer** - Always use SCP/SFTP, never email
3. **Delete backups after import** - Or store securely
4. **Use strong passwords** - For both local and VM databases
5. **Limit access** - Only grant necessary permissions

## Next Steps After Database Migration

1. ✅ Verify all data imported correctly
2. ✅ Test backend connection
3. ✅ Update backend `.env` with VM database credentials
4. ✅ Test API endpoints
5. ✅ Verify images are accessible (if copied separately)

---

**Need Help?** If you encounter issues, check:
- Database user permissions
- Database exists on VM
- File transfer completed successfully
- Import command syntax



