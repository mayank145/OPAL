# Search Functionality Testing Guide

## Quick Test Checklist

### ✅ Frontend Testing (Recommended)

Open your browser to `http://localhost:3000` and test these scenarios:

#### Test 1: Basic Loading
- [ ] Navigate to the FATS list page
- [ ] Verify entries load quickly (should be instant)
- [ ] Check that no timeout errors appear in browser console (F12)

#### Test 2: Search by Issue Title
- [ ] Type "Edit" in the search box
- [ ] Should find entries with "Edit button" in the title
- [ ] Results should appear instantly (< 1 second)

#### Test 3: Search by Operator Name
- [ ] Type "Moritani" in the search box
- [ ] Should find entries where Moritani is mentioned
- [ ] Should find entries even if name is in the description

#### Test 4: Search by Description Text
- [ ] Type "Guide loop stopped" in the search box
- [ ] Should find entries with this text in the description
- [ ] This would have timed out before - now should be instant

#### Test 5: Filter by Section
- [ ] Use the section dropdown/filter
- [ ] Select "Gen2" or "Instruments/PFS"
- [ ] Should filter results instantly

#### Test 6: Combined Search + Filter
- [ ] Type a search term like "Demo"
- [ ] Also select a section filter
- [ ] Should apply both filters instantly

### ✅ Backend API Testing (Manual)

Open a terminal and run these curl commands:

```bash
# Test 1: Get first 10 FATS entries
curl "http://localhost:8000/api/v1/fats/?limit=10" | jq

# Test 2: Search by issue title
curl "http://localhost:8000/api/v1/fats/?search=Edit" | jq

# Test 3: Search by operator
curl "http://localhost:8000/api/v1/fats/?search=dailey" | jq

# Test 4: Search by description (large text field)
curl "http://localhost:8000/api/v1/fats/?search=Moritani" | jq

# Test 5: Filter by section
curl "http://localhost:8000/api/v1/fats/?section=Gen2" | jq

# Test 6: Filter by status
curl "http://localhost:8000/api/v1/fats/?status=Active" | jq

# Test 7: Combined search + filter
curl "http://localhost:8000/api/v1/fats/?search=Demo&section=Gen2" | jq

# Test 8: Search with limit
curl "http://localhost:8000/api/v1/fats/?search=Auto&limit=5" | jq
```

**Note:** If you don't have `jq` installed, remove `| jq` from the commands.

### ✅ Performance Testing

Test response times to ensure optimization is working:

```bash
# Test with timing (should all be under 100ms)
curl -w "\nTime: %{time_total}s\n" -o /dev/null -s "http://localhost:8000/api/v1/fats/?limit=100"
curl -w "\nTime: %{time_total}s\n" -o /dev/null -s "http://localhost:8000/api/v1/fats/?search=Edit"
curl -w "\nTime: %{time_total}s\n" -o /dev/null -s "http://localhost:8000/api/v1/fats/?search=Moritani"
curl -w "\nTime: %{time_total}s\n" -o /dev/null -s "http://localhost:8000/api/v1/fats/?section=Gen2"
```

**Expected results:**
- All queries should complete in **under 100ms**
- Most should be **under 50ms**
- No timeouts or errors

### ✅ Browser Console Testing

1. Open browser to `http://localhost:3000`
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Run these JavaScript commands:

```javascript
// Test 1: Fetch FATS list
fetch('http://localhost:8000/api/v1/fats/?limit=10')
  .then(r => r.json())
  .then(data => console.log('✓ Found', data.length, 'entries'))
  .catch(err => console.error('✗ Error:', err));

// Test 2: Search by term
fetch('http://localhost:8000/api/v1/fats/?search=Edit')
  .then(r => r.json())
  .then(data => console.log('✓ Search found', data.length, 'results'))
  .catch(err => console.error('✗ Error:', err));

// Test 3: Search in descriptions
fetch('http://localhost:8000/api/v1/fats/?search=Moritani')
  .then(r => r.json())
  .then(data => {
    console.log('✓ Description search found', data.length, 'results');
    data.forEach(e => console.log(`  #${e.idno}: ${e.issue}`));
  })
  .catch(err => console.error('✗ Error:', err));
```

### ✅ Network Tab Verification

1. Open browser to `http://localhost:3000`
2. Press **F12** → Go to **Network** tab
3. Perform searches in the UI
4. Click on API requests (they'll be named like `fats?search=...`)
5. Check the **Timing** tab:
   - **Waiting (TTFB)**: Should be < 100ms
   - **Content Download**: Should be < 50ms

### 🔍 What to Look For

**✅ Good Signs:**
- No "timeout" errors in console
- Searches return results instantly
- Network requests complete in < 100ms
- UI feels snappy and responsive

**❌ Bad Signs (if you see these, something is wrong):**
- `AxiosError` or timeout messages
- Requests taking > 1 second
- Empty results when they should have data
- Console errors about backend being unresponsive

### 📊 Verify Database Indexes

You can verify the indexes were applied correctly:

```bash
# Connect to database and check indexes
mysql -u opal -popal_password opal -e "SHOW INDEX FROM fault;"
```

You should see these indexes:
- ✅ `PRIMARY` on `idno`
- ✅ `idx_fault_issue` on `issue`
- ✅ `idx_fault_solution` on `solution` ← NEW
- ✅ `idx_fault_operator` on `operator` ← NEW
- ✅ `idx_fault_section` on `section` ← NEW
- ✅ `idx_fault_status` on `status` ← NEW
- ✅ `idx_fault_assigned_to` on `assigned_to` ← NEW

### 🧪 Edge Cases to Test

1. **Empty search:** Search for a term that doesn't exist like "ZZZnonexistent"
   - Should return `[]` (empty array) quickly, not timeout

2. **Very long search:** Search for a long phrase
   - Should still be fast

3. **Special characters:** Search for terms with symbols like "A/C" or "Gen2"
   - Should handle gracefully

4. **Multiple filters:** Apply search + section + status filters together
   - Should combine all filters correctly

### 📝 Test Results Template

Use this to document your testing:

```
Date: ___________
Tester: ___________

Frontend Tests:
[ ] Basic loading - Pass/Fail
[ ] Search by title - Pass/Fail
[ ] Search by operator - Pass/Fail
[ ] Search by description - Pass/Fail
[ ] Filter by section - Pass/Fail
[ ] Combined filters - Pass/Fail

Performance:
- FATS list load time: _____ ms
- Search by title time: _____ ms
- Search by description time: _____ ms
- Filter by section time: _____ ms

Issues Found:
___________________________________________
___________________________________________

Overall: Pass / Fail
```

---

## Quick Automated Test Script

Save this as a file and run it for quick verification:

```bash
#!/bin/bash
# Quick search functionality test

echo "🧪 Testing Search Functionality"
echo "================================"
echo ""

BASE_URL="http://localhost:8000"

# Test 1
echo "Test 1: Basic FATS list"
RESULT=$(curl -s -w "%{time_total}" -o /dev/null "$BASE_URL/api/v1/fats/?limit=10")
echo "✓ Response time: ${RESULT}s"
echo ""

# Test 2
echo "Test 2: Search by issue"
RESULT=$(curl -s -w "%{time_total}" -o /dev/null "$BASE_URL/api/v1/fats/?search=Edit")
echo "✓ Response time: ${RESULT}s"
echo ""

# Test 3
echo "Test 3: Search by description"
RESULT=$(curl -s -w "%{time_total}" -o /dev/null "$BASE_URL/api/v1/fats/?search=Moritani")
echo "✓ Response time: ${RESULT}s"
echo ""

# Test 4
echo "Test 4: Filter by section"
RESULT=$(curl -s -w "%{time_total}" -o /dev/null "$BASE_URL/api/v1/fats/?section=Gen2")
echo "✓ Response time: ${RESULT}s"
echo ""

echo "================================"
echo "✅ All tests completed!"
echo "All response times should be under 0.1s (100ms)"
```

Run it with:
```bash
chmod +x test_search.sh
./test_search.sh
```
