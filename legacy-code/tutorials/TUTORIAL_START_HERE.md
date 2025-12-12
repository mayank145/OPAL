# OPAL Modernization - Step-by-Step Tutorial
## Learn by Building from Scratch

**Welcome!** This tutorial will guide you through building the modern OPAL system from the ground up. Each step includes:
- ✅ What we're building
- 🎯 Why we're doing it
- 📝 Commands to run
- 🧪 How to test it works
- 💡 Things to learn

**Time Commitment**: 40-50 hours over 4-6 weeks  
**Difficulty**: Beginner to Intermediate  
**Prerequisites**: Basic command line knowledge

---

## 📚 Tutorial Structure

### Phase 1: Environment Setup (Week 1)
- **Lesson 1**: Install Required Software
- **Lesson 2**: Create Project Structure
- **Lesson 3**: Setup Version Control (Git)

### Phase 2: Backend Basics (Week 1-2)
- **Lesson 4**: Hello World with FastAPI
- **Lesson 5**: Database Connection (PostgreSQL)
- **Lesson 6**: First API Endpoint
- **Lesson 7**: Data Models with SQLAlchemy
- **Lesson 8**: CRUD Operations

### Phase 3: Authentication (Week 2-3)
- **Lesson 9**: User Registration
- **Lesson 10**: Login with JWT
- **Lesson 11**: Protected Routes
- **Lesson 12**: LDAP Integration

### Phase 4: Real Features (Week 3-4)
- **Lesson 13**: Summit Log System
- **Lesson 14**: Car Reservation System
- **Lesson 15**: User Management

### Phase 5: Frontend Basics (Week 4-5)
- **Lesson 16**: React Setup with Vite
- **Lesson 17**: First Component
- **Lesson 18**: Routing with React Router
- **Lesson 19**: API Integration
- **Lesson 20**: Material-UI Components

### Phase 6: Full Stack Integration (Week 5-6)
- **Lesson 21**: Login Flow (Frontend + Backend)
- **Lesson 22**: Dashboard Page
- **Lesson 23**: Forms with React Hook Form
- **Lesson 24**: Real-time Updates

### Phase 7: Advanced Topics (Week 6+)
- **Lesson 25**: Background Tasks with Celery
- **Lesson 26**: Docker Containerization
- **Lesson 27**: Testing
- **Lesson 28**: Deployment

---

## 🎓 How to Use This Tutorial

### Your Learning Path:
1. **Read each lesson completely** before starting
2. **Execute each command** yourself (don't copy-paste blindly)
3. **Verify each step works** before moving forward
4. **Experiment!** Try changing things to see what happens
5. **Ask questions** (make notes of what you don't understand)

### Tutorial Format:
Each lesson has:
```
📖 Lesson X: Topic Name
├── 🎯 Learning Goals (what you'll learn)
├── 📝 Instructions (step-by-step)
├── 💻 Code to Write (you'll type this)
├── 🧪 Testing (verify it works)
├── 🐛 Troubleshooting (if something breaks)
└── 🚀 Next Steps (what's coming)
```

---

## ⚠️ IMPORTANT: Start Here

### Before You Begin:

1. ✅ **Read MODERNIZATION_README.md** - Understand the big picture
2. ✅ **Read TECH_STACK.md** - Know what technologies we're using
3. ✅ **Create a learning journal** - Take notes as you go
4. ✅ **Set aside dedicated time** - 1-2 hours per lesson
5. ✅ **Don't rush** - Understanding is more important than speed

### Learning Philosophy:

> "I hear and I forget. I see and I remember. I do and I understand." - Confucius

This tutorial follows the principle of **active learning**:
- You will **type every line** of code
- You will **break things** (and fix them!)
- You will **make mistakes** (that's good!)
- You will **understand WHY**, not just HOW

---

## 🚀 LESSON 1: Install Required Software

### 🎯 Learning Goals
- Understand what each tool does
- Install Python, Node.js, Docker
- Verify installations work
- Setup a proper development environment

### 📚 Background

Before we write any code, we need to install the tools. Think of this like setting up a workshop before building furniture:

**Tools We Need:**
1. **Python 3.11+** - Backend programming language
2. **Node.js 20+** - Frontend tooling and package management
3. **Docker** - Run databases and services
4. **Git** - Version control
5. **VS Code** - Code editor (recommended)

---

### 📝 Step 1.1: Check What's Already Installed

Open your terminal and run these commands:

```bash
# Check Python version
python3 --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Docker version
docker --version

# Check Git version
git --version
```

**🧪 Expected Results:**
- Python: 3.11 or higher
- Node: 20.x or higher
- npm: 10.x or higher
- Docker: 24.x or higher
- Git: 2.x or higher

**💡 What you're learning:**
- The `--version` flag shows installed versions
- These tools need to be in your system PATH
- If a command fails, that tool isn't installed

---

### 📝 Step 1.2: Install Python 3.11 (if needed)

**On macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify installation
python3.11 --version
```

**On Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Verify in Command Prompt: `python --version`

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3.11 --version
```

**🧪 Test it works:**
```bash
python3.11 -c "print('Hello, Python!')"
```
You should see: `Hello, Python!`

**💡 What you're learning:**
- Python is the language for our backend API
- We need 3.11+ for modern features (type hints, performance)
- `-c` flag runs a single Python command

---

### 📝 Step 1.3: Install Node.js 20

**On macOS:**
```bash
# Using Homebrew
brew install node@20

# Verify
node --version
npm --version
```

**On Windows:**
1. Download from https://nodejs.org/
2. Install the LTS version (20.x)
3. Verify in Command Prompt: `node --version`

**On Linux:**
```bash
# Using NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
npm --version
```

**🧪 Test it works:**
```bash
node -e "console.log('Hello, Node.js!')"
```
You should see: `Hello, Node.js!`

**💡 What you're learning:**
- Node.js runs JavaScript outside the browser
- npm is Node's package manager (like pip for Python)
- We use Node.js for frontend development tools

---

### 📝 Step 1.4: Install Docker Desktop

**On macOS:**
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install the .dmg file
3. Open Docker Desktop
4. Wait for it to start (whale icon in menu bar)

**On Windows:**
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install
3. Enable WSL 2 if prompted
4. Start Docker Desktop

**On Linux:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

**🧪 Test it works:**
```bash
# This should NOT require sudo
docker run hello-world
```

You should see a welcome message from Docker.

**💡 What you're learning:**
- Docker runs isolated containers
- Each container is like a mini-computer
- We'll use Docker for PostgreSQL and Redis
- `docker run` downloads and runs a container

---

### 📝 Step 1.5: Install Git

**On macOS:**
```bash
# Usually already installed, but you can update via Homebrew
brew install git
```

**On Windows:**
1. Download from https://git-scm.com/download/win
2. Install with default options
3. Open "Git Bash" from Start menu

**On Linux:**
```bash
sudo apt install git
```

**Configure Git (First Time Only):**
```bash
# Set your name (this will appear in commits)
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Check configuration
git config --list
```

**🧪 Test it works:**
```bash
git --version
```

**💡 What you're learning:**
- Git tracks changes to your code
- Configuration is stored globally (`--global` flag)
- Every commit is tagged with your name and email

---

### 📝 Step 1.6: Install VS Code (Recommended)

**Download:** https://code.visualstudio.com/

**After installation, install these extensions:**

1. Open VS Code
2. Click Extensions icon (or press Cmd+Shift+X / Ctrl+Shift+X)
3. Search and install:
   - `Python` (by Microsoft)
   - `Pylance` (Python language server)
   - `ESLint` (JavaScript/TypeScript linting)
   - `Prettier` (Code formatter)
   - `Docker` (Docker support)
   - `GitLens` (Git integration)
   - `Thunder Client` (API testing)

**🧪 Test it works:**
1. Open VS Code
2. Open terminal in VS Code (View → Terminal)
3. Run: `python3 --version`
4. Run: `node --version`

**💡 What you're learning:**
- VS Code is a powerful, free code editor
- Extensions add functionality
- Integrated terminal is convenient for running commands

---

### 📝 Step 1.7: Setup Your Workspace

**Create your project directory:**

```bash
# Navigate to where you want your project
cd ~/Desktop

# Create project directory
mkdir opal-modernization
cd opal-modernization

# Create a README
echo "# OPAL Modernization Project" > README.md

# Verify you're in the right place
pwd
# Should show: /Users/yourname/Desktop/opal-modernization (or similar)
```

**Open in VS Code:**
```bash
# Open current directory in VS Code
code .
```

**💡 What you're learning:**
- `mkdir` creates directories
- `cd` changes directories
- `pwd` prints working directory
- `code .` opens current directory in VS Code

---

### 🧪 LESSON 1 CHECKPOINT

Before moving to Lesson 2, verify EVERYTHING works:

**Run this complete test:**
```bash
# Test Python
python3.11 --version

# Test Node
node --version
npm --version

# Test Docker
docker --version
docker ps  # Should show running containers (probably none)

# Test Git
git --version
git config user.name  # Should show your name

# Create a test file
echo "console.log('Test');" > test.js
node test.js  # Should print: Test
rm test.js  # Clean up
```

**✅ All commands should work without errors!**

If anything failed, go back and fix it before continuing.

---

### 🐛 Common Issues and Solutions

**Issue 1: "command not found"**
- **Problem**: Tool not installed or not in PATH
- **Solution**: Reinstall and check PATH settings

**Issue 2: "Permission denied" (Docker on Linux)**
- **Problem**: User not in docker group
- **Solution**: Run `sudo usermod -aG docker $USER`, then log out and back in

**Issue 3: Python shows 2.7 or wrong version**
- **Problem**: Multiple Python versions installed
- **Solution**: Use `python3.11` explicitly, or create an alias

**Issue 4: Docker won't start**
- **Problem**: Docker Desktop not running (Mac/Windows)
- **Solution**: Start Docker Desktop application

---

### 📝 Your Learning Journal - Lesson 1

Take a moment to write down:

1. **What I learned:**
   - (Write 3-5 things you learned)

2. **What confused me:**
   - (Write down anything unclear)

3. **Questions I have:**
   - (Write questions to research later)

4. **Commands I want to remember:**
   ```bash
   # Your important commands here
   ```

---

### 🚀 What's Next?

In **Lesson 2**, you'll:
- Create the project structure
- Setup separate backend and frontend directories
- Initialize Git repository
- Create virtual environments
- Understand project organization

**Estimated Time**: 30 minutes

---

## 🎯 Ready for Lesson 2?

Before continuing, make sure:
- ✅ All software is installed
- ✅ All test commands work
- ✅ VS Code is setup with extensions
- ✅ You understand what each tool does
- ✅ You've made notes in your learning journal

**When you're ready, proceed to [LESSON 2: Project Structure](./LESSON_02_PROJECT_STRUCTURE.md)**

---

## 💬 Learning Tips

### Good Habits to Develop:
1. **Read error messages carefully** - They usually tell you what's wrong
2. **Google errors** - Someone else has probably solved it
3. **Take breaks** - Your brain needs time to process
4. **Experiment** - Try changing things to see what happens
5. **Don't memorize** - Understand concepts, look up syntax

### When You Get Stuck:
1. Read the error message completely
2. Check you typed commands correctly
3. Google the error message
4. Check official documentation
5. Take a break and come back later

### Resources:
- Python docs: https://docs.python.org/3/
- Node.js docs: https://nodejs.org/docs/
- Docker docs: https://docs.docker.com/
- Git docs: https://git-scm.com/doc

---

**Remember**: The goal isn't to finish quickly. The goal is to **understand** what you're building! 🎓

Take your time, experiment, break things, and learn!

---

**Next Lesson**: [Lesson 2: Project Structure](./LESSON_02_PROJECT_STRUCTURE.md)

**Document Version**: 1.0  
**Last Updated**: October 8, 2025

