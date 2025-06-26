#!/usr/bin/env python3
"""
Script that processes documents in data/documents/ and creates a FAISS vector index for search
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem
import time

def main():
    """Loads documents from data directory and builds searchable vector index"""
    print("🔧 Building vector index from documents...")
    start_time = time.time()
    
    # Initialize RAG system (this will build the index)
    rag = RAGSystem()
    
    # Load documents and build index
    print("📄 Loading documents...")
    rag.load_documents()
    
    print("🔍 Building FAISS index...")
    rag.build_index()
    
    elapsed = time.time() - start_time
    print(f"✅ Index built successfully in {elapsed:.2f}s")
    print(f"📊 Indexed {len(rag.chunks)} document chunks")
    print(f"💾 Index saved to: data/vector_index/")

if __name__ == "__main__":
    main()
