#!/bin/bash
# Quick search functionality test script

echo "🧪 Testing Search Functionality"
echo "================================"
echo ""

BASE_URL="http://localhost:8000"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local test_name="$1"
    local url="$2"
    local max_time="$3"
    
    echo -n "Testing: $test_name... "
    
    # Make request and get timing
    response_time=$(curl -s -w "%{time_total}" -o /dev/null -m 5 "$url" 2>/dev/null)
    exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        echo -e "${RED}✗ FAILED (timeout or error)${NC}"
        return 1
    fi
    
    # Convert to milliseconds for easier reading
    ms=$(echo "$response_time * 1000" | bc)
    ms_int=${ms%.*}
    
    # Check if under threshold
    threshold_ms=$(echo "$max_time * 1000" | bc)
    threshold_int=${threshold_ms%.*}
    
    if [ "$ms_int" -lt "$threshold_int" ]; then
        echo -e "${GREEN}✓ PASS${NC} (${ms_int}ms)"
        return 0
    else
        echo -e "${YELLOW}⚠ SLOW${NC} (${ms_int}ms, expected <${threshold_int}ms)"
        return 0
    fi
}

# Run tests
echo "Testing backend API endpoints:"
echo ""

test_endpoint "Health check" "$BASE_URL/health" 0.1
test_endpoint "FATS list (10 entries)" "$BASE_URL/api/v1/fats/?limit=10" 0.1
test_endpoint "FATS list (100 entries)" "$BASE_URL/api/v1/fats/?limit=100" 0.1
test_endpoint "Search by fault ID (4767)" "$BASE_URL/api/v1/fats/?search=4767" 0.1
test_endpoint "Search by fault ID (4766)" "$BASE_URL/api/v1/fats/?search=4766" 0.1
test_endpoint "Search by keyword (Edit)" "$BASE_URL/api/v1/fats/?search=Edit" 0.1
test_endpoint "Search by operator (dailey)" "$BASE_URL/api/v1/fats/?search=dailey" 0.1
test_endpoint "Search in description (Moritani)" "$BASE_URL/api/v1/fats/?search=Moritani" 0.1
test_endpoint "Filter by section (Gen2)" "$BASE_URL/api/v1/fats/?section=Gen2" 0.1
test_endpoint "Filter by status (Active)" "$BASE_URL/api/v1/fats/?status=Active" 0.1
test_endpoint "Combined search + filter" "$BASE_URL/api/v1/fats/?search=Demo&section=Gen2" 0.1
test_endpoint "Reference: Sections" "$BASE_URL/api/v1/reference/sections" 0.1
test_endpoint "Reference: Staff" "$BASE_URL/api/v1/reference/staff" 0.1

echo ""
echo "================================"
echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo "Expected: All response times should be under 100ms"
echo "If any tests FAILED or are SLOW, check backend logs"
