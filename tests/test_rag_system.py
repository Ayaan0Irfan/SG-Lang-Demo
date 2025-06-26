"""
Test Suite for RAG System
Professional testing for the core RAG components
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import VectorStore, DocumentChunk, LLMProvider, DocumentProcessor


class TestVectorStore:
    """Test the vector store functionality"""
    
    def test_vector_store_initialization(self):
        """Test vector store can be initialized"""
        store = VectorStore()
        assert store.dimension == 384  # MiniLM dimension
        assert not store.is_built
        assert len(store.chunks) == 0
    
    def test_document_chunk_creation(self):
        """Test document chunk data structure"""
        chunk = DocumentChunk(
            id="test123",
            text="This is a test document",
            source_file="test.txt",
            chunk_index=0,
            metadata={"word_count": 5}
        )
        
        assert chunk.id == "test123"
        assert chunk.text == "This is a test document"
        assert chunk.source_file == "test.txt"
        assert chunk.metadata["word_count"] == 5


class TestLLMProvider:
    """Test LLM provider functionality"""
    
    def test_llm_provider_initialization(self):
        """Test LLM provider can be initialized"""
        provider = LLMProvider()
        # Should initialize without errors
        assert provider is not None
    
    def test_provider_availability_check(self):
        """Test provider availability checking"""
        provider = LLMProvider()
        available_providers = provider.list_available_providers()
        # Should return a list (may be empty if no API keys)
        assert isinstance(available_providers, list)


class TestDocumentProcessor:
    """Test document processing functionality"""
    
    def test_document_processor_initialization(self):
        """Test document processor initialization"""
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        assert processor.chunk_size == 100
        assert processor.chunk_overlap == 20
    
    def test_text_chunking(self):
        """Test text chunking functionality"""
        processor = DocumentProcessor(chunk_size=5, chunk_overlap=1)
        
        # Create test text
        test_text = "This is a test document with more than five words for testing"
        chunks = processor._chunk_text(test_text, "test.txt")
        
        # Should create multiple chunks
        assert len(chunks) > 1
        
        # Each chunk should be a DocumentChunk
        for chunk in chunks:
            assert isinstance(chunk, DocumentChunk)
            assert chunk.source_file == "test.txt"
            assert len(chunk.text) > 0
    
    def test_text_preprocessing(self):
        """Test text preprocessing"""
        processor = DocumentProcessor()
        
        # Test text with extra whitespace
        messy_text = "This  has    extra\n\nwhitespace  \r\n  "
        clean_text = processor.preprocess_text(messy_text)
        
        assert clean_text == "This has extra whitespace"


# Integration test
class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.mark.integration
    def test_basic_workflow(self):
        """Test basic RAG workflow without external dependencies"""
        # Test document processing
        processor = DocumentProcessor(chunk_size=10, chunk_overlap=2)
        
        # Create test chunks
        test_text = "This is a comprehensive test of the RAG system functionality"
        chunks = processor._chunk_text(test_text, "test.txt")
        
        # Test vector store
        store = VectorStore()
        assert not store.is_built
        
        # Would test adding documents, but requires actual embeddings
        # store.add_documents(chunks)
        # assert store.is_built
        
        # Test that we can create the components
        llm = LLMProvider()
        assert llm is not None


if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])
