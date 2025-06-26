#!/usr/bin/env python3
"""
Web Interface Entry Point
Start the Streamlit web application
"""

import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import config


def main():
    """Start the web interface"""
    print(f"[*] Starting {config.app_name} Web Interface")
    print(f"[*] Version: {config.app_version}")
    print(f"[*] Host: {config.web_host}")
    print(f"[*] Port: {config.web_port}")
    print()
    
    # Move streamlit app to web directory
    web_app_path = Path("src/web/app.py")
    if not web_app_path.exists():
        # Copy the existing streamlit app
        import shutil
        shutil.copy("streamlit_app.py", web_app_path)
    
    try:
        subprocess.run([
            "streamlit", "run", str(web_app_path),
            "--server.headless", "true",
            "--server.address", config.web_host,
            "--server.port", str(config.web_port)
        ])
    except KeyboardInterrupt:
        print("\n[*] Web interface stopped by user")
    except FileNotFoundError:
        print("[!] Streamlit not found. Please install with: pip install streamlit")
        print("[*] Falling back to legacy app...")
        subprocess.run([
            "streamlit", "run", "streamlit_app.py",
            "--server.headless", "true",
            "--server.address", config.web_host,
            "--server.port", str(config.web_port)
        ])


if __name__ == "__main__":
    main()
