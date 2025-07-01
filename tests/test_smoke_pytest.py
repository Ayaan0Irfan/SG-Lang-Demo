import os
import pytest
from rag_system import RAGSystem

def test_rag_pipeline_basic_answer():
    rag = RAGSystem()
    rag.build_index(force_rebuild=True)
    result = rag.generate_answer("What is this?")
    assert isinstance(result, dict)
    assert "answer" in result
    assert len(result["sources"]) > 0

def test_rag_pipeline_empty_query():
    rag = RAGSystem()
    rag.build_index(force_rebuild=True)
    result = rag.generate_answer("")
    assert isinstance(result, dict)
    assert "answer" in result
    # Should still return a string answer, even if not informative
    assert isinstance(result["answer"], str)
