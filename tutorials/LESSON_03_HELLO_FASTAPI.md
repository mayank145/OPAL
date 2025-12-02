# LESSON 3: Hello World with FastAPI
## Your First Web API

**Estimated Time**: 30-45 minutes  
**Difficulty**: Beginner  
**Prerequisites**: Lesson 1 & 2 completed

---

## 🎯 Learning Goals

By the end of this lesson, you will:
- Create your first FastAPI application
- Write a simple API endpoint
- Run a development web server
- Test your API in a browser
- Understand how web APIs work
- Use automatic API documentation

---

## 📚 Background: What is an API?

**API = Application Programming Interface**

Think of an API like a restaurant:
- 🍽️ **Restaurant Menu** = API endpoints (what you can order)
- 👨‍🍳 **Kitchen** = Your backend code (prepares the food)
- 🚪 **Waiter** = HTTP protocol (delivers requests/responses)
- 🍕 **Food** = Data (JSON response)

**Example:**
```
You (browser): "GET /api/pizza"
API: "Here's your pizza data: {name: 'Margherita', price: 12}"
```

**FastAPI** is a modern Python framework for building APIs quickly and easily.

**Why FastAPI?**
- ✅ Fast to write code
- ✅ Fast performance (async)
- ✅ Automatic documentation
- ✅ Type safety
- ✅ Easy to learn

---

## 📝 Step 3.1: Navigate to Your Project

Let's get to your backend directory and activate the virtual environment.

```bash
# Navigate to your project
cd ~/Desktop/opal-v2/backend

# Activate virtual environment
source venv/bin/activate
# On Windows: venv\Scripts\activate

# Your prompt should show (venv)
```

**🧪 Verify you're in the right place:**
```bash
pwd
# Should show: /Users/yourname/Desktop/opal-v2/backend

ls -la
# Should show: app/, venv/, requirements.txt, etc.

which python
# Should show path inside venv/
```

**💡 What you're learning:**
- Always activate venv before working
- Check your location with `pwd`
- Virtual environment keeps packages isolated

---

## 📝 Step 3.2: Create Your First FastAPI File

Let's create the main application file:

```bash
# Make sure you're in backend/ with venv activated

# Create main.py in the app directory
cat > app/main.py << 'EOF'
"""
OPAL API - Main Application
This is the entry point for our FastAPI application.
"""

from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="OPAL API",
    description="Modern Observatory Planning and Logging System",
    version="0.1.0"
)


# Root endpoint - returns a welcome message
@app.get("/")
def read_root():
    """
    Welcome endpoint
    Returns a simple greeting message
    """
    return {
        "message": "Welcome to OPAL API",
        "version": "0.1.0",
        "status": "running"
    }


# Health check endpoint - useful for monitoring
@app.get("/health")
def health_check():
    """
    Health check endpoint
    Returns the API health status
    """
    return {
        "status": "healthy",
        "service": "OPAL API"
    }
EOF

# View what you created
cat app/main.py
```

**💡 What you're learning:**

**Line-by-line explanation:**

1. **`from fastapi import FastAPI`**
   - Import the FastAPI class
   - This is the core of our API

2. **`app = FastAPI(...)`**
   - Create an instance of FastAPI
   - `title`, `description`, `version` = metadata for documentation
   - `app` is the main application object

3. **`@app.get("/")`**
   - This is a **decorator** (starts with @)
   - Tells FastAPI: "When someone visits `/`, run this function"
   - `get` = HTTP GET method (retrieving data)
   - `"/"` = the URL path (root)

4. **`def read_root():`**
   - A normal Python function
   - FastAPI will call this when someone visits "/"

5. **`return {...}`**
   - Returns a Python dictionary
   - FastAPI automatically converts to JSON

**HTTP Methods Quick Guide:**
- **GET** = Read data (like visiting a webpage)
- **POST** = Create new data
- **PUT** = Update existing data
- **DELETE** = Remove data

---

## 📝 Step 3.3: Create __init__.py Files

Python needs special `__init__.py` files to recognize directories as packages.

```bash
# Still in backend/ directory

# Create __init__.py in app/
touch app/__init__.py

# Create __init__.py in app/api/
touch app/api/__init__.py

# Verify they exist
ls app/
ls app/api/
```

**💡 What you're learning:**
- `__init__.py` makes a directory a Python package
- Can be empty (which is fine for now)
- Allows Python to import from these directories
- `touch` creates an empty file

---

## 📝 Step 3.4: Run Your API!

Time to see your API in action! This is exciting! 🚀

```bash
# Make sure you're in backend/ with venv activated
# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see output like:**
```
INFO:     Will watch for changes in these directories: ['/Users/yourname/Desktop/opal-v2/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**🎉 Congratulations! Your API is running!**

**💡 What you're learning:**

**Command breakdown:**
- `uvicorn` = ASGI web server (runs your API)
- `app.main:app` = "in the app.main module, use the app object"
  - `app.main` = file at app/main.py
  - `:app` = the variable named `app`
- `--reload` = Auto-restart when code changes (development only)
- `--host 0.0.0.0` = Listen on all network interfaces
- `--port 8000` = Use port 8000

**What's happening:**
1. Uvicorn starts a web server
2. Loads your FastAPI app
3. Listens for incoming HTTP requests
4. Routes requests to your functions
5. Returns responses

---

## 📝 Step 3.5: Test Your API in Browser

**Don't close the terminal where uvicorn is running!** Open a new browser window.

### Test 1: Root Endpoint

**Open in browser:**
```
http://localhost:8000/
```

**You should see:**
```json
{
  "message": "Welcome to OPAL API",
  "version": "0.1.0",
  "status": "running"
}
```

**🎉 IT WORKS!** You just made your first API call!

### Test 2: Health Check

**Open in browser:**
```
http://localhost:8000/health
```

**You should see:**
```json
{
  "status": "healthy",
  "service": "OPAL API"
}
```

**💡 What you're learning:**
- `localhost` = your own computer
- `8000` = the port number
- `/` and `/health` = different endpoints
- Browser makes a GET request
- FastAPI returns JSON automatically

---

## 📝 Step 3.6: Explore Automatic Documentation

FastAPI automatically generates interactive documentation! 🤯

### Swagger UI (Interactive API Docs)

**Open in browser:**
```
http://localhost:8000/docs
```

**What you'll see:**
- List of all your endpoints
- Click any endpoint to expand it
- Click "Try it out" button
- Click "Execute" to test it
- See the response!

**Try it:**
1. Click on `GET /`
2. Click "Try it out"
3. Click "Execute"
4. See the response below!

### ReDoc (Alternative Documentation)

**Open in browser:**
```
http://localhost:8000/redoc
```

This is a different style of documentation - more like reading a manual.

**💡 What you're learning:**
- FastAPI generates docs automatically
- `/docs` = Swagger UI (interactive)
- `/redoc` = ReDoc (documentation style)
- No extra work needed!
- This is why FastAPI is awesome!

---

## 📝 Step 3.7: Add Another Endpoint

Let's add a new endpoint while the server is running!

**In a NEW terminal window:**

```bash
# Navigate to backend
cd ~/Desktop/opal-v2/backend

# Open main.py in VS Code
code app/main.py
```

**Add this new endpoint at the bottom of the file:**

```python
# Add this BEFORE the end of the file

@app.get("/api/test")
def test_endpoint():
    """
    Test endpoint for learning
    Returns a test message
    """
    return {
        "message": "This is a test endpoint",
        "tip": "You can add as many endpoints as you want!",
        "learn": "Each endpoint is just a Python function"
    }
```

**Save the file (Cmd+S or Ctrl+S)**

**💡 What you're learning:**
- You can have multiple endpoints
- Each endpoint is a separate function
- Add them anywhere in the file
- The decorator (`@app.get`) tells FastAPI about them

---

## 📝 Step 3.8: Watch Auto-Reload in Action

**Go back to the terminal where uvicorn is running.**

You should see:
```
INFO:     Detected file change in 'app/main.py'. Reloading...
INFO:     Started reloader process [12347] using WatchFiles
INFO:     Application startup complete.
```

**The server automatically reloaded!** 🎉

**Now test your new endpoint in browser:**
```
http://localhost:8000/api/test
```

**You should see your new response!**

Also check:
```
http://localhost:8000/docs
```

Your new endpoint appears in the documentation automatically!

**💡 What you're learning:**
- `--reload` watches for file changes
- Auto-reloads when you save
- No need to manually restart
- Great for development!

---

## 📝 Step 3.9: Understanding the Code

Let's break down what's happening:

```python
from fastapi import FastAPI
```
- Import the FastAPI class

```python
app = FastAPI(title="OPAL API", ...)
```
- Create your application
- `app` is the main object
- All endpoints attach to this

```python
@app.get("/")
```
- **Decorator** - modifies the function below it
- `@app.get` = register a GET endpoint
- `"/"` = the URL path
- Runs before the function definition

```python
def read_root():
    return {"message": "Hello"}
```
- Normal Python function
- FastAPI calls it when endpoint is accessed
- Return value becomes the HTTP response
- Dictionary → JSON automatically

**Request Flow:**
```
Browser → HTTP GET /
    ↓
FastAPI receives request
    ↓
FastAPI finds matching endpoint
    ↓
Calls read_root() function
    ↓
Function returns dictionary
    ↓
FastAPI converts to JSON
    ↓
Sends HTTP response to browser
```

---

## 📝 Step 3.10: Add a Dynamic Endpoint

Let's make an endpoint that accepts parameters!

**Add this to app/main.py:**

```python
@app.get("/api/greet/{name}")
def greet_user(name: str):
    """
    Greet a user by name
    Path parameter: name
    """
    return {
        "message": f"Hello, {name}!",
        "greeting": "Welcome to OPAL",
        "your_name": name
    }
```

**Save the file and test:**

```
http://localhost:8000/api/greet/Mayank
```

**You should see:**
```json
{
  "message": "Hello, Mayank!",
  "greeting": "Welcome to OPAL",
  "your_name": "Mayank"
}

```

**Try different names:**
```
http://localhost:8000/api/greet/Alice
http://localhost:8000/api/greet/Bob
http://localhost:8000/api/greet/YourName
```

**💡 What you're learning:**

- `{name}` in path = path parameter (variable)
- `name: str` = type hint (must be a string)
- FastAPI extracts the value automatically
- `f"Hello, {name}!"` = f-string (formatted string)
- One function handles all names!

---

## 📝 Step 3.11: Add Query Parameters

Query parameters are different - they come after `?` in the URL.

**Add this endpoint:**

```python
@app.get("/api/calculate")
def calculate(x: int, y: int, operation: str = "add"):
    """
    Simple calculator
    Query parameters: x, y, operation
    """
    if operation == "add":
        result = x + y
    elif operation == "subtract":
        result = x - y
    elif operation == "multiply":
        result = x * y
    elif operation == "divide":
        result = x / y if y != 0 else "Cannot divide by zero"
    else:
        result = "Unknown operation"
    
    return {
        "x": x,
        "y": y,
        "operation": operation,
        "result": result
    }
```

**Save and test:**

```
http://localhost:8000/api/calculate?x=10&y=5&operation=add
http://localhost:8000/api/calculate?x=10&y=5&operation=multiply
http://localhost:8000/api/calculate?x=20&y=4&operation=divide
```

**💡 What you're learning:**

- Query parameters come after `?` in URL
- Separate multiple with `&`
- Format: `?key=value&key2=value2`
- FastAPI extracts them automatically
- `operation: str = "add"` = default value
- Type hints: `x: int` (FastAPI validates!)

**Try this (should fail):**
```
http://localhost:8000/api/calculate?x=hello&y=5
```

FastAPI returns an error because "hello" isn't an integer! ✅

---

## 🧪 LESSON 3 CHECKPOINT

Let's verify everything works!

### Running Server ✅
- [ ] Uvicorn is running (terminal shows "Application startup complete")
- [ ] No error messages in terminal
- [ ] Can access http://localhost:8000/

### Endpoints Working ✅
- [ ] Root endpoint: http://localhost:8000/
- [ ] Health check: http://localhost:8000/health
- [ ] Test endpoint: http://localhost:8000/api/test
- [ ] Greet: http://localhost:8000/api/greet/YourName
- [ ] Calculate: http://localhost:8000/api/calculate?x=10&y=5

### Documentation ✅
- [ ] Swagger UI works: http://localhost:8000/docs
- [ ] Can see all endpoints listed
- [ ] ReDoc works: http://localhost:8000/redoc

### Code Understanding ✅
- [ ] Understand what FastAPI does
- [ ] Know what decorators are (`@app.get`)
- [ ] Understand path parameters (`{name}`)
- [ ] Understand query parameters (`?x=10&y=5`)

**Complete test:**
```bash
# In browser or use curl in new terminal:
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/api/greet/Test
curl "http://localhost:8000/api/calculate?x=5&y=3&operation=multiply"
```

All should return JSON responses! ✅

---

## 📝 Step 3.12: Stop the Server

When you're done testing:

**In the terminal where uvicorn is running:**
- Press **Ctrl+C** (Command+C on Mac)

You should see:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12346]
```

**To restart:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**💡 What you're learning:**
- Ctrl+C stops the server
- Server only runs when uvicorn is running
- Need to restart to run again
- Your code is saved (server stopping doesn't delete it)

---

## 📝 Step 3.13: Commit Your Changes

Let's save your progress to Git!

```bash
# Make sure server is stopped (Ctrl+C)
# Navigate to project root
cd ~/Desktop/opal-v2

# Check what changed
git status

# Should show: app/main.py and app/__init__.py

# Add files
git add .

# Commit
git commit -m "Add FastAPI Hello World

- Created main FastAPI application
- Added root and health check endpoints
- Added test, greet, and calculate endpoints
- Demonstrated path and query parameters
- All endpoints tested and working"

# View history
git log --oneline
```

**💡 What you're learning:**
- Commit after completing a working feature
- Descriptive commit messages help later
- Git tracks your progress
- Can always go back to previous versions

---

## 🐛 Common Issues and Solutions

### Issue 1: "Address already in use"
**Error:** `OSError: [Errno 48] Address already in use`

**Problem:** Port 8000 is already being used

**Solution:**
```bash
# Option 1: Find and kill the process
lsof -ti:8000 | xargs kill -9

# Option 2: Use a different port
uvicorn app.main:app --reload --port 8001
```

### Issue 2: "ModuleNotFoundError: No module named 'fastapi'"
**Problem:** Virtual environment not activated or packages not installed

**Solution:**
```bash
# Activate venv
cd backend
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Verify
pip list | grep fastapi
```

### Issue 3: "Cannot connect to localhost:8000"
**Problem:** Server not running or wrong address

**Solution:**
```bash
# Check if uvicorn is running
# Look for "Application startup complete" message

# Make sure you're using the right address
# Try: http://localhost:8000/ (with trailing slash)
# Or: http://127.0.0.1:8000/
```

### Issue 4: Changes not appearing
**Problem:** Saved file but changes don't show

**Solution:**
```bash
# Check terminal for reload message
# Make sure you saved the file (Cmd+S / Ctrl+S)
# Hard refresh browser (Cmd+Shift+R / Ctrl+F5)
# Check you're editing the right file
```

### Issue 5: Syntax Error
**Problem:** Python syntax error in your code

**Solution:**
```bash
# Read the error message carefully
# Check line number mentioned in error
# Common issues:
#   - Missing : at end of function definition
#   - Wrong indentation
#   - Missing quotes around strings
#   - Missing comma in dictionary
```

---

## 📝 Your Learning Journal - Lesson 3

Write your reflections:

### 1. What I learned:
```
- How web APIs work
- FastAPI creates endpoints
- Decorators connect URLs to functions
- Auto-reload during development
- ...
```

### 2. Cool things I discovered:
```
- Automatic documentation generation
- Type hints validate inputs
- Can test in browser easily
- ...
```

### 3. Commands I used:
```bash
uvicorn app.main:app --reload    # Run server
curl http://localhost:8000/      # Test API
git commit -m "message"          # Save progress
```

### 4. Questions:
```
- How does async/await work?
- What are other HTTP methods?
- How to handle errors?
- ...
```

---

## 🎓 Key Concepts Learned

### FastAPI Basics
- **FastAPI** = Modern Python web framework
- **Endpoints** = URLs that do something
- **Decorators** = `@app.get("/")` registers endpoints
- **Uvicorn** = ASGI server that runs FastAPI

### HTTP Concepts
- **GET** = Retrieve data
- **Path parameters** = `/greet/{name}`
- **Query parameters** = `?x=10&y=5`
- **JSON** = Data format for APIs

### Development Tools
- **Auto-reload** = Changes apply automatically
- **Swagger UI** = Interactive API testing
- **Type hints** = `name: str`, `x: int`
- **Virtual environment** = Isolated packages

---

## 🚀 What's Next?

In **Lesson 4**, you'll:
- Setup PostgreSQL database with Docker
- Connect FastAPI to the database
- Use SQLAlchemy ORM
- Create your first database table
- Store and retrieve data

**Estimated Time**: 45-60 minutes

This is where your API becomes powerful - you'll be able to save data! 💾

---

## ✅ Ready for Lesson 4?

Before continuing, make sure:
- ✅ All endpoints work correctly
- ✅ Understand path vs query parameters
- ✅ Can start/stop the server
- ✅ Documentation pages load
- ✅ Changes committed to Git
- ✅ Understand how FastAPI routes work

**When you're ready, tell me: "I finished Lesson 3" and I'll create Lesson 4!**

---

## 💡 Extra Practice (Optional)

Try these challenges:

### Challenge 1: Add a Fortune Cookie Endpoint
```python
import random

@app.get("/api/fortune")
def get_fortune():
    fortunes = [
        "You will write great code today",
        "A bug is just a feature in disguise",
        "The force will be with your commits",
        "Your pull request will be approved",
        "You will solve that bug before lunch"
    ]
    return {"fortune": random.choice(fortunes)}
```

### Challenge 2: Add a Status Endpoint
```python
from datetime import datetime

@app.get("/api/status")
def get_status():
    return {
        "server": "OPAL API",
        "version": "0.1.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "uptime": "calculate this as homework!"
    }
```

### Challenge 3: Add a User Info Endpoint
```python
@app.get("/api/user/{username}")
def get_user_info(username: str, age: int = None):
    response = {"username": username}
    if age:
        response["age"] = age
        response["message"] = f"Hello {username}, you are {age} years old"
    else:
        response["message"] = f"Hello {username}"
    return response

# Test: /api/user/Alice?age=25
```

### Challenge 4: Add a Math Endpoint with Multiple Operations
```python
@app.get("/api/math/{operation}")
def do_math(operation: str, numbers: str):
    """
    Example: /api/math/sum?numbers=1,2,3,4,5
    """
    nums = [int(n) for n in numbers.split(",")]
    
    if operation == "sum":
        result = sum(nums)
    elif operation == "average":
        result = sum(nums) / len(nums)
    elif operation == "max":
        result = max(nums)
    elif operation == "min":
        result = min(nums)
    else:
        result = "Unknown operation"
    
    return {
        "operation": operation,
        "numbers": nums,
        "result": result
    }
```

Try building these yourself! It's great practice! 🧪

---

**Congratulations on completing Lesson 3! You're now a FastAPI developer! 🎉**

**Your first web API is running!** This is a huge milestone! 🚀

---

**Next**: When ready, say "I finished Lesson 3" for Lesson 4: Database Setup with PostgreSQL

**Document Version**: 1.0  
**Last Updated**: October 8, 2025

