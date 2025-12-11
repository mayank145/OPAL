# Phase 0: Emergency Security Fixes
## IMMEDIATE ACTION REQUIRED

**Timeline:** 1-2 weeks  
**Priority:** CRITICAL  
**Status:** 🔴 NOT STARTED

This document provides step-by-step instructions for implementing critical security patches to the legacy OPAL system before the full modernization.

---

## ⚠️ WARNING

The current system has **CRITICAL** security vulnerabilities:
- SQL Injection in ALL files
- No input validation
- Weak session management
- No CSRF protection

**DO NOT** expose this system to the internet without these fixes.

---

## Quick Start Checklist

- [ ] Create backup of entire system
- [ ] Create `patches/` directory
- [ ] Create `validation.py` module
- [ ] Create `session_manager.py` module
- [ ] Patch all SQL queries (46 files)
- [ ] Add input validation
- [ ] Implement server-side sessions
- [ ] Add HTTPS redirect
- [ ] Add security headers
- [ ] Test all patched functionality
- [ ] Deploy patches to production
- [ ] Monitor for issues

---

## 1. Preparation (Day 1)

### 1.1 Backup Everything

```bash
# Create backup directory
mkdir -p /backup/opal-$(date +%Y%m%d)

# Backup code
cp -r /var/www/html/opal /backup/opal-$(date +%Y%m%d)/code

# Backup database
mysqldump -u root -p sumlogs > /backup/opal-$(date +%Y%m%d)/database.sql

# Verify backups
ls -lh /backup/opal-$(date +%Y%m%d)/
```

### 1.2 Create Patches Directory

```bash
cd /var/www/html/opal
mkdir patches
cd patches
```

### 1.3 Setup Version Control (if not already)

```bash
cd /var/www/html/opal
git init
git add .
git commit -m "Initial commit - legacy code before patches"
git branch emergency-patches
git checkout emergency-patches
```

---

## 2. Create Security Modules (Day 1-2)

### 2.1 Input Validation Module

Create `patches/validation.py`:

```python
#!/usr/bin/env python3
"""
Input validation and sanitization module
"""

import re
from html import escape
from datetime import datetime

class ValidationError(Exception):
    """Custom validation exception"""
    pass

def validate_username(username: str) -> str:
    """
    Validate username
    - 3-30 characters
    - Alphanumeric, underscore, hyphen only
    """
    if not username:
        raise ValidationError("Username is required")
    
    username = username.strip()
    
    if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
        raise ValidationError(
            "Username must be 3-30 characters and contain only letters, numbers, underscore, or hyphen"
        )
    
    return escape(username)

def validate_email(email: str) -> str:
    """Validate email address"""
    if not email:
        raise ValidationError("Email is required")
    
    email = email.strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError("Invalid email format")
    
    return escape(email)

def validate_date(date_str: str) -> str:
    """
    Validate date in YYYY-MM-DD format
    """
    if not date_str:
        raise ValidationError("Date is required")
    
    date_str = date_str.strip()
    
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        raise ValidationError("Date must be in YYYY-MM-DD format")
    
    # Verify it's a valid date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValidationError("Invalid date")
    
    return date_str

def validate_time(time_str: str) -> str:
    """
    Validate time in HH:MM format
    """
    if not time_str:
        raise ValidationError("Time is required")
    
    time_str = time_str.strip()
    
    if not re.match(r'^\d{2}:\d{2}(:\d{2})?$', time_str):
        raise ValidationError("Time must be in HH:MM or HH:MM:SS format")
    
    return time_str

def validate_text_field(text: str, field_name: str, min_len: int = 0, max_len: int = 1000) -> str:
    """
    Validate general text field
    """
    if not text and min_len > 0:
        raise ValidationError(f"{field_name} is required")
    
    text = text.strip() if text else ""
    
    if len(text) < min_len:
        raise ValidationError(f"{field_name} must be at least {min_len} characters")
    
    if len(text) > max_len:
        raise ValidationError(f"{field_name} must be at most {max_len} characters")
    
    # Basic XSS prevention
    return escape(text)

def validate_id(id_val: str, field_name: str = "ID") -> int:
    """
    Validate numeric ID
    """
    if not id_val:
        raise ValidationError(f"{field_name} is required")
    
    try:
        id_int = int(id_val)
        if id_int < 0:
            raise ValidationError(f"{field_name} must be positive")
        return id_int
    except ValueError:
        raise ValidationError(f"{field_name} must be a number")

def sanitize_sql_param(value):
    """
    Prepare value for SQL parameter
    Returns None for empty strings
    """
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value
```

### 2.2 Session Management Module

Create `patches/session_manager.py`:

```python
#!/usr/bin/env python3
"""
Server-side session management
Replaces client-side cookie storage
"""

import shelve
import secrets
import datetime
from typing import Dict, Optional

SESSION_DB = '/var/www/html/opal/sessions/sessions.db'
SESSION_TIMEOUT_HOURS = 8

class SessionManager:
    
    @staticmethod
    def create_session(username: str, additional_data: Dict = None) -> str:
        """
        Create a new session
        Returns session token
        """
        session_token = secrets.token_urlsafe(32)
        
        session_data = {
            'username': username,
            'created_at': datetime.datetime.now(),
            'expires_at': datetime.datetime.now() + datetime.timedelta(hours=SESSION_TIMEOUT_HOURS),
            'last_activity': datetime.datetime.now(),
        }
        
        if additional_data:
            session_data.update(additional_data)
        
        with shelve.open(SESSION_DB) as db:
            db[session_token] = session_data
        
        return session_token
    
    @staticmethod
    def get_session(session_token: str) -> Optional[Dict]:
        """
        Retrieve session data
        Returns None if session not found or expired
        """
        if not session_token:
            return None
        
        with shelve.open(SESSION_DB) as db:
            if session_token not in db:
                return None
            
            session_data = db[session_token]
            
            # Check if expired
            if datetime.datetime.now() > session_data['expires_at']:
                del db[session_token]
                return None
            
            # Update last activity
            session_data['last_activity'] = datetime.datetime.now()
            db[session_token] = session_data
            
            return session_data
    
    @staticmethod
    def update_session(session_token: str, data: Dict) -> bool:
        """
        Update session data
        """
        with shelve.open(SESSION_DB) as db:
            if session_token not in db:
                return False
            
            session_data = db[session_token]
            session_data.update(data)
            db[session_token] = session_data
            
            return True
    
    @staticmethod
    def delete_session(session_token: str) -> bool:
        """
        Delete session (logout)
        """
        with shelve.open(SESSION_DB) as db:
            if session_token in db:
                del db[session_token]
                return True
        return False
    
    @staticmethod
    def cleanup_expired_sessions():
        """
        Remove expired sessions
        Should be run periodically (cron job)
        """
        now = datetime.datetime.now()
        expired_count = 0
        
        with shelve.open(SESSION_DB) as db:
            expired_tokens = [
                token for token, data in db.items()
                if now > data['expires_at']
            ]
            
            for token in expired_tokens:
                del db[token]
                expired_count += 1
        
        return expired_count

# Helper function for CGI scripts
def get_session_from_cookie():
    """
    Extract session token from cookie and return session data
    """
    import os
    import http.cookies as Cookie
    
    try:
        cookie_string = os.environ.get('HTTP_COOKIE', '')
        cookies = Cookie.SimpleCookie()
        cookies.load(cookie_string)
        
        if 'session_token' in cookies:
            session_token = cookies['session_token'].value
            return SessionManager.get_session(session_token)
    except Exception:
        pass
    
    return None

def set_session_cookie(session_token: str) -> str:
    """
    Generate Set-Cookie header for session token
    """
    cookie = f"session_token={session_token}; "
    cookie += f"Max-Age={SESSION_TIMEOUT_HOURS * 3600}; "
    cookie += "Path=/; "
    cookie += "HttpOnly; "
    cookie += "Secure; "  # Enable this when using HTTPS
    cookie += "SameSite=Lax"
    
    return f"Set-Cookie: {cookie}\n"
```

### 2.3 Database Helper Module

Create `patches/db_helper.py`:

```python
#!/usr/bin/env python3
"""
Database helper with parameterized queries
"""

def execute_safe_query(cursor, query: str, params: tuple = None):
    """
    Execute parameterized query safely
    """
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    return cursor

def execute_safe_select(cursor, query: str, params: tuple = None):
    """
    Execute SELECT query and return results
    """
    execute_safe_query(cursor, query, params)
    return cursor.fetchall()

def execute_safe_insert(cursor, query: str, params: tuple):
    """
    Execute INSERT query and return last insert id
    """
    execute_safe_query(cursor, query, params)
    return cursor.lastrowid

def execute_safe_update(cursor, query: str, params: tuple):
    """
    Execute UPDATE query and return affected rows
    """
    execute_safe_query(cursor, query, params)
    return cursor.rowcount
```

---

## 3. Patch SQL Queries (Day 3-5)

### 3.1 Example: Patching userlist.py

**BEFORE (VULNERABLE):**

```python
cursor2.execute("select user, email, stnuser, idno, privy, train, status from users where stnuser='%s' order by user" % ( username ))
```

**AFTER (SECURE):**

```python
import sys
sys.path.insert(0, '/var/www/html/opal/patches')
from validation import validate_username

# Validate input
username = validate_username(username)

# Use parameterized query
cursor2.execute(
    "SELECT user, email, stnuser, idno, privy, train, status FROM users WHERE stnuser=%s ORDER BY user",
    (username,)
)
```

### 3.2 Automated Patching Script

Create `patches/patch_sql_queries.py`:

```python
#!/usr/bin/env python3
"""
Automated SQL injection patching script
"""

import os
import re
import shutil
from pathlib import Path

OPAL_DIR = Path('/var/www/html/opal')
BACKUP_DIR = Path('/backup/opal-patches')

def backup_file(filepath):
    """Create backup before patching"""
    backup_path = BACKUP_DIR / filepath.name
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backed up: {filepath.name}")

def find_vulnerable_queries(content):
    """Find SQL queries using string formatting"""
    patterns = [
        r'cursor\d*\.execute\(["\'].*%s.*["\'] % ',
        r'cursor\d*\.execute\(["\'].*\{.*\}.*["\']\.format\(',
    ]
    
    vulnerabilities = []
    for i, line in enumerate(content.split('\n'), 1):
        for pattern in patterns:
            if re.search(pattern, line):
                vulnerabilities.append((i, line.strip()))
    
    return vulnerabilities

def patch_file(filepath):
    """Patch a single Python file"""
    print(f"\n{'='*60}")
    print(f"Patching: {filepath.name}")
    print('='*60)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find vulnerabilities
    vulnerabilities = find_vulnerable_queries(content)
    
    if not vulnerabilities:
        print("✓ No SQL injection vulnerabilities found")
        return
    
    print(f"⚠️  Found {len(vulnerabilities)} potential vulnerabilities:")
    for line_num, line in vulnerabilities:
        print(f"  Line {line_num}: {line[:80]}...")
    
    # Create backup
    backup_file(filepath)
    
    print(f"\n⚠️  Manual patching required for {filepath.name}")
    print("   Review each query and convert to parameterized format")

def main():
    """Main patching function"""
    BACKUP_DIR.mkdir(exist_ok=True)
    
    print("OPAL SQL Injection Patching Tool")
    print("="*60)
    
    # Find all Python files
    python_files = list(OPAL_DIR.glob('*.py'))
    
    print(f"\nFound {len(python_files)} Python files")
    
    total_vulns = 0
    
    for filepath in python_files:
        if filepath.name.startswith('patch_'):
            continue
        
        patch_file(filepath)
        
        with open(filepath, 'r') as f:
            content = f.read()
        vulns = find_vulnerable_queries(content)
        total_vulns += len(vulns)
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print('='*60)
    print(f"Files scanned: {len(python_files)}")
    print(f"Vulnerabilities found: {total_vulns}")
    print(f"\nNext steps:")
    print("1. Review each file marked with vulnerabilities")
    print("2. Convert queries to parameterized format")
    print("3. Test each patched file")
    print("4. Deploy patches")

if __name__ == '__main__':
    main()
```

Run the script:

```bash
cd /var/www/html/opal/patches
python3 patch_sql_queries.py
```

### 3.3 Manual Patching Guidelines

For each file with SQL queries:

1. **Add imports at the top:**
   ```python
   import sys
   sys.path.insert(0, '/var/www/html/opal/patches')
   from validation import validate_username, validate_text_field, validate_id
   ```

2. **Validate all user inputs:**
   ```python
   # Before using any CGI field value
   username = validate_username(field['username'].value)
   idno = validate_id(field['idno'].value)
   ```

3. **Convert queries to parameterized:**
   ```python
   # BEFORE
   cursor.execute("SELECT * FROM users WHERE username='%s' AND id=%s" % (username, idno))
   
   # AFTER
   cursor.execute("SELECT * FROM users WHERE username=%s AND id=%s", (username, idno))
   ```

4. **Test the file:**
   ```bash
   # Test basic functionality
   python3 userlist.py
   ```

---

## 4. Update Authentication (Day 6-7)

### 4.1 Patch login2.py

**Key changes:**
- Use SessionManager instead of client-side cookies
- Set secure cookie with session token
- Store minimal data in cookie

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/var/www/html/opal/patches')
from session_manager import SessionManager, set_session_cookie
from validation import validate_username

# ... existing imports ...

# After successful authentication
if user_authenticated:
    # Create server-side session
    session_token = SessionManager.create_session(
        username=username,
        additional_data={
            'logcrew': logcrew,
            'privy': user_privy
        }
    )
    
    # Set session cookie
    print(set_session_cookie(session_token))
    print("Content-type: text/html\n")
    # ... rest of response ...
```

### 4.2 Patch logout.py

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/var/www/html/opal/patches')
from session_manager import get_session_from_cookie, SessionManager

session_data = get_session_from_cookie()
if session_data:
    # Get token from cookie
    import os
    import http.cookies as Cookie
    cookie_string = os.environ.get('HTTP_COOKIE', '')
    cookies = Cookie.SimpleCookie()
    cookies.load(cookie_string)
    
    if 'session_token' in cookies:
        session_token = cookies['session_token'].value
        SessionManager.delete_session(session_token)

# Clear cookie
print("Set-Cookie: session_token=; Max-Age=0; Path=/\n")
print("Content-type: text/html\n")
# ... redirect to login ...
```

### 4.3 Patch logproc3.py validCookie()

```python
def validCookie():
    """Validate session using server-side storage"""
    import sys
    sys.path.insert(0, '/var/www/html/opal/patches')
    from session_manager import get_session_from_cookie
    
    session_data = get_session_from_cookie()
    return session_data is not None

def getUsername():
    """Get username from session"""
    import sys
    sys.path.insert(0, '/var/www/html/opal/patches')
    from session_manager import get_session_from_cookie
    
    session_data = get_session_from_cookie()
    if not session_data:
        return ('None', 'none', '0', 'WP')
    
    username = session_data.get('username', 'None')
    end = session_data.get('expires_at').strftime('%m-%d %H:%M')
    term = '480 min'
    logcrew = session_data.get('logcrew', 'WP')
    
    return (username, end, term, logcrew)
```

---

## 5. Add Security Headers (Day 7)

### 5.1 Create Security Headers Module

Create `patches/security_headers.py`:

```python
#!/usr/bin/env python3
"""
Security headers for all responses
"""

def get_security_headers():
    """Return security headers string"""
    headers = []
    headers.append("X-Frame-Options: DENY")
    headers.append("X-Content-Type-Options: nosniff")
    headers.append("X-XSS-Protection: 1; mode=block")
    headers.append("Strict-Transport-Security: max-age=31536000; includeSubDomains")
    headers.append("Content-Security-Policy: default-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.tiny.cloud;")
    headers.append("Referrer-Policy: strict-origin-when-cross-origin")
    
    return '\n'.join(headers) + '\n'

def print_with_security_headers(content_type="text/html"):
    """Print headers including security headers"""
    print(get_security_headers())
    print(f"Content-Type: {content_type}\n")
```

### 5.2 Add to printHTML Functions

Add security headers to all `printHTML` functions:

```python
def printHTML(maintext):
    import sys
    sys.path.insert(0, '/var/www/html/opal/patches')
    from security_headers import print_with_security_headers
    
    # Print security headers
    print_with_security_headers()
    
    # Rest of existing code...
    printpg = "<HTML><HEAD>..."
    print(printpg)
```

---

## 6. Setup HTTPS (Day 8)

### 6.1 Install Let's Encrypt Certificate

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-apache

# Get certificate
sudo certbot --apache -d opal.subaru.nao.ac.jp

# Test auto-renewal
sudo certbot renew --dry-run
```

### 6.2 Configure Apache for HTTPS Redirect

Edit `/etc/apache2/sites-available/opal.conf`:

```apache
<VirtualHost *:80>
    ServerName opal.subaru.nao.ac.jp
    
    # Redirect all HTTP to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>

<VirtualHost *:443>
    ServerName opal.subaru.nao.ac.jp
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/opal.subaru.nao.ac.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/opal.subaru.nao.ac.jp/privkey.pem
    
    # Security headers
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    
    DocumentRoot /var/www/html/opal
    
    <Directory /var/www/html/opal>
        Options +ExecCGI
        AddHandler cgi-script .py
        Require all granted
    </Directory>
</VirtualHost>
```

Restart Apache:

```bash
sudo systemctl restart apache2
```

---

## 7. Testing (Day 9-10)

### 7.1 Manual Testing Checklist

- [ ] Login works with new session management
- [ ] Logout clears session properly
- [ ] Session expires after timeout
- [ ] All forms submit correctly
- [ ] SQL queries don't crash (parameterization works)
- [ ] Special characters in input are handled
- [ ] HTTPS redirect works
- [ ] Security headers present in responses

### 7.2 Security Testing

#### SQL Injection Test

Try malicious inputs:
```
Username: admin' OR '1'='1
Password: anything

Expected: Login fails, no SQL error
```

#### XSS Test

Try entering:
```
<script>alert('XSS')</script>

Expected: Escaped as &lt;script&gt;...
```

#### Session Hijacking Test

1. Login from Browser A
2. Copy session cookie
3. Open Browser B, set same cookie
4. Expected: Both sessions should work (but timeout correctly)

### 7.3 Automated Security Scan

```bash
# Install OWASP ZAP
sudo apt-get install zaproxy

# Run baseline scan
zap-baseline.py -t https://opal.subaru.nao.ac.jp -r report.html
```

---

## 8. Deployment (Day 11)

### 8.1 Pre-Deployment Checklist

- [ ] All files backed up
- [ ] Database backed up
- [ ] All patches tested individually
- [ ] Security scan passed
- [ ] Rollback plan ready
- [ ] Team notified of deployment
- [ ] Maintenance window scheduled

### 8.2 Deployment Script

Create `deploy_patches.sh`:

```bash
#!/bin/bash
set -e

echo "Deploying OPAL Security Patches..."
echo "=================================="

# Check if running as correct user
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Create final backup
BACKUP_DIR="/backup/opal-pre-patch-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR

echo "Creating backup..."
cp -r /var/www/html/opal $BACKUP_DIR/
mysqldump -u root -p sumlogs > $BACKUP_DIR/database.sql

# Copy patched files
echo "Deploying patched files..."
cd /var/www/html/opal

# Set correct permissions
chmod 644 *.py
chmod 755 patches/*.py
chown -R www-data:www-data .

# Create session directory
mkdir -p sessions
chmod 700 sessions
chown www-data:www-data sessions

# Restart web server
echo "Restarting Apache..."
systemctl restart apache2

# Health check
echo "Running health check..."
sleep 2
curl -f https://opal.subaru.nao.ac.jp/login.py > /dev/null

if [ $? -eq 0 ]; then
    echo "✓ Deployment successful!"
    echo "✓ Backup saved to: $BACKUP_DIR"
else
    echo "✗ Health check failed!"
    echo "  Consider rolling back"
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. Monitor logs: tail -f /var/log/apache2/error.log"
echo "2. Test all functionality"
echo "3. Setup session cleanup cron job"
```

### 8.3 Setup Session Cleanup Cron

```bash
# Add to crontab
crontab -e

# Add line:
0 2 * * * /usr/bin/python3 /var/www/html/opal/patches/cleanup_sessions.py
```

Create `cleanup_sessions.py`:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/var/www/html/opal/patches')
from session_manager import SessionManager

if __name__ == '__main__':
    count = SessionManager.cleanup_expired_sessions()
    print(f"Cleaned up {count} expired sessions")
```

---

## 9. Post-Deployment Monitoring (Day 12-14)

### 9.1 Monitor Apache Error Logs

```bash
# Real-time monitoring
tail -f /var/log/apache2/error.log

# Check for errors
grep -i "error\|exception" /var/log/apache2/error.log
```

### 9.2 Monitor Application Logs

Create simple logging:

```python
# Add to each patched file
import logging
logging.basicConfig(
    filename='/var/log/opal/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log important events
logging.info(f"User {username} logged in")
logging.warning(f"Failed login attempt for {username}")
logging.error(f"Database error: {str(e)}")
```

### 9.3 Create Monitoring Dashboard

Simple status page at `status.py`:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/var/www/html/opal/patches')
from session_manager import SessionManager
import MySQLdb
import dbconnect

print("Content-Type: text/html\n")

# Check database
try:
    dbconn = dbconnect.dbconn()
    db = MySQLdb.connect(host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
    db_status = "✓ OK"
except Exception as e:
    db_status = f"✗ ERROR: {e}"

# Check session storage
try:
    # Try to access session db
    with shelve.open(SESSION_DB) as db:
        session_count = len(db)
    session_status = f"✓ OK ({session_count} active sessions)"
except Exception as e:
    session_status = f"✗ ERROR: {e}"

print(f"""
<html>
<head><title>OPAL Status</title></head>
<body>
<h1>OPAL System Status</h1>
<ul>
<li>Database: {db_status}</li>
<li>Sessions: {session_status}</li>
</ul>
</body>
</html>
""")
```

---

## 10. Rollback Procedure

If critical issues occur:

### 10.1 Immediate Rollback

```bash
#!/bin/bash
# rollback.sh

BACKUP_DIR="/backup/opal-pre-patch-YYYYMMDD-HHMMSS"  # Use actual backup dir

echo "Rolling back to pre-patch state..."

# Stop web server
systemctl stop apache2

# Restore files
rm -rf /var/www/html/opal
cp -r $BACKUP_DIR/code /var/www/html/opal

# Restore database (if needed)
# mysql -u root -p sumlogs < $BACKUP_DIR/database.sql

# Restart web server
systemctl start apache2

echo "Rollback complete"
```

### 10.2 Partial Rollback

If only specific files are problematic:

```bash
# Restore individual file
cp /backup/opal-pre-patch-YYYYMMDD/userlist.py /var/www/html/opal/
```

---

## Success Criteria

### Security
- [ ] Zero SQL injection vulnerabilities (verified with sqlmap)
- [ ] All inputs validated and sanitized
- [ ] Server-side session management working
- [ ] HTTPS enforced
- [ ] Security headers present
- [ ] OWASP ZAP scan shows no critical issues

### Functionality
- [ ] All existing features work
- [ ] Login/logout working
- [ ] Forms submit correctly
- [ ] Database operations work
- [ ] No performance degradation

### Operations
- [ ] No errors in logs
- [ ] Sessions clean up automatically
- [ ] Monitoring in place
- [ ] Rollback tested and ready

---

## Support Contacts

**For issues during patching:**
- Primary: [Your contact]
- Backup: [Backup contact]
- Emergency: [Emergency contact]

**Resources:**
- Backup location: `/backup/opal-*`
- Logs: `/var/log/apache2/` and `/var/log/opal/`
- Documentation: `/var/www/html/opal/docs/`

---

## Next Steps After Phase 0

Once emergency patches are deployed and stable:

1. ✅ Begin Phase 1: Planning & Setup
2. ✅ Start architecture design for new system
3. ✅ Continue using patched system safely
4. ✅ Plan gradual migration to modern stack

**Remember:** These patches make the system SAFER, but a complete modernization is still needed for long-term sustainability.

