# Fix Collation Error: utf8mb4_uca1400_ai_ci

## Problem
The VM's MariaDB version doesn't support the collation `utf8mb4_uca1400_ai_ci` that was used in your local database.

## Solution: Replace Collation in SQL File

### Option 1: Fix on Local Machine (Before Transfer)

```bash
# On your LOCAL machine
cd ~/Desktop/Subaru_Telescope/OPAL

# Replace the collation with a compatible one
sed -i '' 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' opal_database_backup.sql

# Or use utf8mb4_general_ci (faster, less accurate)
# sed -i '' 's/utf8mb4_uca1400_ai_ci/utf8mb4_general_ci/g' opal_database_backup.sql

# Then transfer the fixed file
scp opal_database_backup.sql root@VM_IP:/tmp/
```

### Option 2: Fix on VM (After Transfer)

```bash
# On VM
cd /tmp

# Replace the collation
sed -i 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' opal_database_backup.sql

# Or use utf8mb4_general_ci
# sed -i 's/utf8mb4_uca1400_ai_ci/utf8mb4_general_ci/g' opal_database_backup.sql

# Then import
mysql -u root -p opal < opal_database_backup.sql
```

### Option 3: Export with Compatible Collation (Best Solution)

```bash
# On your LOCAL machine, export with compatible collation
mysqldump -u root -p --default-character-set=utf8mb4 \
  --skip-set-charset opal > opal_database_backup.sql

# Then manually fix any remaining collation issues
sed -i '' 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' opal_database_backup.sql

# Transfer and import
scp opal_database_backup.sql root@VM_IP:/tmp/
# On VM:
mysql -u root -p opal < /tmp/opal_database_backup.sql
```

## Quick Fix (Recommended)

**On your LOCAL machine:**

```bash
cd ~/Desktop/Subaru_Telescope/OPAL

# Fix the collation in the SQL file
sed -i '' 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' opal_database_backup.sql

# Verify the replacement worked
grep -c "utf8mb4_uca1400_ai_ci" opal_database_backup.sql
# Should return 0 (no matches found)

# Transfer fixed file
scp opal_database_backup.sql root@VM_IP:/tmp/
```

**On VM:**

```bash
# Import the fixed file
mysql -u root -p opal < /tmp/opal_database_backup.sql
```

## Alternative: Fix on VM

If you already transferred the file:

```bash
# On VM
cd /tmp

# Fix the collation
sed -i 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' opal_database_backup.sql

# Import
mysql -u root -p opal < opal_database_backup.sql
```

## Collation Options

- **utf8mb4_unicode_ci** - Recommended (accurate, supports all languages)
- **utf8mb4_general_ci** - Faster, less accurate (good for English)
- **utf8mb4_bin** - Binary (case-sensitive, fastest)

For FATS system, `utf8mb4_unicode_ci` is recommended.

## Verify Import

After successful import:

```bash
# On VM
mysql -u opal -p -e "USE opal; SHOW TABLES;"
mysql -u opal -p -e "USE opal; SELECT COUNT(*) FROM fault;"
mysql -u opal -p -e "USE opal; SHOW TABLE STATUS LIKE 'fault';" | grep Collation
```

## If You Still Get Errors

If there are other collation issues:

```bash
# On VM, check what collations are available
mysql -u root -p -e "SHOW COLLATION LIKE 'utf8mb4%';"

# Replace all problematic collations
sed -i 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' /tmp/opal_database_backup.sql
sed -i 's/utf8mb4_0900_ai_ci/utf8mb4_unicode_ci/g' /tmp/opal_database_backup.sql
```

---

**Quick Command Summary:**

```bash
# On LOCAL: Fix and transfer
sed -i '' 's/utf8mb4_uca1400_ai_ci/utf8mb4_unicode_ci/g' opal_database_backup.sql
scp opal_database_backup.sql root@VM_IP:/tmp/

# On VM: Import
mysql -u root -p opal < /tmp/opal_database_backup.sql
```



