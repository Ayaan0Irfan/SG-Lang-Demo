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
from rag_system import RAGSystem


def initialize_rag_system():
    """Initialize the RAG system with proper error handling"""
    try:
        rag = RAGSystem()
        rag.build_index()
        return rag, None
    except Exception as e:
        return None, str(e)


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title=config.app_name,
        page_icon="🤖",
        layout="wide"
    )
    
    # Header
    st.title(f"🤖 {config.app_name}")
    st.markdown(f"*Version {config.app_version}*")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        provider = st.selectbox(
            "LLM Provider",
            options=["groq", "together"],
            index=0 if config.default_provider == "groq" else 1
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=config.temperature,
            step=0.1
        )
        
        st.markdown("---")
        st.subheader("System Info")
        st.text(f"Host: {config.web_host}")
        st.text(f"Port: {config.web_port}")
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Ask a Question")
        
        # Initialize RAG system
        if 'rag_system' not in st.session_state:
            with st.spinner("Initializing RAG system..."):
                rag, error = initialize_rag_system()
                if error:
                    st.error(f"Failed to initialize: {error}")
                    st.stop()
                st.session_state.rag_system = rag
                st.success("RAG system ready!")
        
        # Query input
        query = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="Ask anything about the documents..."
        )
        
        # Process query
        if st.button("🔍 Get Answer", type="primary"):
            if query.strip():
                with st.spinner("Processing..."):
                    try:
                        rag = st.session_state.rag_system
                        response = rag.generate_answer(query, provider)
                        
                        st.subheader("📝 Answer")
                        st.write(response.get('answer', 'No answer generated'))
                        
                        if 'sources' in response and response['sources']:
                            st.subheader("📚 Sources")
                            for i, source in enumerate(response['sources'], 1):
                                with st.expander(f"Source {i}"):
                                    st.text(source.get('preview', 'No preview'))
                                    st.caption(f"Score: {source.get('score', 0):.3f}")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question.")
    
    with col2:
        st.subheader("📊 Status")
        
        if st.button("🔄 Refresh"):
            docs_path = Path("data/documents")
            if docs_path.exists():
                doc_count = len(list(docs_path.glob("*.txt")))
                st.metric("Documents", doc_count)
            else:
                st.metric("Documents", 0)
            
            st.metric("Provider", provider.upper())
        
        if st.button("🔨 Rebuild Index"):
            with st.spinner("Rebuilding..."):
                try:
                    rag, error = initialize_rag_system()
                    if error:
                        st.error(f"Failed: {error}")
                    else:
                        st.session_state.rag_system = rag
                        st.success("Index rebuilt!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
