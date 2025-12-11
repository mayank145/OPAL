"""
Tests for FATS API endpoints
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.database
class TestFATSListEndpoint:
    """Tests for listing FATS entries"""
    
    def test_list_fats_empty(self, client: TestClient):
        """Test listing FATS when database is empty"""
        response = client.get("/api/v1/fats/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    @pytest.mark.asyncio
    async def test_list_fats_with_data(self, client: TestClient, create_test_fats):
        """Test listing FATS with data"""
        response = client.get("/api/v1/fats/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first entry structure
        first_fats = data[0]
        assert "idno" in first_fats
        assert "issue" in first_fats
        assert "solution" in first_fats
        assert "status" in first_fats
    
    def test_list_fats_with_limit(self, client: TestClient):
        """Test pagination with limit parameter"""
        response = client.get("/api/v1/fats/?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5
    
    def test_list_fats_with_section_filter(self, client: TestClient):
        """Test filtering by section"""
        response = client.get("/api/v1/fats/?section=AO")
        
        assert response.status_code == 200
        data = response.json()
        # All results should be from AO section
        for fats in data:
            assert fats.get("section") == "AO" or fats.get("section2") == "AO"
    
    def test_list_fats_with_search(self, client: TestClient):
        """Test search functionality"""
        response = client.get("/api/v1/fats/?search=test")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
@pytest.mark.database
class TestFATSGetByID:
    """Tests for getting FATS by ID"""
    
    @pytest.mark.asyncio
    async def test_get_fats_by_id_success(self, client: TestClient, create_test_fats):
        """Test getting existing FATS by ID"""
        fats = create_test_fats
        response = client.get(f"/api/v1/fats/{fats.idno}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["idno"] == fats.idno
        assert data["issue"] == fats.issue
        assert data["solution"] == fats.solution
    
    def test_get_fats_by_id_not_found(self, client: TestClient):
        """Test getting non-existent FATS returns 404"""
        response = client.get("/api/v1/fats/999999")
        
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_get_fats_invalid_id(self, client: TestClient):
        """Test getting FATS with invalid ID format"""
        response = client.get("/api/v1/fats/invalid")
        
        assert response.status_code == 422  # Validation error


@pytest.mark.integration
@pytest.mark.database
class TestFATSSearch:
    """Tests for FATS search functionality"""
    
    def test_search_by_idno(self, client: TestClient):
        """Test searching by ID number"""
        response = client.get("/api/v1/fats/search/3759")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_search_by_idno_with_result(self, client: TestClient, create_test_fats):
        """Test ID search returns correct result"""
        fats = create_test_fats
        response = client.get(f"/api/v1/fats/search/{fats.idno}")
        
        assert response.status_code == 200
        data = response.json()
        
        if len(data) > 0:
            assert data[0]["idno"] == fats.idno
    
    def test_search_by_keyword(self, client: TestClient):
        """Test keyword search"""
        response = client.get("/api/v1/fats/?search=tracking")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_phrase(self, client: TestClient):
        """Test phrase search (exact match)"""
        response = client.get('/api/v1/fats/?search="tracking error"')
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
@pytest.mark.database
class TestFATSCreate:
    """Tests for creating FATS entries"""
    
    def test_create_fats_success(self, client: TestClient, sample_fats_data):
        """Test creating a new FATS entry"""
        response = client.post("/api/v1/fats/", json=sample_fats_data)
        
        assert response.status_code == 200 or response.status_code == 201
        data = response.json()
        
        assert "idno" in data
        assert data["issue"] == sample_fats_data["issue"]
        assert data["solution"] == sample_fats_data["solution"]
    
    def test_create_fats_missing_required_fields(self, client: TestClient):
        """Test creating FATS with missing required fields"""
        incomplete_data = {
            "issue": "Test"
            # Missing solution and other required fields
        }
        
        response = client.post("/api/v1/fats/", json=incomplete_data)
        
        # Should fail validation
        assert response.status_code == 422
    
    def test_create_fats_invalid_data(self, client: TestClient):
        """Test creating FATS with invalid data types"""
        invalid_data = {
            "issue": 123,  # Should be string
            "solution": None,
        }
        
        response = client.post("/api/v1/fats/", json=invalid_data)
        
        assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.database
class TestFATSUpdate:
    """Tests for updating FATS entries"""
    
    @pytest.mark.asyncio
    async def test_update_fats_success(self, client: TestClient, create_test_fats):
        """Test updating existing FATS"""
        fats = create_test_fats
        
        update_data = {
            "issue": "Updated Issue",
            "solution": "Updated Solution",
        }
        
        response = client.put(f"/api/v1/fats/{fats.idno}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["issue"] == "Updated Issue"
    
    def test_update_fats_not_found(self, client: TestClient):
        """Test updating non-existent FATS"""
        update_data = {
            "issue": "Updated Issue",
        }
        
        response = client.put("/api/v1/fats/999999", json=update_data)
        
        assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.database
class TestFATSDelete:
    """Tests for deleting FATS entries"""
    
    @pytest.mark.asyncio
    async def test_delete_fats_success(self, client: TestClient, create_test_fats):
        """Test deleting existing FATS"""
        fats = create_test_fats
        
        response = client.delete(f"/api/v1/fats/{fats.idno}")
        
        assert response.status_code == 200 or response.status_code == 204
    
    def test_delete_fats_not_found(self, client: TestClient):
        """Test deleting non-existent FATS"""
        response = client.delete("/api/v1/fats/999999")
        
        assert response.status_code == 404

