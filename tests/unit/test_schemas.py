"""
Unit tests for Pydantic schemas
"""
import pytest
from pydantic import ValidationError
from datetime import datetime
from backend.app.schemas import ChatRequest, ChatResponse


class TestChatRequest:
    """Test cases for ChatRequest schema"""
    
    def test_valid_chat_request(self):
        """Test creating a valid ChatRequest"""
        request = ChatRequest(user_message="Hello, world!")
        assert request.user_message == "Hello, world!"
    
    def test_empty_user_message(self):
        """Test that empty user_message is allowed"""
        request = ChatRequest(user_message="")
        assert request.user_message == ""
    
    def test_missing_user_message(self):
        """Test that missing user_message raises ValidationError"""
        with pytest.raises(ValidationError):
            ChatRequest()
    
    def test_user_message_type_validation(self):
        """Test that user_message must be a string"""
        with pytest.raises(ValidationError):
            ChatRequest(user_message=123)
    
    def test_extra_fields_ignored(self):
        """Test that extra fields are ignored"""
        request = ChatRequest(user_message="Hello", extra_field="ignored")
        assert request.user_message == "Hello"
        assert not hasattr(request, 'extra_field')


class TestChatResponse:
    """Test cases for ChatResponse schema"""
    
    def test_valid_chat_response(self):
        """Test creating a valid ChatResponse"""
        timestamp = datetime.now()
        response = ChatResponse(
            user_message="Hello",
            bot_response="Hi there!",
            timestamp=timestamp
        )
        assert response.user_message == "Hello"
        assert response.bot_response == "Hi there!"
        assert response.timestamp == timestamp
    
    def test_optional_bot_response(self):
        """Test that bot_response is optional"""
        timestamp = datetime.now()
        response = ChatResponse(
            user_message="Hello",
            bot_response=None,
            timestamp=timestamp
        )
        assert response.user_message == "Hello"
        assert response.bot_response is None
        assert response.timestamp == timestamp
    
    def test_missing_required_fields(self):
        """Test that missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            ChatResponse(user_message="Hello")  # Missing timestamp
        
        with pytest.raises(ValidationError):
            ChatResponse(timestamp=datetime.now())  # Missing user_message
    
    def test_timestamp_type_validation(self):
        """Test that timestamp must be a datetime"""
        with pytest.raises(ValidationError):
            ChatResponse(
                user_message="Hello",
                bot_response="Hi",
                timestamp="not a datetime"
            )
    
    def test_from_attributes_config(self):
        """Test that from_attributes is properly configured"""
        # This tests the Config class setting
        assert hasattr(ChatResponse.model_config, 'from_attributes') or \
               getattr(ChatResponse.model_config, 'from_attributes', False)
