"""
RAG Pipeline Implementation
Complete RAG system combining retrieval and generation
"""

from pathlib import Path
from typing import List, Dict, Tuple
from .vector_store import VectorStore, DocumentChunk
from .llm_providers import LLMProvider
from .document_processor import DocumentProcessor


class RAGSystem:
    """Complete RAG system combining retrieval and generation"""
    
    def __init__(self, docs_dir: str = "data/documents", vector_store_path: str = "data/vector_index/knowledge_base"):
        self.docs_dir = docs_dir
        self.vector_store_path = vector_store_path
        self.vector_store = VectorStore()
        self.llm = LLMProvider()
        self.processor = DocumentProcessor()
        
    def build_index(self, force_rebuild: bool = False):
        """Build or load the vector index"""
        vector_file_path = Path(f"{self.vector_store_path}.faiss")
        
        if vector_file_path.exists() and not force_rebuild:
            print("[*] Loading existing vector index...")
            self.vector_store.load(self.vector_store_path)
        else:
            print("[*] Building new vector index...")
            
            # Load and process documents
            chunks = self.processor.load_documents(self.docs_dir)
            
            # Build vector store
            self.vector_store.add_documents(chunks)
            
            # Save for future use
            self.vector_store.save(self.vector_store_path)
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[DocumentChunk, float]]:
        """Search for relevant documents"""
        return self.vector_store.search(query, top_k)
    
    def generate_answer(self, query: str, provider: str = "groq") -> Dict:
        """Generate answer using RAG pipeline"""
        print(f"[?] Query: {query}")
        
        # Step 1: Retrieve relevant documents
        print("[*] Retrieving relevant documents...")
        relevant_docs = self.search(query, top_k=3)
        
        if not relevant_docs:
            return {
                "answer": "I don't have enough information to answer that question.",
                "sources": [],
                "query": query
            }
        
        # Step 2: Prepare context
        context_parts = []
        sources = []
        
        for i, (chunk, score) in enumerate(relevant_docs, 1):
            context_parts.append(f"Source {i} ({chunk.source_file}):\n{chunk.text}")
            sources.append({
                "file": chunk.source_file,
                "chunk_id": chunk.id,
                "score": score,
                "preview": chunk.text[:100] + "..." if len(chunk.text) > 100 else chunk.text
            })
            print(f"   [*] {chunk.source_file} (score: {score:.3f})")
        
        context = "\n\n".join(context_parts)
        
        # Step 3: Generate response
        print(f"[*] Generating response using {provider}...")
        
        prompt = f"""Based on the following context, please answer the user's question. Be accurate and cite specific information from the context when possible.

Context:
{context}

Question: {query}

Please provide a comprehensive answer based on the context above. If the context doesn't contain enough information to fully answer the question, please say so."""

        answer = self.llm.generate_response(prompt, provider)
        
        return {
            "answer": answer,
            "sources": sources,
            "query": query,
            "context_used": len(relevant_docs)
        }
    
    def interactive_demo(self):
        """Run interactive demo"""
        print("\n" + "="*60)
        print("[*] RAG System Interactive Demo")
        print("="*60)
        print("Ask questions about:")
        print("• AI/ML concepts (RAG, LLMs, vector databases)")
        print("• Company policies (vacation, benefits, security)")
        print("• API documentation (authentication, endpoints)")
        print("• Research papers (GPT-4, BERT, Transformers)")
        print("• Troubleshooting (performance, databases, monitoring)")
        print("\nType 'quit' to exit, 'stats' for system info")
        print("-" * 60)
        
        while True:
            try:
                query = input("\n[?] Your question: ").strip()
                
                if query.lower() == 'quit':
                    print("[*] Goodbye!")
                    break
                    
                if query.lower() == 'stats':
                    self._show_stats()
                    continue
                
                if not query:
                    continue
                
                # Generate answer
                result = self.generate_answer(query)
                
                # Display results
                print(f"\n[+] Answer:")
                print(f"{result['answer']}")
                
                print(f"\n[i] Sources used ({result['context_used']} documents):")
                for i, source in enumerate(result['sources'], 1):
                    print(f"   {i}. {source['file']} (relevance: {source['score']:.3f})")
                    print(f"      Preview: {source['preview']}")
                
            except KeyboardInterrupt:
                print("\n[*] Goodbye!")
                break
            except Exception as e:
                print(f"[!] Error: {e}")
    
    def _show_stats(self):
        """Show system statistics"""
        print(f"\n[i] RAG System Statistics:")
        print(f"   Documents in index: {len(set(chunk.source_file for chunk in self.vector_store.chunks))}")
        print(f"   Total chunks: {len(self.vector_store.chunks)}")
        print(f"   Vector dimensions: {self.vector_store.dimension}")
        print(f"   LLM providers: {', '.join(self.llm.list_available_providers())}")
        
        # Document stats
        if self.vector_store.chunks:
            stats = self.processor.get_document_stats(self.vector_store.chunks)
            print(f"   Total words: {stats['total_words']:,}")
            print(f"   Average chunk size: {stats['avg_chunk_size']:.1f} words")
