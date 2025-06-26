#!/usr/bin/env python3
"""
Script that builds static documentation using MkDocs or serves it locally for development
"""

import subprocess
import sys
import argparse
from pathlib import Path

def build_docs(serve=False, clean=False):
    """Runs MkDocs build or serve command based on parameters"""
    
    docs_dir = Path(__file__).parent.parent / "docs"
    
    if not docs_dir.exists():
        print("❌ docs/ directory not found")
        return False
    
    # Change to docs directory
    import os
    os.chdir(docs_dir)
    
    try:
        if clean:
            print("🧹 Cleaning previous build...")
            subprocess.run([sys.executable, "-m", "mkdocs", "clean"], check=True)
        
        if serve:
            print("🌐 Starting documentation server...")
            print("📖 Documentation will be available at: http://localhost:8000")
            subprocess.run([sys.executable, "-m", "mkdocs", "serve"], check=True)
        else:
            print("🔨 Building documentation...")
            subprocess.run([sys.executable, "-m", "mkdocs", "build"], check=True)
            print("✅ Documentation built successfully!")
            print("📁 Output in: docs/site/")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building documentation: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Documentation server stopped")
        return True

def main():
    parser = argparse.ArgumentParser(description="Build project documentation")
    parser.add_argument("--serve", action="store_true", 
                       help="Serve documentation locally")
    parser.add_argument("--clean", action="store_true",
                       help="Clean previous build")
    
    args = parser.parse_args()
    
    print("📚 SGLang RAG Documentation Builder")
    print("=" * 40)
    
    success = build_docs(serve=args.serve, clean=args.clean)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
