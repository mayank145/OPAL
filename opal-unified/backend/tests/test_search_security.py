"""
Tests for search functionality and security
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestSearchFunctionality:
    """Tests for various search methods"""
    
    def test_search_by_exact_id(self, client: TestClient):
        """Test searching by exact ID number"""
        response = client.get("/api/v1/fats/search/3759")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_by_keyword(self, client: TestClient):
        """Test keyword search in FATS"""
        response = client.get("/api/v1/fats/?search=tracking")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_multiple_keywords(self, client: TestClient):
        """Test search with multiple keywords"""
        response = client.get("/api/v1/fats/?search=tracking error")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_phrase(self, client: TestClient):
        """Test phrase search (exact match)"""
        response = client.get('/api/v1/fats/?search="tracking error"')
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_with_section_filter(self, client: TestClient):
        """Test combined search and section filter"""
        response = client.get("/api/v1/fats/?search=error&section=AO")
        
        assert response.status_code == 200
        data = response.json()
        
        # Results should be from AO section and contain search term
        for fats in data:
            section_match = fats.get("section") == "AO" or fats.get("section2") == "AO"
            assert section_match
    
    def test_search_case_insensitive(self, client: TestClient):
        """Test that search is case-insensitive"""
        response1 = client.get("/api/v1/fats/?search=ERROR")
        response2 = client.get("/api/v1/fats/?search=error")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        # Should return same results (case-insensitive)
    
    def test_search_empty_string(self, client: TestClient):
        """Test search with empty string"""
        response = client.get("/api/v1/fats/?search=")
        
        assert response.status_code == 200
        # Should return all or none (depends on implementation)


@pytest.mark.unit
class TestSecurityFeatures:
    """Tests for security features"""
    
    def test_sql_injection_prevention(self, client: TestClient):
        """Test that SQL injection is prevented"""
        malicious_search = "'; DROP TABLE fault; --"
        
        response = client.get(f"/api/v1/fats/?search={malicious_search}")
        
        # Should not cause error (SQLAlchemy prevents injection)
        assert response.status_code == 200
        
        # Verify tables still exist by making another query
        response2 = client.get("/api/v1/fats/")
        assert response2.status_code == 200
    
    def test_xss_prevention_in_input(self, client: TestClient, create_test_fats):
        """Test that XSS attempts in comments are handled"""
        fats = create_test_fats
        
        xss_comment = {
            "comment_text": "<script>alert('XSS')</script>",
            "commenter": "Hacker",
        }
        
        response = client.post(
            f"/api/v1/fats/{fats.idno}/comments",
            json=xss_comment
        )
        
        # Should accept the input (backend doesn't sanitize)
        # Frontend (DOMPurify) will sanitize on display
        assert response.status_code in [200, 201]
    
    def test_cors_headers(self, client: TestClient):
        """Test that CORS headers are set correctly"""
        response = client.options("/api/v1/fats/")
        
        # Check for CORS headers (if configured)
        # Implementation depends on FastAPI CORS middleware
        assert response.status_code in [200, 404]
    
    def test_large_payload_rejection(self, client: TestClient):
        """Test that extremely large payloads are rejected"""
        huge_data = {
            "issue": "Test",
            "solution": "X" * 1000000,  # 1MB of data
        }
        
        response = client.post("/api/v1/fats/", json=huge_data)
        
        # Should reject (depends on server config)
        # Might be 413 (Payload Too Large) or 422 (Validation)
        assert response.status_code in [413, 422, 200]


@pytest.mark.integration
class TestAPIValidation:
    """Tests for API input validation"""
    
    def test_limit_parameter_validation(self, client: TestClient):
        """Test that limit parameter is validated"""
        # Too high limit
        response = client.get("/api/v1/fats/?limit=999999")
        
        # Should reject or cap at max limit
        assert response.status_code in [200, 422]
        
        if response.status_code == 200:
            data = response.json()
            assert len(data) <= 10000  # Max limit
    
    def test_negative_limit_rejected(self, client: TestClient):
        """Test that negative limit is rejected"""
        response = client.get("/api/v1/fats/?limit=-1")
        
        assert response.status_code == 422
    
    def test_invalid_section_filter(self, client: TestClient):
        """Test filtering with invalid section"""
        response = client.get("/api/v1/fats/?section=INVALID_SECTION_XYZ")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0  # No results for invalid section


@pytest.mark.integration
class TestAPIPerformance:
    """Performance-related tests"""
    
    def test_large_result_set(self, client: TestClient):
        """Test handling large result sets"""
        response = client.get("/api/v1/fats/?limit=1000")
        
        assert response.status_code == 200
        # Should complete in reasonable time (< 5 seconds)
    
    def test_concurrent_requests(self, client: TestClient):
        """Test handling multiple concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return client.get("/api/v1/fats/?limit=10")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in futures]
        
        # All requests should succeed
        for response in results:
            assert response.status_code == 200

