# 🔍 How to Get the Error Details

## Step 1: Go to GitHub Actions
Open: https://github.com/mayank145/OPAL/actions

## Step 2: Click on the Failed Run
- Look for the red ❌ "Enable auto-deployment" or latest workflow
- Click on it

## Step 3: Click on "deploy" Job
- You'll see a job called "deploy" with a red X
- Click on it

## Step 4: Click on "Deploy to Server" Step
- Expand the "Deploy to Server" section
- Look at the logs

## Step 5: Find the Error
Look for lines with:
- ❌ Error:
- failed
- exit code 1
- Cannot find
- Permission denied
- No such file or directory

## Copy the Error Message
**Copy the ENTIRE error section and send it to me**

Example of what to look for:
```
❌ Error: Project directory not found!
OR
bash: line 1: cd: /opt/OPAL/OPAL: No such file or directory
OR
fatal: not a git repository
OR
npm: command not found
```


