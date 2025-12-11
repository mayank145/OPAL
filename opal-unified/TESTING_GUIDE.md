# Testing Guide for OPAL Project

## 📚 Complete Test Suite Documentation

---

## 🎯 Test Coverage Overview

### **Backend Tests (pytest)**
```
tests/
├── __init__.py                      # Package marker
├── conftest.py                      # Shared fixtures
├── test_health.py                   # Health endpoints (5 tests)
├── test_fats_api.py                # FATS CRUD operations (15 tests)
├── test_comments_api.py            # Comments API (8 tests)
└── test_search_security.py         # Search & security (15 tests)

Total: 43 backend tests
Coverage Target: 60-80%
```

### **Frontend Tests (Jest + React Testing Library)**
```
src/
├── App.test.js                      # Main app (7 tests)
├── setupTests.js                    # Test configuration
└── components/
    ├── FATSList.test.js            # List component (12 tests)
    └── FATSDetailInline.test.js    # Detail component (11 tests)

Total: 30 frontend tests
Coverage Target: 50-70%
```

---

## 🚀 Running Tests

### **Backend Tests**

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_health.py

# Run specific test
pytest tests/test_health.py::test_health_check

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run verbose mode
pytest -v

# Run and stop on first failure
pytest -x

# View HTML coverage report
open htmlcov/index.html
```

### **Frontend Tests**

```bash
# Navigate to frontend
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage --watchAll=false

# Run specific test file
npm test -- FATSList.test.js

# Run in watch mode (interactive)
npm test

# Update snapshots
npm test -- -u

# View coverage report
open coverage/lcov-report/index.html
```

---

## 📋 Test Categories

### **1. Unit Tests** (Fast, Isolated)
```
Purpose: Test individual functions/methods
Speed: < 1 second
Database: No
Network: No

Examples:
✅ test_health_check()
✅ test_strip_html_function()
✅ test_date_formatting()
✅ test_sanitize_html()

Run: pytest -m unit
```

### **2. Integration Tests** (Medium, Components)
```
Purpose: Test multiple components together
Speed: 1-5 seconds
Database: Yes (test DB)
Network: Mock API

Examples:
✅ test_list_fats_with_data()
✅ test_add_comment_success()
✅ test_search_with_section_filter()

Run: pytest -m integration
```

### **3. Database Tests** (Slow, Full Stack)
```
Purpose: Test with real database
Speed: 5-30 seconds
Database: Yes
Network: Yes (localhost)

Examples:
✅ test_create_fats_in_db()
✅ test_delete_image_from_db()
✅ test_concurrent_requests()

Run: pytest -m database
```

---

## 🧪 Test Case Details

### **Backend Test Cases**

#### **Health Tests (test_health.py)**
```python
✅ test_health_check()
   - Verifies /health endpoint responds
   - Checks status is "healthy"
   - Validates JSON structure

✅ test_root_endpoint()
   - Verifies API root responds
   - Checks for basic info

✅ test_api_docs_available()
   - Verifies /docs is accessible
   - Validates Swagger UI loads

✅ test_openapi_schema()
   - Verifies OpenAPI schema is valid
   - Checks required fields
```

#### **FATS API Tests (test_fats_api.py)**
```python
TestFATSListEndpoint:
✅ test_list_fats_empty()          - Empty database returns []
✅ test_list_fats_with_data()      - Returns fault entries
✅ test_list_fats_with_limit()     - Pagination works
✅ test_list_fats_with_section_filter() - Filtering works
✅ test_list_fats_with_search()    - Search works

TestFATSGetByID:
✅ test_get_fats_by_id_success()   - Get existing fault
✅ test_get_fats_by_id_not_found() - 404 for missing fault
✅ test_get_fats_invalid_id()      - Validation error

TestFATSSearch:
✅ test_search_by_exact_id()       - ID search works
✅ test_search_by_keyword()        - Keyword search works
✅ test_search_phrase()            - Phrase search works

TestFATSCreate:
✅ test_create_fats_success()      - Create new fault
✅ test_create_fats_missing_required() - Validation
✅ test_create_fats_invalid_data() - Type checking

TestFATSUpdate:
✅ test_update_fats_success()      - Update existing
✅ test_update_fats_not_found()    - 404 handling

TestFATSDelete:
✅ test_delete_fats_success()      - Delete works
✅ test_delete_fats_not_found()    - 404 handling
```

#### **Comments Tests (test_comments_api.py)**
```python
✅ test_get_comments_empty()              - No comments case
✅ test_add_comment_success()             - Add comment
✅ test_get_comments_with_data()          - Retrieve comments
✅ test_add_comment_to_nonexistent_fats() - Error handling
✅ test_add_comment_missing_text()        - Validation
✅ test_comment_with_html_content()       - HTML handling
✅ test_comment_with_todo_and_solution()  - Optional fields
```

#### **Security Tests (test_search_security.py)**
```python
Search Tests:
✅ test_search_by_idno()              - ID search
✅ test_search_by_keyword()           - Keyword search
✅ test_search_multiple_keywords()    - Multiple words
✅ test_search_phrase()               - Exact phrase
✅ test_search_with_section_filter()  - Combined filters
✅ test_search_case_insensitive()     - Case handling

Security Tests:
✅ test_sql_injection_prevention()    - SQLi protection
✅ test_xss_prevention_in_input()     - XSS handling
✅ test_cors_headers()                - CORS config
✅ test_large_payload_rejection()     - DoS protection

Validation Tests:
✅ test_limit_parameter_validation()  - Parameter bounds
✅ test_negative_limit_rejected()     - Input validation
✅ test_invalid_section_filter()      - Filter validation

Performance Tests:
✅ test_large_result_set()            - Performance
✅ test_concurrent_requests()         - Concurrency
```

### **Frontend Test Cases**

#### **App Tests (App.test.js)**
```javascript
✅ renders app title               - Component loads
✅ renders main tab                - Default view
✅ renders Faults List button      - Button present
✅ renders Create button           - Button present
✅ opens All Faults dialog         - Dialog works
✅ opens Create dialog             - Form opens
✅ shows snackbar notification     - Notifications work
```

#### **FATSList Tests (FATSList.test.js)**
```javascript
✅ renders FATS list table         - Table displays
✅ renders table headers correctly - Column headers
✅ search by ID number             - ID search logic
✅ search by keywords              - Keyword search
✅ search by phrase (with quotes)  - Phrase search
✅ filter by section               - Section filter
✅ calls onViewFATS when clicked   - View button
✅ calls onEditFATS when clicked   - Edit button
✅ calls onAddComment when clicked - Comment button
✅ shows loading state             - Loading indicator
✅ shows error message             - Error handling
✅ shows "No faults found"         - Empty state
✅ refresh method reloads data     - Refresh function
```

#### **FATSDetailInline Tests (FATSDetailInline.test.js)**
```javascript
✅ renders fault details           - Data displays
✅ renders sections in order       - Layout correct
✅ renders HTML formatting         - DOMPurify works
✅ displays images in gallery      - Images show
✅ displays comments               - Comments show
✅ opens image preview             - Preview dialog
✅ shows Print button              - Print feature
✅ shows delete button on hover    - Delete feature
✅ shows loading state             - Loading indicator
✅ shows error when not found      - Error handling
✅ fetches data on mount           - Data loading
```

---

## 📊 Running Test Suite

### **Quick Test (Both)**
```bash
# Terminal 1: Backend tests
cd backend
source venv/bin/activate
pytest

# Terminal 2: Frontend tests
cd frontend
npm test -- --watchAll=false
```

### **With Coverage Reports**
```bash
# Backend with coverage
cd backend
source venv/bin/activate
pytest --cov=app --cov-report=html --cov-report=term-missing

# View coverage: open htmlcov/index.html

# Frontend with coverage
cd frontend
npm test -- --coverage --watchAll=false

# View coverage: open coverage/lcov-report/index.html
```

### **Continuous Testing (Development)**
```bash
# Backend (watch mode)
cd backend
source venv/bin/activate
pytest-watch  # Or use: pytest --watch

# Frontend (watch mode)
cd frontend
npm test  # Interactive watch mode
```

---

## 🎯 Coverage Goals

### **Backend Coverage Targets**
```
Current:  0%  (no tests exist yet)
Target:   60% (minimum for production)
Ideal:    80% (high confidence)

Critical Paths (Must be 100%):
✅ Authentication (if implemented)
✅ Data validation
✅ Database operations
✅ Security features
```

### **Frontend Coverage Targets**
```
Current:  0%  (no tests exist yet)
Target:   50% (minimum for production)
Ideal:    70% (high confidence)

Critical Paths (Must be 100%):
✅ User authentication
✅ Data submission forms
✅ Search functionality
✅ File uploads/deletes
```

---

## 🧪 Test Execution Plan

### **Phase 1: Run Initial Tests** (Today)
```bash
# 1. Run backend tests
cd backend
source venv/bin/activate
pytest -v

Expected: Some tests may fail (need to adjust for your DB schema)
Action: Fix failing tests one by one

# 2. Run frontend tests
cd frontend
npm test -- --watchAll=false

Expected: Tests should pass (mocked APIs)
Action: Review coverage report
```

### **Phase 2: Fix Failing Tests** (Day 1-2)
```bash
# Common issues and fixes:

Issue: Database schema mismatch
Fix: Update test fixtures to match actual schema

Issue: API endpoint changed
Fix: Update test URLs

Issue: Field names different
Fix: Update assertions with correct field names

Issue: Missing dependencies
Fix: pip install / npm install missing packages
```

### **Phase 3: Add More Tests** (Week 1)
```bash
# Add tests for untested features:
- Image upload/delete
- Complex search scenarios
- Edge cases
- Error conditions
```

---

## 📈 Improving Test Coverage

### **Find Untested Code**
```bash
# Backend: Generate coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html

# Look for red lines (untested code)
# Add tests for those functions

# Frontend: Generate coverage report
npm test -- --coverage --watchAll=false
open coverage/lcov-report/index.html

# Look for uncovered functions
# Add tests
```

### **Writing Good Tests**
```python
# Good test structure:
def test_feature_name():
    """Clear description of what's being tested"""
    # Arrange: Set up test data
    data = create_test_data()
    
    # Act: Execute the function
    result = function_to_test(data)
    
    # Assert: Verify the result
    assert result == expected_value
    assert error_not_raised
```

---

## 🔧 Troubleshooting Tests

### **Backend: Tests Won't Run**
```bash
# Issue: pytest not found
pip install pytest

# Issue: Module not found
pip install -r requirements.txt

# Issue: Database errors
# Check TEST_DATABASE_URL in conftest.py

# Issue: Async errors
pip install pytest-asyncio
```

### **Frontend: Tests Won't Run**
```bash
# Issue: Testing library not found
npm install @testing-library/react @testing-library/jest-dom

# Issue: Module mock errors
# Add jest.mock() at top of test file

# Issue: Component won't render
# Check for missing props
```

### **Common Test Failures**
```bash
# 1. Assertion Error
# Fix: Check expected vs actual values

# 2. Timeout Error  
# Fix: Add await waitFor() for async operations

# 3. Element Not Found
# Fix: Wait for element to appear (async rendering)

# 4. Mock Not Working
# Fix: Ensure mock is before render()
```

---

## 📊 Test Metrics

### **What to Measure**
```
✅ Test Coverage (% of code tested)
✅ Test Pass Rate (% passing)
✅ Test Speed (time to run)
✅ Test Stability (flakiness)
```

### **Good Metrics**
```
Coverage:     > 60% (backend), > 50% (frontend)
Pass Rate:    100% (all green)
Speed:        < 5 minutes (total suite)
Flakiness:    < 1% (stable tests)
```

---

## 🎯 Test Execution Workflow

### **Before Every Commit**
```bash
# Run quick tests
pytest tests/test_health.py
npm test -- App.test.js --watchAll=false

# If pass: Commit
# If fail: Fix before committing
```

### **Before Pull Request**
```bash
# Run full test suite
cd backend && pytest
cd frontend && npm test -- --watchAll=false

# Check coverage
pytest --cov=app
npm test -- --coverage --watchAll=false

# If all pass: Create PR
```

### **In CI/CD Pipeline**
```
GitHub Actions automatically runs:
✅ All backend tests
✅ All frontend tests
✅ Coverage reports
✅ Security scans

If any fail: PR blocked ❌
If all pass: PR approved ✅
```

---

## 🎨 Writing New Tests

### **Backend Test Template**
```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
def test_your_feature(client: TestClient):
    """Test description"""
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = client.post("/api/endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "value"
```

### **Frontend Test Template**
```javascript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import YourComponent from './YourComponent';

test('your feature', async () => {
  // Arrange
  const user = userEvent.setup();
  render(<YourComponent />);
  
  // Act
  const button = screen.getByText('Click Me');
  await user.click(button);
  
  // Assert
  await waitFor(() => {
    expect(screen.getByText('Result')).toBeInTheDocument();
  });
});
```

---

## 📈 Coverage Reports

### **Backend Coverage**
```bash
# Generate HTML report
pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html

# View in terminal
pytest --cov=app --cov-report=term-missing

# Shows:
- Lines covered (green)
- Lines not covered (red)
- Percentage per file
- Overall percentage
```

### **Frontend Coverage**
```bash
# Generate coverage
npm test -- --coverage --watchAll=false

# View report
open coverage/lcov-report/index.html

# Terminal summary
npm test -- --coverage --watchAll=false --verbose

# Shows:
- Statements covered
- Branches covered
- Functions covered
- Lines covered
```

---

## 🎯 Next Steps

### **Immediate (Today)**
```bash
# 1. Run tests to see current state
cd backend && pytest -v
cd frontend && npm test -- --watchAll=false

# 2. Fix any failing tests
# 3. Check coverage
# 4. Identify gaps
```

### **This Week**
```bash
# 1. Add tests for critical paths:
   - User authentication (if exists)
   - Data submission
   - Search functionality
   - Image operations

# 2. Achieve minimum coverage:
   - Backend: 60%
   - Frontend: 50%

# 3. Integrate with CI/CD
   - Tests run automatically
   - Block merges if tests fail
```

### **Ongoing**
```bash
# Every new feature:
✅ Write tests BEFORE implementing
✅ Test-Driven Development (TDD)
✅ Maintain coverage above target
✅ Review and refactor tests
```

---

## 🎉 Benefits of Testing

### **Confidence**
```
✅ Know code works before deploying
✅ Catch bugs before users do
✅ Refactor without fear
✅ Sleep well at night
```

### **Documentation**
```
✅ Tests show how to use your API
✅ Examples of expected behavior
✅ Living documentation (always up-to-date)
```

### **Speed**
```
✅ Fast feedback (5 minutes vs 5 hours)
✅ Automated (vs manual testing)
✅ Repeatable (same tests every time)
```

---

## 📚 Additional Resources

- **pytest docs:** https://docs.pytest.org/
- **React Testing Library:** https://testing-library.com/react
- **FastAPI testing:** https://fastapi.tiangolo.com/tutorial/testing/
- **Jest docs:** https://jestjs.io/docs/getting-started

---

## 🎯 Quick Start

```bash
# Run all tests now:
cd backend && source venv/bin/activate && pytest -v
cd frontend && npm test -- --watchAll=false

# View this guide:
cat TESTING_GUIDE.md
```

---

**You now have 73 tests ready to run!** 🎉  
**Start with: `pytest -v` and `npm test`** 🚀

