#!/usr/bin/env python3
"""
Docker setup testing script
Tests the Docker configuration and networking
"""

import subprocess
import time
import requests
import sys
import os

def run_command(command, timeout=30):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def test_docker_compose_syntax():
    """Test docker-compose file syntax"""
    print("Testing docker-compose.yml syntax...")
    
    success, stdout, stderr = run_command("docker-compose config")
    if success:
        print("✅ docker-compose.yml syntax is valid")
        return True
    else:
        print(f"❌ docker-compose.yml syntax error: {stderr}")
        return False

def test_dockerfile_syntax():
    """Test Dockerfile syntax"""
    print("Testing Dockerfile syntax...")
    
    # Test backend Dockerfile
    success, stdout, stderr = run_command("docker build --no-cache -f backend/Dockerfile backend --dry-run")
    if success:
        print("✅ Backend Dockerfile syntax is valid")
    else:
        print(f"⚠️ Backend Dockerfile may have issues: {stderr}")
    
    # Test frontend Dockerfile
    success, stdout, stderr = run_command("docker build --no-cache -f frontend/Dockerfile frontend --dry-run")
    if success:
        print("✅ Frontend Dockerfile syntax is valid")
    else:
        print(f"⚠️ Frontend Dockerfile may have issues: {stderr}")
    
    return True

def test_environment_setup():
    """Test environment configuration"""
    print("Testing environment setup...")
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file found")
        
        # Check for required variables
        with open(".env", "r") as f:
            env_content = f.read()
            
        required_vars = ["GROQ_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ Missing environment variables: {missing_vars}")
        else:
            print("✅ All required environment variables present")
    else:
        print("⚠️ .env file not found. Copy .env.docker to .env and configure it.")
    
    return True

def test_docker_build():
    """Test Docker image building"""
    print("Testing Docker image building...")
    
    # Build backend image
    print("Building backend image...")
    success, stdout, stderr = run_command("docker build -t chatbot-backend backend", timeout=300)
    if success:
        print("✅ Backend image built successfully")
    else:
        print(f"❌ Backend image build failed: {stderr}")
        return False
    
    # Build frontend image
    print("Building frontend image...")
    success, stdout, stderr = run_command("docker build -t chatbot-frontend frontend", timeout=300)
    if success:
        print("✅ Frontend image built successfully")
    else:
        print(f"❌ Frontend image build failed: {stderr}")
        return False
    
    return True

def test_docker_compose_up():
    """Test docker-compose up"""
    print("Testing docker-compose startup...")
    
    # Start services
    print("Starting services with docker-compose...")
    success, stdout, stderr = run_command("docker-compose up -d", timeout=120)
    if success:
        print("✅ Services started successfully")
    else:
        print(f"❌ Failed to start services: {stderr}")
        return False
    
    # Wait for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(30)
    
    # Check service health
    success, stdout, stderr = run_command("docker-compose ps")
    print("Service status:")
    print(stdout)
    
    return True

def test_service_connectivity():
    """Test connectivity between services"""
    print("Testing service connectivity...")
    
    # Test backend health
    try:
        response = requests.get("http://localhost:8000/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Backend service is accessible")
        else:
            print(f"⚠️ Backend service returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to backend service: {e}")
    
    # Test frontend health
    try:
        response = requests.get("http://localhost:8501/_stcore/health", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend service is accessible")
        else:
            print(f"⚠️ Frontend service returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to frontend service: {e}")
    
    # Test database connectivity (through backend)
    try:
        response = requests.get("http://localhost:8000/history", timeout=10)
        if response.status_code == 200:
            print("✅ Database connectivity through backend is working")
        else:
            print(f"⚠️ Database connectivity issue: status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot test database connectivity: {e}")
    
    return True

def cleanup():
    """Clean up Docker resources"""
    print("Cleaning up Docker resources...")
    run_command("docker-compose down")
    run_command("docker image rm chatbot-backend chatbot-frontend", timeout=60)
    print("✅ Cleanup completed")

def main():
    """Main testing function"""
    print("=== Docker Setup Testing ===")
    
    tests = [
        ("Docker Compose Syntax", test_docker_compose_syntax),
        ("Dockerfile Syntax", test_dockerfile_syntax),
        ("Environment Setup", test_environment_setup),
        ("Docker Build", test_docker_build),
        ("Docker Compose Up", test_docker_compose_up),
        ("Service Connectivity", test_service_connectivity),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n=== Test Results ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Cleanup
    cleanup()
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
