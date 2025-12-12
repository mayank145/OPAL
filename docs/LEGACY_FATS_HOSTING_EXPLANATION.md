# Legacy FATS System - Hosting Architecture Explanation

## 🏗️ Hosting Architecture Overview

The legacy FATS system uses a **traditional CGI (Common Gateway Interface)** architecture, which is an older web hosting method from the 1990s-2000s.

## 📋 Hosting Components

### 1. **Web Server**
- **Type**: Apache HTTP Server (most likely)
- **Module**: `mod_cgi` or `mod_python` enabled
- **Purpose**: Receives HTTP requests and executes Python scripts

### 2. **CGI Scripts**
- **Files**: `fatsone.py`, `fatslist.py`, `fatscomment.py`
- **Location**: Typically in `/var/www/cgi-bin/` or `/var/www/html/` (with `.cgi` extension or configured to execute `.py` files)
- **Execution**: Each HTTP request spawns a new Python process

### 3. **Python Environment**
- **Shebang lines**: 
  ```python
  #! /usr/local/python
  #! /usr/bin/python
  ```
- **Version**: Python 2.x or Python 3.x (compatible with both)
- **Location**: System Python at `/usr/local/python` or `/usr/bin/python`

### 4. **Database**
- **Type**: MySQL/MariaDB
- **Connection**: Direct MySQLdb/pymysql connections
- **Module**: `dbconnect.py` (contains connection credentials)
- **Connection per request**: Each CGI script opens a new database connection

## 🔄 How It Works (Request Flow)

```
1. User Browser
   ↓ (HTTP Request)
2. Apache Web Server
   ↓ (Receives request for fatslist.py)
3. mod_cgi Module
   ↓ (Spawns new Python process)
4. Python Interpreter
   ↓ (Executes fatslist.py)
5. CGI Module
   ↓ (Parses HTTP headers, form data, cookies)
6. Python Script
   ↓ (Connects to MySQL database)
7. Database Query
   ↓ (Executes SQL)
8. Database Response
   ↓ (Returns data)
9. Python Script
   ↓ (Generates HTML string)
10. print("Content-type: text/html\n\n")
    ↓ (Outputs HTML)
11. Apache Web Server
    ↓ (Sends response to browser)
12. User Browser
    ↓ (Displays HTML page)
```

## 📝 Key Code Patterns

### CGI Request Handling
```python
import cgi
import cgitb; cgitb.enable()  # Error debugging

field = cgi.FieldStorage()  # Gets form data from HTTP request
method = os.environ.get("REQUEST_METHOD", "")  # GET or POST
```

### Database Connection
```python
import dbconnect
import MySQLdb

dbconn = dbconnect.fatsconn()  # Gets DB credentials
db = MySQLdb.connect(
    host=dbconn[0], 
    user=dbconn[1], 
    passwd=dbconn[2], 
    db=dbconn[3]
)
cursor = db.cursor()
```

### HTML Output
```python
def printHTML(maintext):
    printpg = ''
    printpg += "Content-type: text/html;\n\n"  # CGI header
    printpg += "<!DOCTYPE html>"
    printpg += "<HTML><HEAD>..."
    printpg += maintext
    printpg += "</BODY></HTML>"
    print(printpg)  # Outputs to stdout (sent to browser)
```

## 🗂️ Typical File Structure

```
/var/www/html/opal/
├── fatsone.py          # Individual FATS entry view/edit
├── fatslist.py         # FATS listing page
├── fatscomment.py      # FATS comments
├── dbconnect.py        # Database connection config
├── logproc3.py         # Logging utility
└── ... (other .py files)
```

## ⚙️ Apache Configuration

Typical Apache configuration would look like:

```apache
# /etc/apache2/sites-available/opal.conf

<VirtualHost *:80>
    ServerName opal.example.com
    DocumentRoot /var/www/html/opal
    
    # Enable CGI execution
    ScriptAlias /cgi-bin/ /var/www/html/opal/
    
    <Directory "/var/www/html/opal">
        Options +ExecCGI
        AddHandler cgi-script .py
        Require all granted
    </Directory>
</VirtualHost>
```

Or using `.htaccess`:
```apache
Options +ExecCGI
AddHandler cgi-script .py
```

## 🔍 Characteristics of CGI Hosting

### ✅ Advantages (for its time)
- Simple to understand
- No server state to manage
- Each request is isolated
- Works with any web server

### ❌ Disadvantages (modern perspective)
- **Performance**: Spawns new process per request (slow)
- **Scalability**: Cannot handle high traffic
- **Resource usage**: High memory/CPU overhead
- **No connection pooling**: New DB connection per request
- **No shared state**: Cannot cache data between requests
- **Security**: Direct SQL queries (SQL injection vulnerable)
- **Maintenance**: Hard to debug and maintain

## 📊 Performance Comparison

| Metric | Legacy CGI | Modern FastAPI |
|--------|-----------|----------------|
| Requests/sec | ~50-100 | ~1000-5000 |
| Process per request | Yes (new process) | No (shared process) |
| Database connections | New per request | Pooled |
| Memory usage | High | Low |
| Response time | 200-500ms | 10-50ms |

## 🔐 Security Considerations

### Current Issues:
1. **SQL Injection**: Direct string formatting in queries
   ```python
   cursor.execute("select * from fault where idno = %s" % (idno))
   ```
2. **No input validation**: Direct use of `field['idno'].value`
3. **No authentication**: Relies on web server or session cookies
4. **Error exposure**: `cgitb.enable()` shows full tracebacks

## 🌐 Access Pattern

Users access the system via:
- **URL**: `http://server/opal/fatslist.py` or `http://server/cgi-bin/fatslist.py`
- **Form submissions**: POST requests to same script
- **Query parameters**: `?idno=1234&search1=issue`

## 🔄 Migration to Modern System

The new `opal-unified` system replaces this with:
- **FastAPI**: Modern async web framework
- **React**: Client-side rendering
- **REST API**: JSON-based communication
- **Connection pooling**: Efficient database usage
- **Security**: Parameterized queries, input validation

## 📍 Typical Production Setup

Based on the code structure, the legacy system is likely hosted on:

1. **Server**: Linux (Ubuntu/CentOS)
2. **Web Server**: Apache 2.x
3. **Python**: System Python (2.7 or 3.x)
4. **Database**: MySQL/MariaDB on same server or separate
5. **Location**: `/var/www/html/opal/` or similar
6. **Permissions**: Files executable by web server user (www-data/apache)

## 🔧 Maintenance Requirements

- **File permissions**: Scripts must be executable
- **Python path**: Shebang must point to correct Python
- **Database**: Must be accessible from web server
- **Logs**: Usually in `/var/log/apache2/error.log`
- **Debugging**: `cgitb` outputs errors to browser (security risk in production)

## 📚 Summary

The legacy FATS system uses a **server-side CGI architecture** where:
- Each page is a Python script
- Web server executes script on each request
- Script generates HTML and outputs it
- No client-side JavaScript framework
- Direct database connections
- Traditional form-based interactions

This is a **legacy architecture** that was common in the 1990s-2000s but is now considered outdated due to performance and security limitations.

