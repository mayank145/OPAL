"""
Tests for FATS Comments API endpoints
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.database
class TestCommentsAPI:
    """Tests for comments endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_comments_empty(self, client: TestClient, create_test_fats):
        """Test getting comments for FATS with no comments"""
        fats = create_test_fats
        response = client.get(f"/api/v1/fats/{fats.idno}/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    @pytest.mark.asyncio
    async def test_add_comment_success(self, client: TestClient, create_test_fats, sample_comment_data):
        """Test adding a comment to FATS"""
        fats = create_test_fats
        
        response = client.post(
            f"/api/v1/fats/{fats.idno}/comments",
            json=sample_comment_data
        )
        
        assert response.status_code == 200 or response.status_code == 201
        data = response.json()
        
        assert "id" in data
        assert data["comment_text"] == sample_comment_data["comment_text"]
        assert data["commenter"] == sample_comment_data["commenter"]
    
    @pytest.mark.asyncio
    async def test_get_comments_with_data(self, client: TestClient, create_test_fats, sample_comment_data):
        """Test getting comments after adding one"""
        fats = create_test_fats
        
        # Add comment
        client.post(f"/api/v1/fats/{fats.idno}/comments", json=sample_comment_data)
        
        # Get comments
        response = client.get(f"/api/v1/fats/{fats.idno}/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["comment_text"] == sample_comment_data["comment_text"]
    
    def test_add_comment_to_nonexistent_fats(self, client: TestClient, sample_comment_data):
        """Test adding comment to non-existent FATS"""
        response = client.post(
            "/api/v1/fats/999999/comments",
            json=sample_comment_data
        )
        
        # Might be 404 or might create orphan comment (depends on implementation)
        assert response.status_code in [404, 200, 201]
    
    def test_add_comment_missing_text(self, client: TestClient, create_test_fats):
        """Test adding comment without required comment_text"""
        fats = create_test_fats
        
        invalid_comment = {
            "commenter": "Test",
            # Missing comment_text (required)
        }
        
        response = client.post(
            f"/api/v1/fats/{fats.idno}/comments",
            json=invalid_comment
        )
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_comment_with_html_content(self, client: TestClient, create_test_fats):
        """Test that HTML in comments is stored correctly"""
        fats = create_test_fats
        
        comment_with_html = {
            "comment_text": "<p><strong>Important:</strong> Test comment</p>",
            "commenter": "Test User",
        }
        
        response = client.post(
            f"/api/v1/fats/{fats.idno}/comments",
            json=comment_with_html
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        
        # HTML should be stored (will be sanitized on frontend)
        assert "<p>" in data["comment_text"] or data["comment_text"] == comment_with_html["comment_text"]
    
    @pytest.mark.asyncio
    async def test_comment_with_todo_and_solution(self, client: TestClient, create_test_fats):
        """Test comment with optional TODO and solution fields"""
        fats = create_test_fats
        
        full_comment = {
            "comment_text": "Main comment",
            "commenter": "User",
            "todo": "Action item",
            "solution": "Solution note",
        }
        
        response = client.post(
            f"/api/v1/fats/{fats.idno}/comments",
            json=full_comment
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        
        assert data["comment_text"] == "Main comment"
        assert data["todo"] == "Action item"
        assert data["solution"] == "Solution note"

