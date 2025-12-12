# OPAL FATS - Quick Deployment Checklist

## 📋 Quick Reference for Implementation

**Server:** 133.40.149.66  
**User:** root  
**Application Path:** /opt/OPAL/opal-unified

---

## ✅ Pre-Deployment Checklist

- [ ] Have root access to server
- [ ] Apache (httpd) is installed and running
- [ ] Current dev servers are running (ports 3000, 8000)
- [ ] Database is accessible (user: opal, pass: opal)

---

## 🚀 Part 1: Production Deployment (30-40 minutes)

### Quick Steps:

```bash
# 1. Stop development servers (2 min)
pkill -f "uvicorn app.main:app"
pkill -f "react-scripts start"

# 2. Update backend config (2 min)
nano /opt/OPAL/opal-unified/backend/.env
# Change: DEBUG=false

# 3. Create systemd service (5 min)
nano /etc/systemd/system/opal-backend.service
# Copy content from main instructions
systemctl daemon-reload
systemctl enable opal-backend
systemctl start opal-backend

# 4. Build frontend (10 min)
cd /opt/OPAL/opal-unified/frontend
cat > .env.production << 'EOF'
REACT_APP_API_URL=http://133.40.149.66
EOF
npm run build

# 5. Configure Apache (10 min)
nano /etc/httpd/conf.d/opal-fats.conf
# Copy content from main instructions
setsebool -P httpd_can_network_connect 1
httpd -t
systemctl restart httpd

# 6. Configure firewall (2 min)
firewall-cmd --permanent --add-service=http
firewall-cmd --reload

# 7. Verify (5 min)
curl http://133.40.149.66/
curl http://133.40.149.66/api/v1/fats/stats/summary
# Open in browser: http://133.40.149.66/
```

---

## 💾 Part 2: Backup Configuration (20-30 minutes)

### Quick Steps:

```bash
# 1. Create backup directory (1 min)
mkdir -p /opt/backups/opal-fats/{database,files}
chmod 700 /opt/backups/opal-fats

# 2. Create backup scripts (10 min)
# Create 3 scripts (copy from main instructions):
nano /opt/backups/opal-fats/backup-database.sh
nano /opt/backups/opal-fats/backup-files.sh
nano /opt/backups/opal-fats/backup-all.sh

chmod +x /opt/backups/opal-fats/*.sh

# 3. Test backups (5 min)
/opt/backups/opal-fats/backup-all.sh

# 4. Set up cron (2 min)
crontab -e
# Add: 0 2 * * * /opt/backups/opal-fats/backup-all.sh >> /opt/backups/opal-fats/backup.log 2>&1

# 5. Create restore scripts (5 min)
nano /opt/backups/opal-fats/restore-database.sh
nano /opt/backups/opal-fats/restore-files.sh
chmod +x /opt/backups/opal-fats/restore-*.sh

# 6. Verify (2 min)
ls -lh /opt/backups/opal-fats/database/
ls -lh /opt/backups/opal-fats/files/
crontab -l
```

---

## 🎯 Final Verification

```bash
# Backend service
systemctl status opal-backend

# Apache serving
curl -I http://133.40.149.66/

# API working
curl http://133.40.149.66/api/v1/fats/stats/summary

# Backups exist
ls -lh /opt/backups/opal-fats/database/
ls -lh /opt/backups/opal-fats/files/

# Cron configured
crontab -l | grep opal-fats
```

**Open in browser:** http://133.40.149.66/

---

## 📱 Quick Commands Reference

### Service Management
```bash
systemctl status opal-backend    # Check status
systemctl restart opal-backend   # Restart
journalctl -u opal-backend -f    # View logs
systemctl restart httpd          # Restart Apache
```

### Backups
```bash
/opt/backups/opal-fats/backup-all.sh              # Manual backup
ls -lh /opt/backups/opal-fats/database/           # List DB backups
ls -lh /opt/backups/opal-fats/files/              # List file backups
```

### Logs
```bash
tail -f /opt/OPAL/opal-unified/backend/logs/backend.log
tail -f /var/log/httpd/opal-fats-error.log
tail -f /opt/backups/opal-fats/backup.log
```

---

## 🔥 Emergency Rollback

If something goes wrong:

```bash
# Stop production backend
systemctl stop opal-backend

# Start development backend
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &

# Start development frontend
cd /opt/OPAL/opal-unified/frontend
nohup npm start > /tmp/frontend.log 2>&1 &

# Access at: http://133.40.149.66:3000
```

---

## ✅ Success Criteria

- [ ] Can access application at: http://133.40.149.66/
- [ ] Backend service auto-starts: `systemctl is-enabled opal-backend`
- [ ] Apache is serving files properly
- [ ] API endpoints work through Apache
- [ ] Daily backups are scheduled
- [ ] Can manually run backups
- [ ] Restore scripts are in place

---

**Total Time Estimate:** 50-70 minutes  
**Skill Level Required:** Linux system administrator  
**Rollback Time:** 5 minutes

---

## 📞 Need Help?

See detailed instructions in: `PRODUCTION_DEPLOYMENT_INSTRUCTIONS.md`

