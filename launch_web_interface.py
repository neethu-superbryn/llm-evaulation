#!/usr/bin/env python3
"""
Launch script for the IntellAgent Web Interface
"""

import subprocess
import sys
import os

def check_virtual_env():
    """Check if we're in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def main():
    print("🚀 Starting IntellAgent Web Interface...")
    
    # Check if we're in virtual environment
    if not check_virtual_env():
        print("⚠️  Virtual environment not detected.")
        print("   Recommended: source venv/bin/activate")
        print("   Continuing anyway...")
    
    # Launch streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_interface.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down IntellAgent Web Interface")
    except Exception as e:
        print(f"❌ Error launching web interface: {e}")
        print("💡 Try running: source venv/bin/activate && python launch_web_interface.py")

if __name__ == "__main__":
    main()