================================================================================
OPAL FATS - PRODUCTION DEPLOYMENT & BACKUP CONFIGURATION
================================================================================

Created: December 5, 2025
For: System Administrator
Server: 133.40.149.66
Time Required: 60-85 minutes

================================================================================
IMPORTANT: READ THIS FIRST
================================================================================

This package contains complete instructions for deploying OPAL FATS in
production mode with automated backups.

Current Status: Development mode (running on ports 3000 and 8000)
Target Status: Production mode (port 80, systemd services, automated backups)

================================================================================
FILES IN THIS PACKAGE
================================================================================

1. DEPLOYMENT_SUMMARY_FOR_ADMIN.md [START HERE]
   - Overview of the entire deployment
   - Pre-deployment checks
   - Time estimates and requirements
   - Success criteria

2. PRODUCTION_DEPLOYMENT_INSTRUCTIONS.md [MAIN GUIDE]
   - Complete step-by-step instructions
   - All configuration files included
   - Backup setup instructions
   - Troubleshooting guide
   - This is the detailed guide - follow this!

3. QUICK_DEPLOYMENT_CHECKLIST.md [QUICK REFERENCE]
   - Fast checklist format
   - Quick commands
   - Emergency rollback procedure
   - Use this alongside the main guide

4. This file (DEPLOYMENT_FILES_README.txt)
   - You're reading it now!

================================================================================
GETTING STARTED
================================================================================

Step 1: Read DEPLOYMENT_SUMMARY_FOR_ADMIN.md
        - Understand what will be deployed
        - Check time requirements
        - Verify prerequisites

Step 2: Run pre-deployment checks from the summary file
        - Verify you have root access
        - Check Apache is running
        - Confirm database is accessible
        - Verify disk space

Step 3: Follow PRODUCTION_DEPLOYMENT_INSTRUCTIONS.md
        - Part 1: Production Deployment (30-40 min)
        - Part 2: Backup Configuration (20-30 min)
        - Use QUICK_DEPLOYMENT_CHECKLIST.md as reference

Step 4: Verify everything works
        - Access http://133.40.149.66/
        - Test all features
        - Verify backups are running
        - Check logs

================================================================================
QUICK ACCESS (AFTER DEPLOYMENT)
================================================================================

Main Application:    http://133.40.149.66/
API Documentation:   http://133.40.149.66/docs
Health Check:        http://133.40.149.66/health

Logs:
  Backend:  /opt/OPAL/opal-unified/backend/logs/backend.log
  Apache:   /var/log/httpd/opal-fats-error.log
  Backups:  /opt/backups/opal-fats/backup.log

Commands:
  systemctl status opal-backend    # Check backend service
  systemctl restart httpd          # Restart Apache
  /opt/backups/opal-fats/backup-all.sh    # Manual backup

================================================================================
WHAT GETS DEPLOYED
================================================================================

✅ Backend as systemd service (auto-starts on boot)
✅ Frontend production build (optimized React app)
✅ Apache reverse proxy (professional web server)
✅ Security hardening (DEBUG=false, firewall, CORS)
✅ Automated daily backups (database + files at 2:00 AM)
✅ Backup retention (keeps last 7 days)
✅ Restore scripts (easy recovery)

================================================================================
SUPPORT
================================================================================

All documentation is self-contained in the instruction files.

For issues:
  1. Check the "Troubleshooting" section in the main instructions
  2. Review logs (locations listed above)
  3. Use the "Emergency Procedures" in the summary document

================================================================================
IMPORTANT NOTES
================================================================================

⚠️  This will stop the current development servers
⚠️  Run a manual backup before starting deployment
⚠️  Choose a low-traffic time for deployment
⚠️  Test thoroughly after deployment
⚠️  Keep these instructions for future reference

✅  Complete rollback procedure included if needed
✅  No data will be lost (database already has 1454 FATS entries)
✅  All scripts are tested and production-ready

================================================================================
QUESTIONS?
================================================================================

Everything you need is in the instruction files:
  - Detailed steps
  - Configuration examples
  - Troubleshooting guides
  - Emergency procedures

Read DEPLOYMENT_SUMMARY_FOR_ADMIN.md first!

================================================================================
Good luck with the deployment!
================================================================================

