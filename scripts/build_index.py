#!/usr/bin/env python3
"""
Index Builder Script
Script that processes documents in data/documents/ and creates a FAISS vector index for search
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem


def main():
    """Loads documents from data directory and builds searchable vector index"""
    print("🔧 Building vector index from documents...")
    start_time = time.time()
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Build index (this includes loading documents)
    print("📄 Building index (this includes loading documents)...")
    rag.build_index(force_rebuild=True)
    
    elapsed = time.time() - start_time
    print(f"✅ Index built successfully in {elapsed:.2f}s")
    
    # Show stats
    if hasattr(rag, '_show_stats'):
        print("\n📊 Index Statistics:")
        rag._show_stats()
    else:
        print(f"📊 Indexed {len(rag.vector_store.chunks) if rag.vector_store.chunks else 0} document chunks")
        print(f"💾 Index saved to: data/vector_index/")


if __name__ == "__main__":
    main()
