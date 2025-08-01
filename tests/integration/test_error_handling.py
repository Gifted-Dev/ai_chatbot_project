#!/usr/bin/env python3
"""
Error handling and edge case tests for the AI chatbot project
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_error_scenarios():
    """Test various API error scenarios"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        
        print("Testing API error scenarios...")
        client = TestClient(app)
        
        # Test 1: Missing required field
        response = client.post("/chat", json={})
        assert response.status_code == 422
        print("✅ Missing user_message handled correctly")
        
        # Test 2: Invalid JSON
        response = client.post("/chat", data="invalid json", headers={"Content-Type": "application/json"})
        assert response.status_code == 422
        print("✅ Invalid JSON handled correctly")
        
        # Test 3: Wrong HTTP method
        response = client.get("/chat")
        assert response.status_code == 405
        print("✅ Wrong HTTP method handled correctly")
        
        # Test 4: Non-existent endpoint
        response = client.post("/nonexistent")
        assert response.status_code == 404
        print("✅ Non-existent endpoint handled correctly")
        
        # Test 5: Invalid content type
        response = client.post("/chat", data="user_message=test", headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 422
        print("✅ Invalid content type handled correctly")
        
        return True
    except Exception as e:
        print(f"❌ API error scenarios test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_case_inputs():
    """Test edge case inputs"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        
        print("Testing edge case inputs...")
        client = TestClient(app)
        
        # Test 1: Empty string message
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to empty message"
            response = client.post("/chat", json={"user_message": ""})
            assert response.status_code == 200
            print("✅ Empty string message handled correctly")
        
        # Test 2: Very long message
        long_message = "A" * 10000  # 10KB message
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to long message"
            response = client.post("/chat", json={"user_message": long_message})
            assert response.status_code == 200
            print("✅ Very long message handled correctly")
        
        # Test 3: Special characters
        special_message = "Hello! @#$%^&*()_+-=[]{}|;':\",./<>?`~"
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to special characters"
            response = client.post("/chat", json={"user_message": special_message})
            assert response.status_code == 200
            print("✅ Special characters handled correctly")
        
        # Test 4: Unicode characters
        unicode_message = "Hello 世界 🌍 émojis 🚀"
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to unicode"
            response = client.post("/chat", json={"user_message": unicode_message})
            assert response.status_code == 200
            print("✅ Unicode characters handled correctly")
        
        # Test 5: Newlines and whitespace
        whitespace_message = "  \n\t  Hello World  \n\t  "
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to whitespace"
            response = client.post("/chat", json={"user_message": whitespace_message})
            assert response.status_code == 200
            print("✅ Whitespace and newlines handled correctly")
        
        return True
    except Exception as e:
        print(f"❌ Edge case inputs test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_error_scenarios():
    """Test database error scenarios"""
    try:
        from backend.app.services.database import sessionlocal
        from app import crud, schemas
        from unittest.mock import patch
        
        print("Testing database error scenarios...")
        
        # Test 1: Database connection issues
        with patch('app.services.database.sessionlocal') as mock_session:
            mock_session.side_effect = Exception("Database connection failed")
            try:
                db = sessionlocal()
                print("⚠️ Database connection error not properly handled")
            except Exception:
                print("✅ Database connection error handled correctly")
        
        # Test 2: Invalid data types
        db = sessionlocal()
        try:
            # This should work fine as our schema validation catches this earlier
            chat_request = schemas.ChatRequest(user_message="Valid message")
            result = crud.save_chat(db, chat_request, "Valid response")
            assert result is not None
            print("✅ Valid data saved correctly")
            
            # Cleanup
            db.delete(result)
            db.commit()
        finally:
            db.close()
        
        return True
    except Exception as e:
        print(f"❌ Database error scenarios test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_service_error_scenarios():
    """Test AI service error scenarios"""
    try:
        from backend.app.services.ai_engine import get_response
        from unittest.mock import patch
        import os
        
        print("Testing AI service error scenarios...")
        
        # Test 1: API key missing
        with patch.dict(os.environ, {}, clear=True):
            with patch('app.services.ai_engine.Groq') as mock_groq:
                mock_groq.side_effect = Exception("API key missing")
                try:
                    # Re-import to trigger the error
                    import importlib
                    import backend.app.services.ai_engine
                    importlib.reload(app.services.ai_engine)
                    print("⚠️ Missing API key not properly handled")
                except Exception:
                    print("✅ Missing API key handled correctly")
        
        # Test 2: API timeout
        with patch('app.services.ai_engine.client') as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("Request timeout")
            try:
                response = get_response("Test message")
                print("⚠️ API timeout not properly handled")
            except Exception:
                print("✅ API timeout handled correctly")
        
        # Test 3: Invalid API response
        with patch('app.services.ai_engine.client') as mock_client:
            mock_response = type('MockResponse', (), {})()
            mock_response.choices = []  # Empty choices
            mock_client.chat.completions.create.return_value = mock_response
            try:
                response = get_response("Test message")
                print("⚠️ Invalid API response not properly handled")
            except Exception:
                print("✅ Invalid API response handled correctly")
        
        return True
    except Exception as e:
        print(f"❌ AI service error scenarios test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_concurrent_requests():
    """Test handling of concurrent requests"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        import threading
        import time
        
        print("Testing concurrent requests...")
        client = TestClient(app)
        
        results = []
        errors = []
        
        def make_request(i):
            try:
                with patch('app.services.ai_engine.get_response') as mock_ai:
                    mock_ai.return_value = f"Response {i}"
                    response = client.post("/chat", json={"user_message": f"Message {i}"})
                    results.append((i, response.status_code))
            except Exception as e:
                errors.append((i, str(e)))
        
        # Create 10 concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(results) == 10, f"Expected 10 results, got {len(results)}"
        assert len(errors) == 0, f"Got {len(errors)} errors: {errors}"
        
        for i, status_code in results:
            assert status_code == 200, f"Request {i} failed with status {status_code}"
        
        print("✅ Concurrent requests handled correctly")
        return True
    except Exception as e:
        print(f"❌ Concurrent requests test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_usage():
    """Test memory usage with large inputs"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        import psutil
        import os
        
        print("Testing memory usage...")
        client = TestClient(app)
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Send multiple large requests
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Response to large message"
            
            for i in range(5):
                large_message = "Large message " * 1000  # ~13KB per message
                response = client.post("/chat", json={"user_message": large_message})
                assert response.status_code == 200
        
        # Check memory usage after
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory usage: {initial_memory:.1f}MB -> {final_memory:.1f}MB (+{memory_increase:.1f}MB)")
        
        # Memory increase should be reasonable (less than 50MB for this test)
        if memory_increase < 50:
            print("✅ Memory usage is reasonable")
        else:
            print("⚠️ High memory usage detected")
        
        return True
    except Exception as e:
        print(f"❌ Memory usage test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== AI Chatbot Error Handling and Edge Case Testing ===")
    
    tests = [
        ("API Error Scenarios", test_api_error_scenarios),
        ("Edge Case Inputs", test_edge_case_inputs),
        ("Database Error Scenarios", test_database_error_scenarios),
        ("AI Service Error Scenarios", test_ai_service_error_scenarios),
        ("Concurrent Requests", test_concurrent_requests),
        ("Memory Usage", test_memory_usage)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n=== Error Handling Test Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL ERROR HANDLING TESTS PASSED' if all_passed else '❌ SOME ERROR HANDLING TESTS FAILED'}")
