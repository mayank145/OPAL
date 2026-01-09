# 🔐 GitHub Secrets Setup Guide
## Enable Auto-Deployment for OPAL

---

## 📋 **What You Need**

To enable automatic deployment, you need to add **3 secrets** to your GitHub repository:

1. **PROD_SERVER_HOST** - Your production server IP
2. **PROD_SERVER_USER** - SSH username for the server
3. **PROD_SERVER_SSH_KEY** - Your SSH private key

---

## 🚀 **Step-by-Step Instructions**

### **Step 1: Go to GitHub Secrets Page**

Open this URL in your browser:
```
https://github.com/mayank145/OPAL/settings/secrets/actions
```

**Or navigate manually:**
1. Go to https://github.com/mayank145/OPAL
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)

---

### **Step 2: Add Secret #1 - Server Host**

1. Click the **"New repository secret"** button
2. Fill in:
   - **Name:** `PROD_SERVER_HOST`
   - **Value:** `133.40.149.66`
3. Click **"Add secret"**

✅ **Secret 1 added!**

---

### **Step 3: Add Secret #2 - Server User**

1. Click **"New repository secret"** again
2. Fill in:
   - **Name:** `PROD_SERVER_USER`
   - **Value:** `root`
3. Click **"Add secret"**

✅ **Secret 2 added!**

---

### **Step 4: Add Secret #3 - SSH Private Key**

1. Click **"New repository secret"** again
2. Fill in:
   - **Name:** `PROD_SERVER_SSH_KEY`
   - **Value:** Copy the ENTIRE private key below (including BEGIN and END lines)

**Your SSH Private Key:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDLkTIm3D64C7zVQOmvYOfYM5cLAb7wuPs5MVVEjL3xegAAAKAFAUBYBQFA
WAAAAAtzc2gtZWQyNTUxOQAAACDLkTIm3D64C7zVQOmvYOfYM5cLAb7wuPs5MVVEjL3xeg
AAAEDAPZbxYqhiFbOem+JmiJzsjcmiBQEaoGekPe++fzP4aMuRMibcPrgLvNVA6a9g59gz
lwsBvvC4+zkxVUSMvfF6AAAAHGNob3VkaGFyeW1heWFuazE0NUBnbWFpbC5jb20B
-----END OPENSSH PRIVATE KEY-----
```

**Important:** 
- Copy EVERYTHING from `-----BEGIN` to `-----END` (including those lines)
- Don't add extra spaces or newlines

3. Click **"Add secret"**

✅ **Secret 3 added!**

---

## ✅ **Step 5: Verify Secrets Are Added**

You should now see 3 secrets on the page:
- ✅ `PROD_SERVER_HOST`
- ✅ `PROD_SERVER_USER`
- ✅ `PROD_SERVER_SSH_KEY`

**Screenshot reference:**
```
Repository secrets (3)
├── PROD_SERVER_HOST ✓
├── PROD_SERVER_USER ✓
└── PROD_SERVER_SSH_KEY ✓
```

---

## 🔓 **Step 6: Enable Auto-Deployment**

Now that secrets are configured, we need to update the workflow file:

### **Option A: I'll do it for you**
Tell me "enable auto-deploy now" and I'll push the updated workflow.

### **Option B: Manual update**
Edit `.github/workflows/deploy-production.yml` and uncomment these lines:

**Change FROM:**
```yaml
on:
  workflow_dispatch:  # Manual trigger only
  # push:
  #   branches:
  #     - main
  #   tags:
  #     - 'v*'
```

**Change TO:**
```yaml
on:
  workflow_dispatch:  # Manual trigger
  push:
    branches:
      - main
    tags:
      - 'v*'
```

Then commit and push:
```bash
git add .github/workflows/deploy-production.yml
git commit -m "Enable auto-deployment with configured secrets"
git push origin main
```

---

## 🎯 **What Happens After Enabling?**

### **Automatic Deployment Workflow:**

```
1. You push code to main branch
   ↓
2. GitHub runs CI/CD tests
   ├── Backend tests (6 tests)
   └── Frontend tests
   ↓
3. If tests pass ✅
   ↓
4. GitHub automatically deploys to production
   ├── SSH into 133.40.149.66
   ├── Pull latest code
   ├── Update backend (pip install)
   ├── Build frontend (npm run build)
   ├── Restart services
   └── Verify deployment
   ↓
5. Deployment complete! 🎉
```

---

## 🔒 **Security Notes**

### **Are My Secrets Safe?**
✅ **YES!** GitHub encrypts all secrets
- Only GitHub Actions can access them
- They never appear in logs
- Repository collaborators can't view them
- Even you can't view them after adding (only update/delete)

### **SSH Key Security**
✅ **Safe to use:**
- The key is encrypted in GitHub
- Only used during deployment
- Transmitted securely over SSH

### **Best Practices:**
- ✅ Use a dedicated deployment key (optional)
- ✅ Limit SSH key to specific commands (optional)
- ✅ Monitor deployment logs regularly
- ✅ Rotate keys periodically (every 6-12 months)

---

## 🧪 **Test Auto-Deployment**

After enabling, test it:

1. Make a small change (e.g., update a comment in code)
2. Commit and push to main
3. Go to: https://github.com/mayank145/OPAL/actions
4. Watch the deployment workflow run
5. Verify on production server

---

## 🆘 **Troubleshooting**

### **Deployment Fails with "Permission denied"**
- Check that SSH key is correct
- Verify the key has proper line breaks
- Ensure server accepts this key

### **Deployment Fails with "Host key verification failed"**
- Add `StrictHostKeyChecking=no` to SSH action (not recommended for production)
- Or add server to known_hosts

### **Services Don't Restart**
- Check if `root` user has sudo permissions (shouldn't need sudo if running as root)
- Verify systemd services exist on server

---

## 📋 **Quick Checklist**

Before enabling auto-deploy, ensure:
- [ ] All 3 secrets added to GitHub
- [ ] SSH key works (test with: `ssh root@133.40.149.66`)
- [ ] Production server is accessible
- [ ] Systemd services exist (`opal-backend`, `httpd`)
- [ ] Project path is correct (`/opt/OPAL/opal-unified`)
- [ ] CI/CD tests are passing

---

## 🎉 **Ready to Enable?**

Once you've added all 3 secrets, tell me:
- **"Enable auto-deploy now"** - I'll update and push the workflow
- **"Test deployment manually first"** - I'll help you test via workflow_dispatch
- **"Wait, I have questions"** - Ask away!

---

**Last Updated:** December 23, 2025  
**Status:** Secrets guide ready  
**Next Step:** Add secrets to GitHub, then enable auto-deploy


