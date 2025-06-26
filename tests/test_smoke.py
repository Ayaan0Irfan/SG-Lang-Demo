#!/usr/bin/env python3
"""
Smoke test that verifies basic document loading and query functionality with minimal test data
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem

def create_test_documents() -> Path:
    """Creates temporary directory with test documents containing known facts"""
    
    # Create temporary directory for test documents
    temp_dir = Path(tempfile.mkdtemp(prefix="smoke_test_"))
    
    # Document 1: Geography facts
    (temp_dir / "geography.txt").write_text("""
Geography Facts

France is a country in Western Europe. The capital of France is Paris, which is also its largest city.
Paris is located in the north-central part of France and has a population of over 2 million people.

Germany's capital is Berlin. Italy's capital is Rome. Spain's capital is Madrid.
""", encoding='utf-8')
    
    # Document 2: Company policies  
    (temp_dir / "policies.txt").write_text("""
Company Handbook

Vacation Policy:
- Employees are entitled to 20 vacation days per year
- Vacation requests must be submitted 2 weeks in advance
- Maximum of 5 consecutive vacation days without manager approval

Remote Work Policy:
- Remote work is allowed up to 3 days per week
- All remote work must be pre-approved by your manager
""", encoding='utf-8')
    
    # Document 3: Technical documentation
    (temp_dir / "technical.txt").write_text("""
API Documentation

Authentication:
The API uses Bearer token authentication. Include the token in the Authorization header.

Error Handling:
- 401: Invalid or missing authentication token
- 404: Resource not found  
- 500: Internal server error

Rate Limiting:
API calls are limited to 1000 requests per hour per API key.
""", encoding='utf-8')
    
    return temp_dir

def test_document_ingestion(rag_system: RAGSystem) -> bool:
    """Test that documents are properly loaded and indexed"""
    
    print("📄 Testing document ingestion...")
    
    # Load documents
    rag_system.load_documents()
    
    # Verify documents were loaded
    if len(rag_system.raw_documents) == 0:
        print("❌ FAIL: No documents loaded")
        return False
    
    print(f"✅ Loaded {len(rag_system.raw_documents)} documents")
    
    # Build index
    rag_system.build_index()
    
    # Verify index was built
    if not rag_system.vector_store.is_built:
        print("❌ FAIL: Vector index not built")
        return False
        
    if len(rag_system.chunks) == 0:
        print("❌ FAIL: No document chunks created")
        return False
    
    print(f"✅ Built index with {len(rag_system.chunks)} chunks")
    return True

def test_query_processing(rag_system: RAGSystem) -> bool:
    """Test that queries return relevant responses"""
    
    print("🧪 Testing query processing...")
    
    # Test cases: (query, expected_keywords)
    test_cases = [
        ("What is the capital of France?", ["paris", "france", "capital"]),
        ("How many vacation days do employees get?", ["vacation", "20", "days"]),
        ("What authentication does the API use?", ["bearer", "token", "authentication"])
    ]
    
    for i, (query, expected_keywords) in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {query} ---")
        
        try:
            response = rag_system.query(query)
            
            if not response:
                print(f"❌ FAIL: Empty response for query: {query}")
                return False
            
            if len(response) < 20:
                print(f"❌ FAIL: Response too short ({len(response)} chars): {response}")
                return False
            
            # Check if response contains expected keywords
            response_lower = response.lower()
            found_keywords = [kw for kw in expected_keywords if kw in response_lower]
            
            if len(found_keywords) == 0:
                print(f"❌ FAIL: Response doesn't contain any expected keywords")
                print(f"   Expected: {expected_keywords}")
                print(f"   Response: {response[:100]}...")
                return False
            
            print(f"✅ PASS: Found keywords {found_keywords}")
            print(f"   Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ FAIL: Exception during query: {e}")
            return False
    
    return True

def test_vector_similarity_search(rag_system: RAGSystem) -> bool:
    """Test that vector similarity search finds relevant chunks"""
    
    print("🔍 Testing vector similarity search...")
    
    test_queries = [
        ("Paris France capital", "geography"),
        ("vacation policy days", "policies"), 
        ("API authentication bearer", "technical")
    ]
    
    for query, expected_source in test_queries:
        try:
            # Get similar chunks
            similar_chunks = rag_system.vector_store.similarity_search(query, k=3)
            
            if not similar_chunks:
                print(f"❌ FAIL: No similar chunks found for: {query}")
                return False
            
            # Check if at least one chunk is from expected source
            found_expected = any(expected_source in chunk.source.lower() 
                               for chunk in similar_chunks)
            
            if not found_expected:
                print(f"❌ FAIL: No chunks from expected source '{expected_source}'")
                print(f"   Found sources: {[chunk.source for chunk in similar_chunks]}")
                return False
            
            print(f"✅ PASS: Found relevant chunks for '{query}'")
            
        except Exception as e:
            print(f"❌ FAIL: Exception during similarity search: {e}")
            return False
    
    return True

def run_smoke_test() -> bool:
    """Run complete smoke test suite"""
    
    print("🔥 Starting RAG System Smoke Test")
    print("=" * 50)
    
    # Create test documents
    print("🏗️  Setting up test environment...")
    test_docs_dir = create_test_documents()
    
    try:
        # Initialize RAG system with test documents
        rag = RAGSystem()
        rag.documents_dir = test_docs_dir  # Override documents directory
        
        # Run tests
        tests = [
            ("Document Ingestion", test_document_ingestion),
            ("Vector Similarity Search", test_vector_similarity_search), 
            ("Query Processing", test_query_processing),
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            print(f"\n🧪 Running {test_name} Test...")
            try:
                passed = test_func(rag)
                if not passed:
                    all_passed = False
                    print(f"❌ {test_name} test FAILED")
                else:
                    print(f"✅ {test_name} test PASSED")
            except Exception as e:
                print(f"❌ {test_name} test FAILED with exception: {e}")
                all_passed = False
        
        return all_passed
        
    finally:
        # Cleanup test documents
        print(f"\n🧹 Cleaning up test documents...")
        shutil.rmtree(test_docs_dir, ignore_errors=True)

def main():
    """Main entry point"""
    
    success = run_smoke_test()
    
    if success:
        print("\n🎉 ALL SMOKE TESTS PASSED!")
        print("✅ RAG system is working correctly")
        sys.exit(0)
    else:
        print("\n💥 SMOKE TESTS FAILED!")
        print("❌ RAG system has issues that need to be fixed")
        sys.exit(1)

if __name__ == "__main__":
    main()
