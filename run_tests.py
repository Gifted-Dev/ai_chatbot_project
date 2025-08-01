#!/usr/bin/env python3
"""
Simple test runner for the AI Chatbot project
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run all tests"""
    print("🧪 Running AI Chatbot Tests...")

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Add backend to Python path
    backend_path = project_root / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    try:
        # Run all tests
        result = subprocess.run([
            "python", "-m", "pytest", "tests/", "-v"
        ], check=True)
        print("✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError:
        print("❌ Some tests failed!")
        return 1
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return 1

if __name__ == "__main__":
    sys.exit(main())
