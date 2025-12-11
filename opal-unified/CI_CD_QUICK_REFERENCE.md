# CI/CD Quick Reference Card

## 🚀 Quick Start (3 Steps)

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Your message"
git push origin main
```

### 2. CI Runs Automatically
- ✅ Tests run
- ✅ Code checked
- ✅ Build created

### 3. CD Deploys Automatically (if tests pass)
- 🚀 Deployed to VM
- 🏥 Health checked
- ✅ Live

---

## 📋 Daily Workflow

```bash
# Morning: Start work
git checkout -b feature/my-feature

# During: Make changes
# ... edit files ...
pytest                  # Test locally
git commit -m "..."

# End of day: Push
git push origin feature/my-feature

# Create PR on GitHub
# Wait for CI ✅
# Merge → Auto-deploys 🚀
```

---

## ⚠️ CRITICAL RULES

### ❌ NEVER Do:
```
❌ Commit passwords/secrets
❌ Push directly to main
❌ Force push (git push -f)
❌ Skip tests
❌ Deploy on Friday evening
❌ Change database without backup
```

### ✅ ALWAYS Do:
```
✅ Run tests before committing
✅ Use pull requests
✅ Backup before database changes
✅ Check CI status before merge
✅ Monitor after deployment
✅ Have rollback plan
```

---

## 🔐 Security Checklist

Before every commit:
```
☐ No passwords in code
☐ No API keys in code
☐ .env is in .gitignore
☐ Secrets use environment variables
☐ Dependencies updated
```

---

## 🚨 Emergency Procedures

### Rollback Deployment
```bash
# Option 1: Git revert
git revert HEAD
git push origin main

# Option 2: Restore backup
ssh root@opalfailover
cd /opt/OPAL/opal-unified
tar -xzf backup-latest.tar.gz
# Restart services
```

### Check System Health
```bash
# Backend
curl http://opalfailover:8000/health

# Frontend
curl http://opalfailover:3000

# Logs
ssh root@opalfailover
tail -f /tmp/backend.log
tail -f /tmp/frontend.log
```

---

## 📊 CI/CD Pipeline Status

### Check Pipeline
```
GitHub → Actions tab

Green ✅ = All good
Red ❌ = Something broke (check logs)
Yellow ⚠️ = Running
```

### Common Errors
```
"Tests failed" → Run pytest locally
"Build failed" → Check syntax errors
"Deployment failed" → Check SSH keys
"Health check failed" → Check VM services
```

---

## 🔧 Troubleshooting

### Tests Fail in CI (but pass locally)
```bash
# Check versions match:
python --version  # Should be 3.11
node --version    # Should be 18.x

# Update requirements:
pip freeze > backend/requirements.txt
```

### Deployment Hangs
```bash
# Check VM is accessible:
ssh root@opalfailover

# Check disk space:
df -h

# Check running processes:
ps aux | grep uvicorn
ps aux | grep node
```

### Services Won't Start
```bash
# Backend:
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --reload  # Manual start

# Frontend:
cd /opt/OPAL/opal-unified/frontend
npm start  # Manual start
```

---

## 📞 Who to Contact

### Issue Types
```
CI/CD Pipeline Issues → DevOps Team
Code Review Needed → Team Lead
Deployment Failed → System Admin
Security Concern → Security Team
```

---

## 🎯 Key Metrics

### Good Pipeline
```
✅ Tests run in < 5 minutes
✅ Deployment takes < 10 minutes
✅ Success rate > 95%
✅ Zero downtime deployments
```

### Warning Signs
```
⚠️ Tests taking > 10 minutes
⚠️ Deployment taking > 20 minutes
⚠️ Multiple failures per day
⚠️ Manual interventions needed
```

---

## 📚 Resources

- Full Guide: `CI_CD_SETUP_GUIDE.md`
- GitHub Actions: https://github.com/YOUR_REPO/actions
- VM Access: `ssh root@opalfailover`
- Health Check: http://opalfailover:8000/health

---

**Remember:**
- CI/CD is your safety net
- Red builds are learning opportunities
- When in doubt, rollback
- Test locally before pushing
- Communicate with your team

---

_Last Updated: $(date)_

