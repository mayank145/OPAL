# Production Deployment Checklist

## Pre-Deployment

### 1. Security Configuration ✅
- [ ] **SECRET_KEY**: Generate a strong secret key
  ```bash
  python3 -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] **Database Password**: Use strong, unique password
- [ ] **CORS Origins**: Set to production domain(s) only
- [ ] **DEBUG**: Set to `false` in production
- [ ] **Environment Variables**: All sensitive values in `.env` (not committed to git)

### 2. Code Review ✅
- [x] All `print()` statements replaced with proper logging
- [x] Console.log statements conditionalized (development only)
- [x] No hardcoded credentials
- [x] No hardcoded localhost URLs (except in defaults)
- [x] Error messages don't expose sensitive information

### 3. Database Setup ✅
- [ ] Database created and configured
- [ ] Database user has appropriate permissions
- [ ] Database backups configured
- [ ] Connection pool settings optimized for production

### 4. File System ✅
- [ ] `uploads/fats/` directory exists and is writable
- [ ] Proper file permissions set (755 for directories, 644 for files)
- [ ] Disk space sufficient for image uploads
- [ ] Backup strategy for uploaded images

### 5. Dependencies ✅
- [ ] All dependencies installed from `requirements.txt`
- [ ] No development dependencies in production
- [ ] Python version matches (3.9+)
- [ ] Node.js version matches (v16+)

## Backend Deployment

### 1. Environment Setup
```bash
cd backend
cp .env.production.example .env
# Edit .env with production values
```

### 2. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
- [ ] `.env` file configured with production values
- [ ] `DEBUG=false` in `.env`
- [ ] Database connection string correct
- [ ] CORS origins set to production domain
- [ ] Secret key generated and set

### 4. Logging
- [ ] `logs/` directory created
- [ ] Log rotation configured (optional, via systemd or logrotate)
- [ ] Log file permissions set correctly

### 5. Run as Service (systemd)
```bash
# Create systemd service file
sudo nano /etc/systemd/system/opal-backend.service
```

Service file content:
```ini
[Unit]
Description=OPAL Unified System Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/opal-unified/backend
Environment="PATH=/path/to/opal-unified/backend/venv/bin"
ExecStart=/path/to/opal-unified/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable opal-backend
sudo systemctl start opal-backend
sudo systemctl status opal-backend
```

### 6. Verify Backend
- [ ] Health check: `curl http://localhost:8000/health`
- [ ] Database health: `curl http://localhost:8000/health/db`
- [ ] API endpoint: `curl http://localhost:8000/api/v1/fats/?limit=1`
- [ ] Logs: `tail -f logs/app.log`

## Frontend Deployment

### 1. Environment Setup
```bash
cd frontend
cp .env.production.example .env.production
# Edit .env.production with production API URL
```

### 2. Build for Production
```bash
npm install
npm run build
```

### 3. Serve with Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;
    
    # Frontend
    root /path/to/opal-unified/frontend/build;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API Proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 4. Verify Frontend
- [ ] Frontend loads at production URL
- [ ] API calls work (check Network tab)
- [ ] No console errors
- [ ] Images load correctly

## Security Hardening

### 1. Firewall
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. SSL/TLS
- [ ] SSL certificate installed (Let's Encrypt recommended)
- [ ] HTTPS redirect configured
- [ ] HSTS headers enabled
- [ ] Strong cipher suites configured

### 3. Database Security
- [ ] Database user has minimal required permissions
- [ ] Database not accessible from outside (firewall)
- [ ] Regular backups configured
- [ ] Backup encryption enabled

### 4. Application Security
- [ ] Rate limiting configured (if needed)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention (React handles this)
- [ ] CSRF protection (if needed)

## Monitoring & Maintenance

### 1. Logging
- [ ] Log rotation configured
- [ ] Log monitoring set up
- [ ] Error alerts configured

### 2. Backups
- [ ] Database backup script created
- [ ] Image backup script created
- [ ] Backup schedule configured (daily recommended)
- [ ] Backup restoration tested

### 3. Performance
- [ ] Database indexes optimized
- [ ] Query performance tested
- [ ] Image optimization (if needed)
- [ ] CDN configured (optional)

### 4. Updates
- [ ] Update strategy defined
- [ ] Rollback plan prepared
- [ ] Testing environment available

## Post-Deployment Verification

### 1. Functional Testing
- [ ] Create new FATS entry
- [ ] Edit FATS entry
- [ ] Add comment
- [ ] Upload image
- [ ] View images
- [ ] Search functionality
- [ ] Filter functionality

### 2. Performance Testing
- [ ] Page load times acceptable
- [ ] API response times acceptable
- [ ] Image upload works
- [ ] No memory leaks

### 3. Security Testing
- [ ] HTTPS enforced
- [ ] CORS configured correctly
- [ ] No sensitive data in responses
- [ ] Authentication working (if implemented)

## Rollback Plan

If issues occur:
1. Stop services: `sudo systemctl stop opal-backend`
2. Restore database from backup
3. Restore code from previous version
4. Restart services
5. Verify functionality

## Support Information

- **Backend Logs**: `/path/to/opal-unified/backend/logs/app.log`
- **Nginx Logs**: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- **System Logs**: `journalctl -u opal-backend -f`
- **Health Check**: `https://your-domain.com/api/health`

## Notes

- Keep `.env` files secure and never commit them to git
- Regularly update dependencies for security patches
- Monitor disk space for image uploads
- Set up automated backups
- Document any custom configurations

