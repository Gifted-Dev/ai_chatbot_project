"""
Unit tests for CRUD operations
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models import ChatMessage, Base
from app import crud, schemas


class TestCRUD:
    """Test cases for CRUD operations"""
    
    @pytest.fixture
    def db_session(self):
        """Create a test database session"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = TestingSessionLocal()
        yield session
        session.close()
    
    def test_save_chat(self, db_session):
        """Test saving a chat message"""
        chat_request = schemas.ChatRequest(user_message="Test message")
        response_text = "Test response"
        
        chat_entry = crud.save_chat(db_session, chat_request, response_text)
        
        assert chat_entry.id is not None
        assert chat_entry.user_message == "Test message"
        assert chat_entry.bot_response == "Test response"
        assert chat_entry.timestamp is not None
    
    def test_save_chat_with_none_response(self, db_session):
        """Test saving a chat message with None response"""
        chat_request = schemas.ChatRequest(user_message="Test message")
        response_text = None
        
        chat_entry = crud.save_chat(db_session, chat_request, response_text)
        
        assert chat_entry.user_message == "Test message"
        assert chat_entry.bot_response is None
    
    def test_get_chat_history_empty(self, db_session):
        """Test getting chat history when database is empty"""
        history = crud.get_chat_history(db_session)
        assert history == []
    
    def test_get_chat_history_with_data(self, db_session):
        """Test getting chat history with data"""
        # Add some test data
        for i in range(5):
            chat_request = schemas.ChatRequest(user_message=f"Message {i}")
            crud.save_chat(db_session, chat_request, f"Response {i}")
        
        history = crud.get_chat_history(db_session)
        assert len(history) == 5
        
        # Check that results are ordered by timestamp desc (most recent first)
        assert history[0].user_message == "Message 4"  # Most recent
        assert history[-1].user_message == "Message 0"  # Oldest
    
    def test_get_chat_history_with_limit(self, db_session):
        """Test getting chat history with limit"""
        # Add some test data
        for i in range(10):
            chat_request = schemas.ChatRequest(user_message=f"Message {i}")
            crud.save_chat(db_session, chat_request, f"Response {i}")
        
        history = crud.get_chat_history(db_session, limit=3)
        assert len(history) == 3
        
        # Should get the 3 most recent
        assert history[0].user_message == "Message 9"
        assert history[1].user_message == "Message 8"
        assert history[2].user_message == "Message 7"
    
    def test_get_chat_history_default_limit(self, db_session):
        """Test that default limit is 10"""
        # Add more than 10 entries
        for i in range(15):
            chat_request = schemas.ChatRequest(user_message=f"Message {i}")
            crud.save_chat(db_session, chat_request, f"Response {i}")
        
        history = crud.get_chat_history(db_session)
        assert len(history) == 10  # Default limit
    
    def test_save_chat_persistence(self, db_session):
        """Test that saved chat persists in database"""
        chat_request = schemas.ChatRequest(user_message="Persistent message")
        chat_entry = crud.save_chat(db_session, chat_request, "Persistent response")
        
        # Query directly from database
        saved_entry = db_session.query(ChatMessage).filter_by(id=chat_entry.id).first()
        assert saved_entry is not None
        assert saved_entry.user_message == "Persistent message"
        assert saved_entry.bot_response == "Persistent response"
