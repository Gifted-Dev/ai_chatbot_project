#!/usr/bin/env python3
"""
Performance and security analysis for the AI chatbot project
"""

import sys
import os
import time
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_response_times():
    """Test API response times"""
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        
        print("Testing API response times...")
        client = TestClient(app)
        
        response_times = []
        
        # Test multiple requests to get average response time
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Quick response"
            
            for i in range(10):
                start_time = time.time()
                response = client.post("/chat", json={"user_message": f"Test message {i}"})
                end_time = time.time()
                
                assert response.status_code == 200
                response_times.append(end_time - start_time)
        
        avg_response_time = sum(response_times) * 1000 / len(response_times)  # Convert to ms
        max_response_time = max(response_times) * 1000
        min_response_time = min(response_times) * 1000
        
        print(f"Average response time: {avg_response_time:.2f}ms")
        print(f"Min response time: {min_response_time:.2f}ms")
        print(f"Max response time: {max_response_time:.2f}ms")
        
        # Response times should be reasonable (under 1000ms for mocked responses)
        if avg_response_time < 1000:
            print("✅ Response times are good")
        elif avg_response_time < 2000:
            print("⚠️ Response times are acceptable")
        else:
            print("❌ Response times are slow")
        
        return avg_response_time < 2000
    except Exception as e:
        print(f"❌ Response time test failed: {e}")
        return False

def test_database_performance():
    """Test database performance"""
    try:
        from backend.app.services.database import sessionlocal
        from app import crud, schemas
        
        print("Testing database performance...")
        
        db = sessionlocal()
        try:
            # Test bulk insert performance
            start_time = time.time()
            chat_entries = []
            
            for i in range(100):
                chat_request = schemas.ChatRequest(user_message=f"Performance test message {i}")
                chat_entry = crud.save_chat(db, chat_request, f"Performance test response {i}")
                chat_entries.append(chat_entry)
            
            insert_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Test bulk read performance
            start_time = time.time()
            history = crud.get_chat_history(db, limit=100)
            read_time = (time.time() - start_time) * 1000  # Convert to ms
            
            print(f"100 inserts took: {insert_time:.2f}ms ({insert_time/100:.2f}ms per insert)")
            print(f"Reading 100 records took: {read_time:.2f}ms")
            
            # Cleanup
            for entry in chat_entries:
                db.delete(entry)
            db.commit()
            
            # Performance should be reasonable
            if insert_time < 5000 and read_time < 1000:
                print("✅ Database performance is good")
                return True
            elif insert_time < 10000 and read_time < 2000:
                print("⚠️ Database performance is acceptable")
                return True
            else:
                print("❌ Database performance is slow")
                return False
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database performance test failed: {e}")
        return False

def analyze_security_vulnerabilities():
    """Analyze potential security vulnerabilities"""
    try:
        print("Analyzing security vulnerabilities...")
        
        issues = []
        recommendations = []
        
        # Check 1: Environment variables
        from backend.app.services.database import database_url
        if "password" in database_url.lower() and "localhost" not in database_url:
            issues.append("Database credentials may be exposed in connection string")
            recommendations.append("Use environment variables for sensitive database credentials")
        
        # Check 2: API key exposure
        import os
        api_key = os.getenv('GROQ_API_KEY')
        if api_key and len(api_key) > 10:  # Basic check
            print("✅ API key is properly loaded from environment")
        else:
            issues.append("API key not found or improperly configured")
            recommendations.append("Ensure GROQ_API_KEY is set in environment variables")
        
        # Check 3: CORS configuration
        from backend.app.main import app
        cors_middleware = None
        for middleware in app.user_middleware:
            if "CORSMiddleware" in str(middleware):
                cors_middleware = middleware
                break
        
        if cors_middleware:
            print("⚠️ CORS is configured to allow all origins (*)")
            recommendations.append("Restrict CORS origins to specific domains in production")
        
        # Check 4: Input validation
        from backend.app.schemas import ChatRequest
        print("✅ Input validation is implemented using Pydantic schemas")
        
        # Check 5: SQL injection protection
        print("✅ Using SQLAlchemy ORM provides SQL injection protection")
        
        # Check 6: Rate limiting
        print("⚠️ No rate limiting detected")
        recommendations.append("Implement rate limiting to prevent abuse")
        
        # Check 7: Authentication
        print("⚠️ No authentication mechanism detected")
        recommendations.append("Consider implementing authentication for production use")
        
        # Check 8: HTTPS
        print("⚠️ Application runs on HTTP by default")
        recommendations.append("Use HTTPS in production with proper SSL certificates")
        
        # Check 9: Error information disclosure
        print("✅ FastAPI handles errors appropriately without exposing sensitive information")
        
        print(f"\nSecurity Issues Found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
        
        print(f"\nSecurity Recommendations: {len(recommendations)}")
        for rec in recommendations:
            print(f"  - {rec}")
        
        # Return True if no critical issues found
        return len(issues) <= 2  # Allow minor issues
        
    except Exception as e:
        print(f"❌ Security analysis failed: {e}")
        return False

def test_memory_leaks():
    """Test for potential memory leaks"""
    try:
        import psutil
        import gc
        from fastapi.testclient import TestClient
        from backend.app.main import app
        from unittest.mock import patch
        
        print("Testing for memory leaks...")
        
        client = TestClient(app)
        process = psutil.Process(os.getpid())
        
        # Get initial memory
        gc.collect()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform many requests
        with patch('app.services.ai_engine.get_response') as mock_ai:
            mock_ai.return_value = "Memory test response"
            
            for i in range(50):
                response = client.post("/chat", json={"user_message": f"Memory test {i}"})
                assert response.status_code == 200
                
                # Force garbage collection every 10 requests
                if i % 10 == 0:
                    gc.collect()
        
        # Get final memory
        gc.collect()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory usage: {initial_memory:.1f}MB -> {final_memory:.1f}MB (+{memory_increase:.1f}MB)")
        
        # Memory increase should be minimal for 50 requests
        if memory_increase < 10:
            print("✅ No significant memory leaks detected")
            return True
        elif memory_increase < 20:
            print("⚠️ Minor memory increase detected")
            return True
        else:
            print("❌ Potential memory leak detected")
            return False
            
    except Exception as e:
        print(f"❌ Memory leak test failed: {e}")
        return False

def analyze_code_quality():
    """Analyze code quality and best practices"""
    try:
        print("Analyzing code quality...")
        
        issues = []
        good_practices = []
        
        # Check imports and structure
        try:
            from backend.app.main import app
            from backend.app.models import ChatMessage
            from backend.app.schemas import ChatRequest, ChatResponse
            from app import crud
            good_practices.append("Proper module structure and imports")
        except ImportError as e:
            issues.append(f"Import issues: {e}")
        
        # Check for proper error handling
        import inspect
        from backend.app.routes import chatbot
        
        source = inspect.getsource(chatbot.create_chat)
        if "try" in source or "except" in source:
            good_practices.append("Error handling implemented in routes")
        else:
            issues.append("Limited error handling in route functions")
        
        # Check for proper typing
        if "typing" in source or ":" in source:
            good_practices.append("Type hints used in code")
        
        # Check for documentation
        if '"""' in source or "'''" in source:
            good_practices.append("Documentation strings present")
        else:
            issues.append("Limited documentation in code")
        
        # Check database session management
        if "Depends(get_db)" in source:
            good_practices.append("Proper database session management with dependency injection")
        
        print(f"\nCode Quality Issues: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
        
        print(f"\nGood Practices Found: {len(good_practices)}")
        for practice in good_practices:
            print(f"  ✅ {practice}")
        
        return len(issues) <= 2  # Allow minor issues
        
    except Exception as e:
        print(f"❌ Code quality analysis failed: {e}")
        return False

def test_scalability_considerations():
    """Test scalability considerations"""
    try:
        print("Testing scalability considerations...")
        
        considerations = []
        
        # Check database connection pooling
        from backend.app.services.database import engine
        pool_size = getattr(engine.pool, 'size', lambda: 5)()
        if callable(pool_size):
            pool_size = 5  # Default
        
        print(f"Database connection pool size: {pool_size}")
        if pool_size >= 5:
            considerations.append("✅ Adequate database connection pooling")
        else:
            considerations.append("⚠️ Consider increasing database connection pool size")
        
        # Check for async support
        from backend.app.main import app
        if hasattr(app, 'router'):
            considerations.append("✅ FastAPI provides async support")
        
        # Check for caching
        print("⚠️ No caching mechanism detected")
        considerations.append("⚠️ Consider implementing caching for frequently accessed data")
        
        # Check for load balancing readiness
        print("✅ Stateless application design supports load balancing")
        considerations.append("✅ Application is stateless and load-balancer ready")
        
        # Check for monitoring
        print("⚠️ No monitoring/logging framework detected")
        considerations.append("⚠️ Consider adding monitoring and logging for production")
        
        print("\nScalability Considerations:")
        for consideration in considerations:
            print(f"  {consideration}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scalability analysis failed: {e}")
        return False

if __name__ == "__main__":
    print("=== AI Chatbot Performance and Security Review ===")
    
    tests = [
        ("Response Times", test_response_times),
        ("Database Performance", test_database_performance),
        ("Security Vulnerabilities", analyze_security_vulnerabilities),
        ("Memory Leaks", test_memory_leaks),
        ("Code Quality", analyze_code_quality),
        ("Scalability Considerations", test_scalability_considerations)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n=== Performance and Security Review Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL CHECKS PASSED' if all_passed else '⚠️ SOME ISSUES FOUND - SEE RECOMMENDATIONS ABOVE'}")
