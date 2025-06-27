#!/usr/bin/env python3
"""
Script that runs predefined queries against the RAG system to demonstrate basic functionality
"""

import sys
from pathlib import Path

# Add src to path  
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem
import time

def main():
    """Initializes RAG system and runs sample queries to show document retrieval and response generation"""
    print("🚀 SGLang RAG System - Quick Demo")
    print("=" * 50)
    
    # Initialize system
    print("🔧 Initializing RAG system...")
    rag = RAGSystem()
    rag.build_index()  # This handles document loading and index building
    
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
        response = rag.generate_answer(query)
        elapsed = time.time() - start_time
        
        print(f"📝 Response ({elapsed:.2f}s): {response.get('answer', 'No answer')[:200]}...")
        if response.get('sources'):
            print(f"📚 Sources: {len(response['sources'])} documents found")
        
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()
