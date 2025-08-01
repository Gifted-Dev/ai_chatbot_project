"""
Unit tests for AI engine service
"""
import pytest
from unittest.mock import patch, MagicMock
import os
from backend.app.services.ai_engine import get_response


class TestAIEngine:
    """Test cases for AI engine service"""
    
    def test_get_response_with_mock(self):
        """Test get_response with mocked Groq client"""
        with patch('app.services.ai_engine.client') as mock_client:
            # Setup mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Mocked AI response"
            mock_client.chat.completions.create.return_value = mock_response
            
            result = get_response("Test message")
            
            assert result == "Mocked AI response"
            mock_client.chat.completions.create.assert_called_once()
    
    def test_get_response_parameters(self):
        """Test that get_response calls Groq with correct parameters"""
        with patch('app.services.ai_engine.client') as mock_client:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            
            get_response("Hello AI")
            
            # Check that the call was made with expected parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args is not None
            
            # Check messages parameter
            messages = call_args.kwargs['messages']
            assert len(messages) == 2
            assert messages[0]['role'] == 'system'
            assert messages[1]['role'] == 'user'
            assert messages[1]['content'] == 'Hello AI'
            
            # Check model parameter
            assert call_args.kwargs['model'] == 'llama-3.3-70b-versatile'
    
    def test_get_response_system_prompt(self):
        """Test that system prompt is properly included"""
        with patch('app.services.ai_engine.client') as mock_client:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            
            get_response("Test message")
            
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            system_message = messages[0]
            
            assert system_message['role'] == 'system'
            assert 'educational assistant' in system_message['content'].lower()
            assert 'helpful' in system_message['content'].lower()
    
    def test_get_response_empty_message(self):
        """Test get_response with empty message"""
        with patch('app.services.ai_engine.client') as mock_client:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Empty message response"
            mock_client.chat.completions.create.return_value = mock_response
            
            result = get_response("")
            
            assert result == "Empty message response"
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            assert messages[1]['content'] == ""
    
    def test_get_response_long_message(self):
        """Test get_response with long message"""
        long_message = "This is a very long message. " * 100
        
        with patch('app.services.ai_engine.client') as mock_client:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Long message response"
            mock_client.chat.completions.create.return_value = mock_response
            
            result = get_response(long_message)
            
            assert result == "Long message response"
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            assert messages[1]['content'] == long_message
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    def test_api_key_configuration(self):
        """Test that API key is properly configured"""
        with patch('app.services.ai_engine.Groq') as mock_groq:
            # Re-import to trigger the client creation with mocked Groq
            import importlib
            import backend.app.services.ai_engine
            importlib.reload(app.services.ai_engine)
            
            mock_groq.assert_called_with(api_key='test_key')
    
    def test_get_response_exception_handling(self):
        """Test that exceptions are properly handled"""
        with patch('app.services.ai_engine.client') as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            
            with pytest.raises(Exception):
                get_response("Test message")
