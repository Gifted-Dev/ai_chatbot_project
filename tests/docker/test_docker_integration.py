#!/usr/bin/env python3
"""
Comprehensive Docker integration test for AI Chatbot project
Tests the entire Docker stack including frontend-backend integration
"""

import subprocess
import time
import requests
import sys
import os
import json
from datetime import datetime

class DockerIntegrationTester:
    def __init__(self):
        self.base_url_backend = "http://localhost:8000"
        self.base_url_frontend = "http://localhost:8501"
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def run_command(self, command, timeout=30):
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
    
    def test_docker_prerequisites(self):
        """Test Docker and Docker Compose installation"""
        print("\n--- Testing Docker Prerequisites ---")
        
        # Test Docker
        success, stdout, stderr = self.run_command("docker --version")
        if success:
            version = stdout.strip()
            self.log_test("Docker Installation", True, f"Found: {version}")
        else:
            self.log_test("Docker Installation", False, "Docker not found or not running")
            return False
        
        # Test Docker Compose
        success, stdout, stderr = self.run_command("docker-compose --version")
        if success:
            version = stdout.strip()
            self.log_test("Docker Compose Installation", True, f"Found: {version}")
        else:
            self.log_test("Docker Compose Installation", False, "Docker Compose not found")
            return False
            
        return True
    
    def test_docker_compose_config(self):
        """Test Docker Compose configuration"""
        print("\n--- Testing Docker Compose Configuration ---")
        
        success, stdout, stderr = self.run_command("docker-compose config")
        if success:
            self.log_test("Docker Compose Config", True, "Configuration is valid")
            return True
        else:
            self.log_test("Docker Compose Config", False, f"Config error: {stderr}")
            return False
    
    def test_environment_setup(self):
        """Test environment configuration"""
        print("\n--- Testing Environment Setup ---")
        
        # Check .env file
        if os.path.exists(".env"):
            self.log_test("Environment File", True, ".env file found")
            
            # Check for required variables
            with open(".env", "r") as f:
                env_content = f.read()
            
            if "GROQ_API_KEY" in env_content and "your_groq_api_key_here" not in env_content:
                self.log_test("API Key Configuration", True, "GROQ_API_KEY is configured")
            else:
                self.log_test("API Key Configuration", False, "GROQ_API_KEY not properly configured")
                
        else:
            self.log_test("Environment File", False, ".env file not found")
            return False
            
        return True
    
    def test_docker_build_and_start(self):
        """Test Docker build and service startup"""
        print("\n--- Testing Docker Build and Startup ---")
        
        # Clean up any existing containers
        print("Cleaning up existing containers...")
        self.run_command("docker-compose down -v", timeout=60)
        
        # Build and start services
        print("Building and starting services...")
        success, stdout, stderr = self.run_command("docker-compose up --build -d", timeout=300)
        
        if success:
            self.log_test("Docker Build and Start", True, "Services started successfully")
        else:
            self.log_test("Docker Build and Start", False, f"Failed to start: {stderr}")
            return False
        
        # Wait for services to be ready
        print("Waiting for services to initialize...")
        time.sleep(45)  # Give services time to start
        
        return True
    
    def test_service_health(self):
        """Test individual service health"""
        print("\n--- Testing Service Health ---")
        
        # Check service status
        success, stdout, stderr = self.run_command("docker-compose ps")
        print("Service Status:")
        print(stdout)
        
        # Test database health
        success, stdout, stderr = self.run_command(
            "docker-compose exec -T database pg_isready -U chatbot_user -d chatbot_db"
        )
        self.log_test("Database Health", success, "PostgreSQL is ready" if success else "Database not ready")
        
        # Test backend health
        try:
            response = requests.get(f"{self.base_url_backend}/docs", timeout=10)
            if response.status_code == 200:
                self.log_test("Backend Health", True, f"Backend responding on {self.base_url_backend}")
            else:
                self.log_test("Backend Health", False, f"Backend returned status {response.status_code}")
        except Exception as e:
            self.log_test("Backend Health", False, f"Cannot connect to backend: {e}")
        
        # Test frontend health
        try:
            response = requests.get(f"{self.base_url_frontend}/_stcore/health", timeout=10)
            if response.status_code == 200:
                self.log_test("Frontend Health", True, f"Frontend responding on {self.base_url_frontend}")
            else:
                self.log_test("Frontend Health", False, f"Frontend returned status {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Health", False, f"Cannot connect to frontend: {e}")
        
        return True
    
    def test_api_functionality(self):
        """Test API functionality"""
        print("\n--- Testing API Functionality ---")
        
        # Test chat endpoint
        try:
            test_message = "Hello, this is a Docker integration test. Please respond briefly."
            response = requests.post(
                f"{self.base_url_backend}/chat",
                json={"user_message": test_message},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if "bot_response" in data and "timestamp" in data:
                    self.log_test("Chat API", True, f"Chat API working, response length: {len(data['bot_response'])}")
                else:
                    self.log_test("Chat API", False, "Invalid response format")
            else:
                self.log_test("Chat API", False, f"Chat API returned status {response.status_code}")
                
        except Exception as e:
            self.log_test("Chat API", False, f"Chat API error: {e}")
        
        # Test history endpoint
        try:
            response = requests.get(f"{self.base_url_backend}/history", timeout=10)
            if response.status_code == 200:
                history = response.json()
                self.log_test("History API", True, f"History API working, {len(history)} entries")
            else:
                self.log_test("History API", False, f"History API returned status {response.status_code}")
        except Exception as e:
            self.log_test("History API", False, f"History API error: {e}")
        
        return True
    
    def test_frontend_backend_integration(self):
        """Test frontend-backend integration"""
        print("\n--- Testing Frontend-Backend Integration ---")
        
        # Test if frontend can reach backend
        try:
            # This tests the internal Docker networking
            success, stdout, stderr = self.run_command(
                "docker-compose exec -T frontend curl -f http://backend:8000/docs"
            )
            self.log_test("Internal Network", success, "Frontend can reach backend via Docker network" if success else "Network connectivity issue")
        except Exception as e:
            self.log_test("Internal Network", False, f"Network test failed: {e}")
        
        # Test frontend accessibility
        try:
            response = requests.get(self.base_url_frontend, timeout=10)
            if response.status_code == 200:
                self.log_test("Frontend Accessibility", True, "Frontend is accessible from host")
            else:
                self.log_test("Frontend Accessibility", False, f"Frontend returned status {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Accessibility", False, f"Cannot access frontend: {e}")
        
        return True
    
    def test_data_persistence(self):
        """Test data persistence"""
        print("\n--- Testing Data Persistence ---")
        
        # Send a test message
        test_message = f"Persistence test message at {datetime.now().isoformat()}"
        try:
            response = requests.post(
                f"{self.base_url_backend}/chat",
                json={"user_message": test_message},
                timeout=30
            )
            
            if response.status_code == 200:
                # Check if message appears in history
                time.sleep(2)  # Wait for database write
                history_response = requests.get(f"{self.base_url_backend}/history", timeout=10)
                
                if history_response.status_code == 200:
                    history = history_response.json()
                    found = any(entry.get("user") == test_message for entry in history)
                    self.log_test("Data Persistence", found, "Message persisted in database" if found else "Message not found in history")
                else:
                    self.log_test("Data Persistence", False, "Could not retrieve history")
            else:
                self.log_test("Data Persistence", False, "Could not send test message")
                
        except Exception as e:
            self.log_test("Data Persistence", False, f"Persistence test failed: {e}")
        
        return True
    
    def cleanup(self):
        """Clean up Docker resources"""
        print("\n--- Cleaning Up ---")
        success, stdout, stderr = self.run_command("docker-compose down", timeout=60)
        if success:
            print("✅ Docker services stopped")
        else:
            print(f"⚠️ Cleanup warning: {stderr}")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("🧪 DOCKER INTEGRATION TEST REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": (passed_tests/total_tests)*100
            },
            "tests": self.test_results
        }
        
        with open("docker_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: docker_test_report.json")
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🐳 Starting Docker Integration Tests...")
        
        try:
            # Run test suite
            self.test_docker_prerequisites()
            self.test_docker_compose_config()
            self.test_environment_setup()
            self.test_docker_build_and_start()
            self.test_service_health()
            self.test_api_functionality()
            self.test_frontend_backend_integration()
            self.test_data_persistence()
            
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrupted by user")
        except Exception as e:
            print(f"\n❌ Test suite failed with exception: {e}")
        finally:
            self.cleanup()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = DockerIntegrationTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
