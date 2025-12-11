# Quick Database Export Guide

## Current Situation
- Database `opal` exists ✅
- Can access as root ✅
- `opal` user has access denied ❌

## Solution: Export Using Root

### Step 1: Export Database

```bash
# On your LOCAL machine
cd ~/Desktop/Subaru_Telescope/OPAL

# Export using root (you'll be prompted for root password)
mysqldump -u root -p opal > opal_database_backup.sql
```

### Step 2: Verify Export

```bash
# Check file was created
ls -lh opal_database_backup.sql

# Check it's not empty
wc -l opal_database_backup.sql

# Preview first few lines
head -20 opal_database_backup.sql
```

### Step 3: Transfer to VM

```bash
# Replace VM_IP with your actual VM IP
scp opal_database_backup.sql root@VM_IP:/tmp/
```

### Step 4: Import on VM

```bash
# SSH into VM
ssh root@VM_IP

# On VM, create database and user first
sudo mysql -u root -p
```

In MySQL prompt:
```sql
CREATE DATABASE IF NOT EXISTS opal;
CREATE USER IF NOT EXISTS 'opal'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Then import:
```bash
# On VM
mysql -u root -p opal < /tmp/opal_database_backup.sql
```

### Step 5: Verify on VM

```bash
# On VM
mysql -u opal -p -e "USE opal; SHOW TABLES;"
mysql -u opal -p -e "USE opal; SELECT COUNT(*) FROM fault;"
```

## Alternative: Fix opal User on Local Machine

If you want to use the `opal` user for future exports:

```bash
# Login as root
sudo mysql -u root -p
```

In MySQL prompt:
```sql
-- Check if opal user exists
SELECT User, Host FROM mysql.user WHERE User='opal';

-- If it doesn't exist, create it
CREATE USER 'opal'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Then you can use:
```bash
mysqldump -u opal -p opal > opal_database_backup.sql
```

## One-Liner (Export + Transfer + Import)

From your local machine, you can do it all at once:

```bash
# Export, compress, transfer, and import in one command
mysqldump -u root -p opal | gzip | ssh root@VM_IP 'gunzip | mysql -u root -p opal'
```

This will:
1. Export database (prompts for local root password)
2. Compress it
3. Transfer to VM
4. Decompress and import (prompts for VM root password)

---

**Recommended:** Use root for export since you already have access. The VM will have its own `opal` user with its own password.



