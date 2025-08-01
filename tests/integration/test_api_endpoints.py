"""
Unit tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.main import app


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return TestClient(app)
    
    def test_chat_endpoint_success(self, client):
        """Test successful chat endpoint call"""
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Test AI response"
            
            response = client.post("/chat", json={"user_message": "Hello"})
            
            assert response.status_code == 200
            data = response.json()
            assert data["user_message"] == "Hello"
            assert data["bot_response"] == "Test AI response"
            assert "timestamp" in data
    
    def test_chat_endpoint_missing_message(self, client):
        """Test chat endpoint with missing user_message"""
        response = client.post("/chat", json={})
        assert response.status_code == 422  # Validation error
    
    def test_chat_endpoint_invalid_json(self, client):
        """Test chat endpoint with invalid JSON"""
        response = client.post("/chat", data="invalid json")
        assert response.status_code == 422
    
    def test_chat_endpoint_empty_message(self, client):
        """Test chat endpoint with empty message"""
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to empty message"
            
            response = client.post("/chat", json={"user_message": ""})
            
            assert response.status_code == 200
            data = response.json()
            assert data["user_message"] == ""
            assert data["bot_response"] == "Response to empty message"
    
    def test_chat_endpoint_ai_service_error(self, client):
        """Test chat endpoint when AI service fails"""
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.side_effect = Exception("AI service error")
            
            response = client.post("/chat", json={"user_message": "Hello"})
            
            # Should return 500 internal server error
            assert response.status_code == 500
    
    def test_history_endpoint_success(self, client):
        """Test successful history endpoint call"""
        response = client.get("/history")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Check structure of history entries if any exist
        if len(data) > 0:
            entry = data[0]
            assert "user" in entry
            assert "bot" in entry
    
    def test_history_endpoint_with_limit(self, client):
        """Test history endpoint with limit parameter"""
        response = client.get("/history?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
    
    def test_history_endpoint_invalid_limit(self, client):
        """Test history endpoint with invalid limit"""
        response = client.get("/history?limit=invalid")
        
        # Should still work, likely ignoring invalid parameter
        assert response.status_code == 200
    
    def test_cors_headers(self, client):
        """Test that CORS headers are properly set"""
        response = client.options("/chat")
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
    
    def test_openapi_docs(self, client):
        """Test that OpenAPI documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_nonexistent_endpoint(self, client):
        """Test calling a non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_chat_endpoint_database_integration(self, client):
        """Test that chat endpoint properly saves to database"""
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Database test response"
            
            # Get initial history count
            history_before = client.get("/history").json()
            initial_count = len(history_before)
            
            # Make a chat request
            response = client.post("/chat", json={"user_message": "Database test"})
            assert response.status_code == 200
            
            # Check that history increased
            history_after = client.get("/history").json()
            final_count = len(history_after)
            
            assert final_count > initial_count
            
            # Check that the new entry is in history
            latest_entry = history_after[0]  # Should be most recent
            assert latest_entry["user"] == "Database test"
            assert latest_entry["bot"] == "Database test response"
