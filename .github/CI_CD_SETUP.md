# CI/CD Setup Guide for OPAL FATS

## 📋 Overview

This repository has GitHub Actions workflows for automated testing and deployment.

## 🔄 Workflows

### 1. Backend CI (`backend-ci.yml`)
**Triggers:** Push/PR to main/master that affects `backend/` files
**Actions:**
- Sets up Python 3.9
- Installs dependencies
- Runs pytest tests
- Lints code with flake8

### 2. Frontend CI (`frontend-ci.yml`)
**Triggers:** Push/PR to main/master that affects `frontend/` files
**Actions:**
- Sets up Node.js 16
- Installs dependencies
- Runs React tests with coverage
- Builds production bundle
- Lints code

### 3. Production Deployment (`deploy-production.yml`)
**Triggers:** 
- Manual trigger via GitHub Actions UI
- Push to `main` branch
- Version tags (e.g., `v1.0.0`)

**Actions:**
- SSHs into production server
- Pulls latest code
- Updates backend dependencies
- Rebuilds frontend
- Restarts services
- Verifies deployment

## 🔐 Required GitHub Secrets

To enable auto-deployment, add these secrets to your GitHub repository:

1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Add these secrets:

| Secret Name | Description | Value |
|------------|-------------|--------|
| `PROD_SERVER_HOST` | Production server IP | `133.40.149.66` |
| `PROD_SERVER_USER` | SSH username | `root` |
| `PROD_SERVER_SSH_KEY` | Private SSH key | (Your SSH private key) |

### How to get SSH private key:
```bash
# On production server
cat ~/.ssh/id_ed25519
```

Copy the entire output (including BEGIN and END lines) to the `PROD_SERVER_SSH_KEY` secret.

## 🚀 Manual Deployment from GitHub

1. Go to your repository on GitHub
2. Click `Actions` tab
3. Select `Deploy to Production`
4. Click `Run workflow`
5. Select branch and click `Run workflow`

## ✅ Workflow Status Badges

Add these to your `README.md`:

```markdown
![Backend CI](https://github.com/mayank145/OPAL/workflows/Backend%20CI/badge.svg)
![Frontend CI](https://github.com/mayank145/OPAL/workflows/Frontend%20CI/badge.svg)
```

## 📝 Current Status

- ✅ CI/CD workflows created locally
- ⏳ Needs to be pushed to GitHub
- ⏳ GitHub Secrets need to be configured
- ⏳ First workflow run pending

## 🔧 Next Steps

1. **Commit and push the workflows:**
   ```bash
   cd /opt/OPAL/opal-unified
   git add .github/workflows/
   git commit -m "Add CI/CD workflows for automated testing and deployment"
   git push origin main
   ```

2. **Configure GitHub Secrets** (see above)

3. **Test the workflows:**
   - Make a small change and push
   - Check the Actions tab on GitHub
   - Workflows should run automatically

4. **Enable branch protection:**
   - Require CI to pass before merging
   - Require code reviews

## 🎯 Benefits

- ✅ Automated testing on every push
- ✅ Catch bugs before deployment
- ✅ One-click production deployment
- ✅ Consistent build process
- ✅ Deployment verification
- ✅ Rollback capability with git tags

## 🐛 Troubleshooting

**Workflows not running?**
- Check the `.github/workflows/` files are in the main branch
- Verify branch names match (main vs master)

**Deployment failing?**
- Check GitHub Secrets are configured
- Verify SSH key has proper permissions
- Check server logs: `journalctl -u opal-backend -f`

**Tests failing?**
- Run tests locally first: `cd backend && pytest`
- Check database connection in CI
- Verify all environment variables are set

