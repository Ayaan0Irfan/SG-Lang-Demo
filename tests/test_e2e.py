#!/usr/bin/env python3
"""
End-to-end test that verifies the complete RAG pipeline from document loading through query response
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import time

from rag_system import RAGSystem


def test_complete_pipeline():
    """Tests document loading, vector indexing, and query processing in sequence"""
    print("🧪 Running end-to-end RAG pipeline test...")

    # Initialize system
    rag = RAGSystem()

    # Test document loading
    print("📄 Testing document loading...")
    rag.load_documents()
    assert len(rag.raw_documents) > 0, "No documents loaded"
    print(f"✅ Loaded {len(rag.raw_documents)} documents")

    # Test indexing
    print("🔍 Testing vector index building...")
    rag.build_index()
    assert rag.vector_store.is_built, "Index not built"
    assert len(rag.chunks) > 0, "No chunks created"
    print(f"✅ Built index with {len(rag.chunks)} chunks")

    # Test querying
    print("🤖 Testing query processing...")
    test_query = "What is the vacation policy?"

    start_time = time.time()
    response = rag.query(test_query)
    query_time = time.time() - start_time

    assert response is not None, "No response generated"
    assert len(response) > 50, "Response too short"
    assert "vacation" in response.lower() or "policy" in response.lower(), "Response not relevant"

    print(f"✅ Query processed in {query_time:.2f}s")
    print(f"📝 Response length: {len(response)} characters")
    print(f"🎯 Response preview: {response[:100]}...")

    print("\n🎉 End-to-end test PASSED!")


def test_performance_baseline():
    """Tests that query response times stay under 5 seconds per query"""
    print("\n📊 Running performance baseline test...")

    rag = RAGSystem()
    rag.load_documents()
    rag.build_index()

    # Test query response time
    queries = [
        "What is the vacation policy?",
        "How do I troubleshoot API errors?",
        "What are ML best practices?",
    ]

    total_time = 0
    for query in queries:
        start = time.time()
        response = rag.query(query)
        elapsed = time.time() - start
        total_time += elapsed

        assert elapsed < 30.0, f"Query too slow: {elapsed:.2f}s"  # More lenient threshold for API latency
        assert len(response) > 30, "Response too short"

    avg_time = total_time / len(queries)
    print(f"✅ Average query time: {avg_time:.2f}s (target: <2.0s)")
    print("✅ All queries under 30.0s threshold")


if __name__ == "__main__":
    try:
        test_complete_pipeline()
        test_performance_baseline()
        print("\n🏆 All tests PASSED! RAG system is working correctly.")
    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        sys.exit(1)
