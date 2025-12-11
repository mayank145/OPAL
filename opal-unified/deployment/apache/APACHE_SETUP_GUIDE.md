# Apache Server Setup Guide for FATS System

This guide explains how to configure Apache web server for the FATS (Fault Tracking System).

## Prerequisites

- Apache 2.4+ installed
- SSL certificates (for HTTPS)
- Backend running on port 8000
- Frontend built and ready in `frontend/build/`

## Apache Modules Required

Enable the following Apache modules:

```bash
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_wstunnel
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod expires

# Restart Apache
sudo systemctl restart apache2
```

## Configuration Files

Two configuration files are provided:

1. **`fats-backend.conf`** - For API backend (optional, if using separate subdomain)
2. **`fats-frontend.conf`** - For frontend and API proxy (recommended)

## Setup Options

### Option 1: Single Domain (Recommended)

Serve frontend and proxy API requests from the same domain.

**Steps:**

1. **Copy configuration:**
   ```bash
   sudo cp deployment/apache/fats-frontend.conf /etc/apache2/sites-available/fats.conf
   ```

2. **Edit configuration:**
   ```bash
   sudo nano /etc/apache2/sites-available/fats.conf
   ```
   
   Update these paths:
   - `ServerName your-domain.com` - Your domain name
   - `DocumentRoot /path/to/opal-unified/frontend/build` - Path to frontend build
   - SSL certificate paths

3. **Enable site:**
   ```bash
   sudo a2ensite fats.conf
   sudo systemctl reload apache2
   ```

### Option 2: Separate Subdomains

Use separate subdomains for frontend and backend.

**Steps:**

1. **Backend API (api.your-domain.com):**
   ```bash
   sudo cp deployment/apache/fats-backend.conf /etc/apache2/sites-available/fats-backend.conf
   sudo nano /etc/apache2/sites-available/fats-backend.conf
   # Update ServerName and SSL paths
   sudo a2ensite fats-backend.conf
   ```

2. **Frontend (your-domain.com):**
   ```bash
   sudo cp deployment/apache/fats-frontend.conf /etc/apache2/sites-available/fats-frontend.conf
   sudo nano /etc/apache2/sites-available/fats-frontend.conf
   # Update ServerName, DocumentRoot, and remove API proxy sections
   sudo a2ensite fats-frontend.conf
   ```

3. **Reload Apache:**
   ```bash
   sudo systemctl reload apache2
   ```

## Configuration Details

### Frontend Configuration

- **DocumentRoot**: Points to `frontend/build/` directory
- **React Router**: Rewrite rules to serve `index.html` for all routes
- **Static Caching**: 1-year cache for static assets
- **API Proxy**: Proxies `/api/*` requests to backend

### Backend Configuration

- **Proxy**: All requests proxied to `http://127.0.0.1:8000`
- **WebSocket**: Support for WebSocket connections
- **Timeout**: 300 seconds for long-running requests

## SSL/HTTPS Setup

### Using Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-apache

# Get certificate
sudo certbot --apache -d your-domain.com -d www.your-domain.com

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

### Manual SSL Setup

1. Place certificates:
   ```bash
   sudo cp your-cert.crt /etc/ssl/certs/
   sudo cp your-key.key /etc/ssl/private/
   sudo chmod 600 /etc/ssl/private/your-key.key
   ```

2. Update configuration with certificate paths

3. Enable SSL site and restart:
   ```bash
   sudo a2ensite fats.conf
   sudo systemctl restart apache2
   ```

## Testing Configuration

1. **Check syntax:**
   ```bash
   sudo apache2ctl configtest
   ```

2. **Check status:**
   ```bash
   sudo systemctl status apache2
   ```

3. **Test frontend:**
   ```bash
   curl http://your-domain.com
   # Should return HTML
   ```

4. **Test API:**
   ```bash
   curl http://your-domain.com/api/health
   # Should return JSON
   ```

## Troubleshooting

### Backend Not Responding

1. **Check backend is running:**
   ```bash
   curl http://127.0.0.1:8000/health
   ```

2. **Check Apache error logs:**
   ```bash
   sudo tail -f /var/log/apache2/fats-frontend-error.log
   ```

3. **Check proxy configuration:**
   ```bash
   sudo apache2ctl -S
   ```

### Frontend Not Loading

1. **Check build directory exists:**
   ```bash
   ls -la /path/to/opal-unified/frontend/build
   ```

2. **Check permissions:**
   ```bash
   sudo chown -R www-data:www-data /path/to/opal-unified/frontend/build
   sudo chmod -R 755 /path/to/opal-unified/frontend/build
   ```

3. **Check Apache can read files:**
   ```bash
   sudo -u www-data ls /path/to/opal-unified/frontend/build
   ```

### CORS Issues

If you see CORS errors, ensure:

1. Backend CORS is configured correctly in `backend/app/main.py`
2. Apache headers are not conflicting
3. Frontend API URL matches the domain

### React Router 404 Errors

Ensure rewrite rules are enabled:
```apache
RewriteEngine On
RewriteBase /
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

## Security Recommendations

1. **Disable directory listing:**
   ```apache
   Options -Indexes
   ```

2. **Hide Apache version:**
   ```apache
   ServerTokens Prod
   ServerSignature Off
   ```

3. **Limit request size:**
   ```apache
   LimitRequestBody 10485760  # 10MB
   ```

4. **Rate limiting** (install mod_evasive):
   ```bash
   sudo apt-get install libapache2-mod-evasive
   sudo a2enmod evasive
   ```

## Log Files

- **Access logs**: `/var/log/apache2/fats-frontend-access.log`
- **Error logs**: `/var/log/apache2/fats-frontend-error.log`
- **Backend access**: `/var/log/apache2/fats-backend-access.log`
- **Backend errors**: `/var/log/apache2/fats-backend-error.log`

## Performance Tuning

1. **Enable compression:**
   ```bash
   sudo a2enmod deflate
   ```
   
   Add to configuration:
   ```apache
   <Location />
       SetOutputFilter DEFLATE
       SetEnvIfNoCase Request_URI \
           \.(?:gif|jpe?g|png)$ no-gzip dont-vary
   </Location>
   ```

2. **Adjust worker threads** in `/etc/apache2/mpm-common.conf`:
   ```apache
   StartServers 2
   MinSpareThreads 25
   MaxSpareThreads 75
   ThreadsPerChild 25
   MaxRequestWorkers 150
   ```

## Maintenance

### Reload Configuration
```bash
sudo systemctl reload apache2
```

### Restart Apache
```bash
sudo systemctl restart apache2
```

### Check Active Sites
```bash
sudo apache2ctl -S
```

### Disable Site
```bash
sudo a2dissite fats.conf
sudo systemctl reload apache2
```

## Next Steps

After Apache is configured:

1. ✅ Update frontend `.env.production` with correct API URL
2. ✅ Rebuild frontend: `npm run build`
3. ✅ Test all functionality
4. ✅ Set up monitoring and backups
5. ✅ Configure firewall rules

---

**For more details, see:**
- `PRODUCTION_DEPLOYMENT_CHECKLIST.md`
- `VM_DEPLOYMENT_GUIDE.md`

