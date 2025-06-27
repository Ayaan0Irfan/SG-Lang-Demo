#!/usr/bin/env python3
"""
Entry point that launches the Streamlit web interface for the RAG system
"""

import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import config


def main():
    """Launches Streamlit application with the web interface components"""
    print(f"[*] Starting {config.app_name} Web Interface")
    print(f"[*] Version: {config.app_version}")
    print(f"[*] Host: {config.web_host}")
    print(f"[*] Port: {config.web_port}")
    print()
    
    # Use the web app
    web_app_path = Path("src/web/app.py")
    if not web_app_path.exists():
        print("[!] Web app not found. Please ensure src/web/app.py exists.")
        return
    
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
        return


if __name__ == "__main__":
    main()
