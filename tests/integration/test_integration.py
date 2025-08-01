#!/usr/bin/env python3
"""
Integration tests for the AI chatbot project
Tests end-to-end functionality across all components
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_integration():
    """Test database integration with models and CRUD"""
    try:
        from backend.app.services.database import engine, sessionlocal
        from backend.app.models import ChatMessage, Base
        from app import crud, schemas
        from sqlalchemy import inspect
        
        print("Testing database integration...")
        
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            assert result.fetchone()[0] == 1
        print("✅ Database connection working")
        
        # Test table creation
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert 'chat_messages' in tables
        print("✅ Database tables created")
        
        # Test CRUD operations
        db = sessionlocal()
        try:
            # Create
            chat_request = schemas.ChatRequest(user_message="Integration test message")
            chat_entry = crud.save_chat(db, chat_request, "Integration test response")
            assert chat_entry.id is not None
            print("✅ CRUD create operation working")
            
            # Read
            history = crud.get_chat_history(db, limit=1)
            assert len(history) >= 1
            assert history[0].user_message == "Integration test message"
            print("✅ CRUD read operation working")
            
            # Cleanup
            db.delete(chat_entry)
            db.commit()
            
        finally:
            db.close()
        
        return True
    except Exception as e:
        print(f"❌ Database integration failed: {e}")
        return False

def test_ai_service_integration():
    """Test AI service integration"""
    try:
        from backend.app.services.ai_engine import get_response
        import os
        
        print("Testing AI service integration...")
        
        # Check API key
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("⚠️ GROQ_API_KEY not found, skipping AI service test")
            return True
        
        # Test AI response
        response = get_response("Hello, please respond with 'Integration test successful'")
        assert response is not None
        assert len(response) > 0
        print(f"✅ AI service responding: {response[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ AI service integration failed: {e}")
        return False

def test_api_integration():
    """Test API integration with all components"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        
        print("Testing API integration...")
        
        client = TestClient(app)
        
        # Test health check via docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        print("✅ API documentation accessible")
        
        # Test /history endpoint
        response = client.get("/history")
        assert response.status_code == 200
        history = response.json()
        assert isinstance(history, list)
        print("✅ History endpoint working")
        
        # Test /chat endpoint with mocked AI
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Integration test AI response"
            
            response = client.post("/chat", json={"user_message": "Integration test"})
            assert response.status_code == 200
            
            data = response.json()
            assert data["user_message"] == "Integration test"
            assert data["bot_response"] == "Integration test AI response"
            assert "timestamp" in data
            print("✅ Chat endpoint working with mocked AI")
        
        return True
    except Exception as e:
        print(f"❌ API integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_end_to_end_flow():
    """Test complete end-to-end flow"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        
        print("Testing end-to-end flow...")
        
        client = TestClient(app)
        
        # Get initial history count
        initial_response = client.get("/history")
        initial_count = len(initial_response.json())
        
        # Send a chat message
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "End-to-end test response"
            
            chat_response = client.post("/chat", json={
                "user_message": "End-to-end test message"
            })
            assert chat_response.status_code == 200
            
            chat_data = chat_response.json()
            assert chat_data["user_message"] == "End-to-end test message"
            assert chat_data["bot_response"] == "End-to-end test response"
        
        # Verify message was saved to database
        final_response = client.get("/history")
        final_count = len(final_response.json())
        assert final_count > initial_count
        
        # Verify the message appears in history
        history = final_response.json()
        found_message = False
        for entry in history:
            if entry["user"] == "End-to-end test message":
                assert entry["bot"] == "End-to-end test response"
                found_message = True
                break
        
        assert found_message, "Message not found in history"
        print("✅ End-to-end flow working correctly")
        
        return True
    except Exception as e:
        print(f"❌ End-to-end flow failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling across components"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        
        print("Testing error handling...")
        
        client = TestClient(app)
        
        # Test invalid JSON
        response = client.post("/chat", data="invalid json")
        assert response.status_code == 422
        print("✅ Invalid JSON handled correctly")
        
        # Test missing required field
        response = client.post("/chat", json={})
        assert response.status_code == 422
        print("✅ Missing required field handled correctly")
        
        # Test non-existent endpoint
        response = client.get("/nonexistent")
        assert response.status_code == 404
        print("✅ Non-existent endpoint handled correctly")
        
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== AI Chatbot Integration Testing ===")
    
    tests = [
        ("Database Integration", test_database_integration),
        ("AI Service Integration", test_ai_service_integration),
        ("API Integration", test_api_integration),
        ("End-to-End Flow", test_end_to_end_flow),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n=== Integration Test Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL INTEGRATION TESTS PASSED' if all_passed else '❌ SOME INTEGRATION TESTS FAILED'}")
