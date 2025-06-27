"""
Streamlit Web Interface for SGLang RAG System
Professional web interface for the RAG application
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from config import config
from rag_system import RAGSystem, DocumentProcessor, VectorStore


def initialize_rag_system():
    """Initialize the RAG system with proper error handling"""
    try:
        # Create RAG system
        rag = RAGSystem()
        
        # Build index
        rag.build_index()
        
        return rag, None
    except Exception as e:
        return None, str(e)


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title=config.app_name,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title(f"🤖 {config.app_name}")
    st.markdown(f"*Version {config.app_version}*")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Provider selection
        provider = st.selectbox(
            "LLM Provider",
            options=["groq", "together"],
            index=0 if config.default_provider == "groq" else 1
        )
        
        # Temperature setting
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=config.temperature,
            step=0.1
        )
        
        # Max tokens
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=50,
            max_value=2000,
            value=config.max_tokens,
            step=50
        )
        
        st.markdown("---")
        st.subheader("System Info")
        st.text(f"Host: {config.web_host}")
        st.text(f"Port: {config.web_port}")
        st.text(f"Embedding: {config.embedding_model}")
        st.text(f"Chunk Size: {config.chunk_size}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Ask a Question")
        
        # Initialize RAG system
        if 'rag_system' not in st.session_state:
            with st.spinner("Initializing RAG system..."):
                rag, error = initialize_rag_system()
                if error:
                    st.error(f"Failed to initialize RAG system: {error}")
                    st.stop()
                st.session_state.rag_system = rag
                st.success("RAG system initialized successfully!")
        
        # Query input
        query = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="Ask anything about the documents..."
        )
        
        # Process query
        if st.button("🔍 Get Answer", type="primary"):
            if query.strip():
                with st.spinner("Processing your question..."):
                    try:
                        # Update RAG system settings (note: these are passed to generate_answer)
                        # rag.provider = provider  # Not needed, passed as parameter
                        
                        # Get response
                        response = rag.generate_answer(query, provider)
                        
                        # Display results
                        st.subheader("📝 Answer")
                        st.write(response.get('answer', 'No answer generated'))
                        
                        # Show sources if available
                        if 'sources' in response and response['sources']:
                            st.subheader("📚 Sources")
                            for i, source in enumerate(response['sources'], 1):
                                with st.expander(f"Source {i}"):
                                    st.text(source.get('content', 'No content'))
                                    if 'metadata' in source:
                                        st.caption(f"File: {source['metadata'].get('source', 'Unknown')}")
                        
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")
            else:
                st.warning("Please enter a question first.")
    
    with col2:
        st.subheader("📊 System Status")
        
        # System metrics (placeholder)
        if st.button("🔄 Refresh Status"):
            try:
                # Document count
                docs_path = Path("data/documents")
                if docs_path.exists():
                    doc_count = len(list(docs_path.glob("*.txt")))
                    st.metric("Documents", doc_count)
                else:
                    st.metric("Documents", 0)
                
                # Vector store status
                st.metric("Vector Store", "Active" if 'rag_system' in st.session_state else "Not Loaded")
                
                # Configuration
                st.metric("Provider", provider.upper())
                st.metric("Temperature", f"{temperature:.1f}")
                
            except Exception as e:
                st.error(f"Error getting status: {str(e)}")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🔨 Rebuild Index"):
            with st.spinner("Rebuilding vector index..."):
                try:
                    # Reinitialize RAG system to rebuild index
                    rag, error = initialize_rag_system()
                    if error:
                        st.error(f"Failed to rebuild index: {error}")
                    else:
                        st.session_state.rag_system = rag
                        st.success("Index rebuilt successfully!")
                except Exception as e:
                    st.error(f"Error rebuilding index: {str(e)}")
        
        if st.button("📁 Show Documents"):
            try:
                docs_path = Path("data/documents")
                if docs_path.exists():
                    files = list(docs_path.glob("*.txt"))
                    if files:
                        st.write("Available documents:")
                        for file in files:
                            st.text(f"• {file.name}")
                    else:
                        st.info("No documents found in data/documents/")
                else:
                    st.warning("Documents directory not found")
            except Exception as e:
                st.error(f"Error listing documents: {str(e)}")


if __name__ == "__main__":
    main()
