# 🏃 Self-Hosted GitHub Runner Setup

## Why Use Self-Hosted Runner?

Instead of GitHub Actions connecting TO your server (blocked by firewall),
your server connects TO GitHub (allowed by firewall).

---

## 📋 Setup Steps

### Step 1: Go to GitHub Settings

1. Open: https://github.com/mayank145/OPAL/settings/actions/runners/new
2. Select: **Linux** and **x64**
3. You'll see commands like below

### Step 2: On Your Production Server

SSH into your server:
```bash
ssh root@133.40.149.66
```

### Step 3: Create Runner Directory
```bash
mkdir -p /opt/actions-runner
cd /opt/actions-runner
```

### Step 4: Download Runner
```bash
# Download
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
```

### Step 5: Configure Runner
```bash
# Get your registration token from GitHub
# Go to: https://github.com/mayank145/OPAL/settings/actions/runners/new

# Run config (replace TOKEN with the one from GitHub)
./config.sh --url https://github.com/mayank145/OPAL --token YOUR_TOKEN_HERE
```

**When prompted:**
- Runner group: `default` (press Enter)
- Runner name: `production-server` (or press Enter for hostname)
- Work folder: `_work` (press Enter)
- Run as service: `y` (type y and Enter)

### Step 6: Install and Start Service
```bash
# Install as service
sudo ./svc.sh install

# Start the runner
sudo ./svc.sh start

# Check status
sudo ./svc.sh status
```

---

## ✅ Verify Runner is Connected

1. Go to: https://github.com/mayank145/OPAL/settings/actions/runners
2. You should see your runner listed as **Active** (green dot)

---

## 🔧 Update Deployment Workflow

Now update the workflow to use your self-hosted runner:

```yaml
jobs:
  deploy:
    runs-on: self-hosted  # Changed from ubuntu-latest
```

---

## 🎯 Benefits

- ✅ No firewall changes needed
- ✅ Direct access to your server
- ✅ Faster deployments (no SSH)
- ✅ More secure
- ✅ Can run deployment scripts directly

---

## 🆘 Troubleshooting

### Runner not showing up?
```bash
cd /opt/actions-runner
sudo ./svc.sh status
sudo ./svc.sh start
```

### Need to remove runner?
```bash
cd /opt/actions-runner
sudo ./svc.sh stop
sudo ./svc.sh uninstall
./config.sh remove --token YOUR_TOKEN
```

---

**After setup, I'll update the workflow to use the self-hosted runner!**


