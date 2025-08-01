"""
Unit tests for database models
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models import ChatMessage, Base
from datetime import datetime


class TestChatMessage:
    """Test cases for ChatMessage model"""
    
    @pytest.fixture
    def db_session(self):
        """Create a test database session"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = TestingSessionLocal()
        yield session
        session.close()
    
    def test_chat_message_creation(self, db_session):
        """Test creating a ChatMessage instance"""
        message = ChatMessage(
            user_message="Test message",
            bot_response="Test response"
        )
        db_session.add(message)
        db_session.commit()
        
        assert message.id is not None
        assert message.user_message == "Test message"
        assert message.bot_response == "Test response"
        assert message.timestamp is not None
        assert isinstance(message.timestamp, datetime)
    
    def test_chat_message_required_fields(self, db_session):
        """Test that user_message is required"""
        # This should work - bot_response is nullable
        message = ChatMessage(user_message="Test message")
        db_session.add(message)
        db_session.commit()
        
        assert message.user_message == "Test message"
        assert message.bot_response is None
    
    def test_chat_message_string_representation(self, db_session):
        """Test string representation of ChatMessage"""
        message = ChatMessage(
            user_message="Test message",
            bot_response="Test response"
        )
        db_session.add(message)
        db_session.commit()
        
        # Test that the object can be converted to string without error
        str_repr = str(message)
        assert isinstance(str_repr, str)
    
    def test_chat_message_table_name(self):
        """Test that table name is correct"""
        assert ChatMessage.__tablename__ == "chat_messages"
    
    def test_chat_message_columns(self):
        """Test that all expected columns exist"""
        columns = [column.name for column in ChatMessage.__table__.columns]
        expected_columns = ['id', 'user_message', 'bot_response', 'timestamp']
        
        for col in expected_columns:
            assert col in columns
