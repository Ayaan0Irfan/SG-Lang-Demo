#!/usr/bin/env python3
"""
Quick Demo - Test core RAG functionality
Demonstrates document loading, indexing, and querying
"""

import sys
from pathlib import Path

# Add src to path  
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem
import time

def main():
    """Run a quick demonstration of RAG capabilities"""
    print("🚀 SGLang RAG System - Quick Demo")
    print("=" * 50)
    
    # Initialize system
    print("🔧 Initializing RAG system...")
    rag = RAGSystem()
    rag.load_documents()
    rag.build_index()
    
    # Test queries
    test_queries = [
        "What is the vacation policy?",
        "How do I troubleshoot API errors?", 
        "What are the key principles of machine learning?"
    ]
    
    print(f"\n🧪 Testing with {len(test_queries)} sample queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        
        start_time = time.time()
        response = rag.query(query)
        elapsed = time.time() - start_time
        
        print(f"📝 Response ({elapsed:.2f}s): {response[:200]}...")
        
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()
