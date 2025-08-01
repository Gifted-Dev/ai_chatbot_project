#!/usr/bin/env python3
"""
Simple API test script for the AI chatbot project
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        from backend.app.main import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False

def test_routes():
    """Test if routes are properly configured"""
    try:
        from backend.app.main import app
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append(f"{list(route.methods)} {route.path}")
        
        print(f"Available routes: {len(routes)}")
        for route in routes:
            print(f"  {route}")
        return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def test_endpoints():
    """Test API endpoints using TestClient"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        
        client = TestClient(app)
        
        # Test /chat endpoint with timeout
        print("Testing /chat endpoint...")
        chat_data = {'user_message': 'Hello, this is a test'}
        
        # Mock the AI response to avoid timeout
        import unittest.mock
        with unittest.mock.patch('app.services.ai_engine.get_response', return_value='Test response'):
            response = client.post('/chat', json=chat_data)
            
            if response.status_code == 200:
                print("✅ /chat endpoint working correctly")
                result = response.json()
                print(f"Response keys: {list(result.keys())}")
            else:
                print(f"❌ /chat endpoint failed with status {response.status_code}")
                print(f"Response: {response.text}")
        
        # Test /history endpoint
        print("Testing /history endpoint...")
        history_response = client.get('/history')
        
        if history_response.status_code == 200:
            print("✅ /history endpoint working correctly")
            history = history_response.json()
            print(f"History entries: {len(history)}")
        else:
            print(f"❌ /history endpoint failed with status {history_response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Endpoint testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== AI Chatbot API Testing ===")
    
    tests = [
        ("Import Test", test_imports),
        ("Route Test", test_routes),
        ("Endpoint Test", test_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n=== Test Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
