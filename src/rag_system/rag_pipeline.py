"""
RAG Pipeline Implementation
Complete RAG system combining retrieval and generation
"""

from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Add src to path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from .document_processor import DocumentProcessor
from .llm_providers import LLMProvider
from .vector_store import DocumentChunk, VectorStore
from sglang_helpers.structured_prompts import StructuredPrompts
from sglang_helpers.parallel_processing import ParallelProcessor


class RAGSystem:
    """Complete RAG system combining retrieval and generation with SGLang structured prompts"""

    def __init__(
        self,
        docs_dir: str = "data/documents",
        vector_store_path: str = "data/vector_index/knowledge_base",
    ):
        self.docs_dir = docs_dir
        self.vector_store_path = vector_store_path
        self.vector_store = VectorStore()
        self.llm = LLMProvider()
        self.processor = DocumentProcessor()
        
        # Initialize SGLang components
        self.structured_prompts = StructuredPrompts()
        self.parallel_processor = ParallelProcessor(max_concurrent=5)

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
        try:
            # Validate input
            if not query or not query.strip():
                return {
                    "answer": "Please provide a valid question.",
                    "sources": [],
                    "query": query,
                    "error": "Empty or invalid query"
                }

            print(f"[?] Query: {query}")

            # Step 1: Retrieve relevant documents
            print("[*] Retrieving relevant documents...")
            try:
                relevant_docs = self.search(query, top_k=3)
            except Exception as e:
                print(f"[!] Error during document search: {e}")
                return {
                    "answer": "Sorry, there was an error searching the documents.",
                    "sources": [],
                    "query": query,
                    "error": f"Search error: {str(e)}"
                }

            if not relevant_docs:
                return {
                    "answer": "I don't have enough information to answer that question.",
                    "sources": [],
                    "query": query,
                }

            # Step 2: Prepare context
            context_parts = []
            sources = []

            for i, (chunk, score) in enumerate(relevant_docs, 1):
                context_parts.append(f"Source {i} ({chunk.source_file}):\n{chunk.text}")
                sources.append(
                    {
                        "file": chunk.source_file,
                        "chunk_id": chunk.id,
                        "score": score,
                        "preview": chunk.text[:100] + "..." if len(chunk.text) > 100 else chunk.text,
                    }
                )
                print(f"   [*] {chunk.source_file} (score: {score:.3f})")

            context = "\n\n".join(context_parts)

            # Step 3: Generate response using SGLang structured prompts
            print(f"[*] Generating response using {provider}...")

            try:
                # Use SGLang structured prompt for better consistency
                prompt = self.structured_prompts.structured_rag_prompt(query, context)
                answer = self.llm.generate_response(prompt, provider)
            except Exception as e:
                print(f"[!] Error generating response: {e}")
                return {
                    "answer": "Sorry, there was an error generating the response. Please try again.",
                    "sources": sources,
                    "query": query,
                    "error": f"LLM error: {str(e)}"
                }

            return {
                "answer": answer,
                "sources": sources,
                "query": query,
                "context_used": len(relevant_docs),
            }

        except Exception as e:
            print(f"[!] Unexpected error in generate_answer: {e}")
            return {
                "answer": "An unexpected error occurred. Please try again.",
                "sources": [],
                "query": query,
                "error": f"Unexpected error: {str(e)}"
            }

    def generate_multi_perspective_answer(self, query: str, provider: str = "groq") -> Dict:
        """Generate answer from multiple perspectives using SGLang structured prompts"""
        print(f"[?] Multi-perspective Query: {query}")

        # Step 1: Retrieve relevant documents
        print("[*] Retrieving relevant documents...")
        relevant_docs = self.search(query, top_k=3)

        if not relevant_docs:
            return {
                "answer": "I don't have enough information to answer that question.",
                "perspectives": {},
                "synthesis": "",
                "sources": [],
                "query": query,
            }

        # Step 2: Prepare context
        context_parts = []
        sources = []

        for i, (chunk, score) in enumerate(relevant_docs, 1):
            context_parts.append(f"Source {i} ({chunk.source_file}):\n{chunk.text}")
            sources.append(
                {
                    "file": chunk.source_file,
                    "chunk_id": chunk.id,
                    "score": score,
                    "preview": chunk.text[:100] + "..." if len(chunk.text) > 100 else chunk.text,
                }
            )

        context = "\n\n".join(context_parts)

        # Step 3: Generate perspectives using SGLang
        print("[*] Generating multi-perspective analysis...")
        perspectives = ["technical", "business", "user"]
        perspective_results = {}

        for perspective in perspectives:
            print(f"   [*] Analyzing from {perspective} perspective...")
            prompt = self.structured_prompts.multi_perspective_prompt(query, context, perspective)
            response = self.llm.generate_response(prompt, provider, max_tokens=300)
            perspective_results[perspective] = response

        # Step 4: Synthesize perspectives
        print("[*] Synthesizing perspectives...")
        synthesis_prompt = self.structured_prompts.synthesis_prompt(query, perspective_results)
        synthesis = self.llm.generate_response(synthesis_prompt, provider, max_tokens=400)

        return {
            "answer": synthesis,
            "perspectives": perspective_results,
            "synthesis": synthesis,
            "sources": sources,
            "query": query,
        }

    async def generate_answer_async(self, query: str, provider: str = "groq") -> Dict:
        """Async version using SGLang parallel processing"""
        print(f"[?] Async Query: {query}")

        # Step 1: Retrieve relevant documents
        relevant_docs = self.search(query, top_k=3)

        if not relevant_docs:
            return {
                "answer": "I don't have enough information to answer that question.",
                "sources": [],
                "query": query,
            }

        # Prepare context
        context_parts = []
        sources = []
        for i, (chunk, score) in enumerate(relevant_docs, 1):
            context_parts.append(f"Source {i} ({chunk.source_file}):\n{chunk.text}")
            sources.append(
                {
                    "file": chunk.source_file,
                    "chunk_id": chunk.id,
                    "score": score,
                    "preview": chunk.text[:100] + "..." if len(chunk.text) > 100 else chunk.text,
                }
            )

        context = "\n\n".join(context_parts)

        # Generate response asynchronously
        prompt = self.structured_prompts.structured_rag_prompt(query, context)
        
        # This would need async LLM support - for now return synchronous result
        answer = self.llm.generate_response(prompt, provider)

        return {
            "answer": answer,
            "sources": sources,
            "query": query,
            "processing": "async"
        }

    def interactive_demo(self):
        """Run interactive demo with SGLang features"""
        print("\n" + "=" * 60)
        print("[*] SGLang RAG System Interactive Demo")
        print("=" * 60)
        print("Ask questions about:")
        print("• AI/ML concepts (RAG, LLMs, vector databases)")
        print("• Company policies (vacation, benefits, security)")
        print("• API documentation (authentication, endpoints)")
        print("• Research papers (GPT-4, BERT, Transformers)")
        print("• Troubleshooting (performance, databases, monitoring)")
        print("\nSpecial commands:")
        print("• 'quit' - Exit the demo")
        print("• 'stats' - Show system info")
        print("• 'multi: <question>' - Multi-perspective analysis using SGLang")
        print("-" * 60)

        while True:
            try:
                query = input("\n[?] Your question: ").strip()

                if query.lower() == "quit":
                    print("[*] Goodbye!")
                    break

                if query.lower() == "stats":
                    self._show_stats()
                    continue

                if not query:
                    continue

                # Check for multi-perspective command
                if query.lower().startswith("multi:"):
                    actual_query = query[6:].strip()
                    if actual_query:
                        print("[*] Using SGLang multi-perspective analysis...")
                        result = self.generate_multi_perspective_answer(actual_query)
                        
                        print("\n[+] Synthesized Answer:")
                        print(f"{result['answer']}")
                        
                        print("\n[+] Individual Perspectives:")
                        for perspective, analysis in result["perspectives"].items():
                            print(f"\n--- {perspective.upper()} PERSPECTIVE ---")
                            print(analysis[:200] + "..." if len(analysis) > 200 else analysis)
                        
                        print(f"\n[i] Sources used ({len(result['sources'])} documents):")
                        for i, source in enumerate(result["sources"], 1):
                            print(f"   {i}. {source['file']} (relevance: {source['score']:.3f})")
                            print(f"      Preview: {source['preview']}")
                    else:
                        print("Please provide a question after 'multi:'")
                    continue

                # Generate regular answer using SGLang structured prompts
                result = self.generate_answer(query)

                # Display results
                print("\n[+] Answer:")
                print(f"{result['answer']}")

                print(f"\n[i] Sources used ({len(result['sources'])} documents):")
                for i, source in enumerate(result["sources"], 1):
                    print(f"   {i}. {source['file']} (relevance: {source['score']:.3f}")
                    print(f"      Preview: {source['preview']}")
            except Exception as e:
                print(f"[!] Error: {e}")

    # --------- Test-facing helpers for CI and notebooks ---------
    def load_documents(self, path: str | Path | None = None, *, force: bool = False):
        """
        Thin wrapper so tests can call `rag.load_documents()`.
        """
        if force or not getattr(self, "_docs_loaded", False):
            docs_path = Path(path or self.docs_dir)
            self._raw_documents = list(docs_path.glob("*.txt"))
            # Actually load and chunk docs using the real loader
            self.chunks = self.processor.load_documents(str(docs_path))
            self._docs_loaded = True
        return self._raw_documents

    @property
    def raw_documents(self):
        if not getattr(self, "_docs_loaded", False):
            raise RuntimeError("Call load_documents() first.")
        return self._raw_documents

    @property
    def chunks(self):
        if not hasattr(self, "_chunks"):
            raise RuntimeError("Run build_index() first.")
        return self._chunks

    @chunks.setter
    def chunks(self, value):
        self._chunks = value

    def query(self, prompt: str, **kwargs):
        # For test compatibility: returns just the answer string
        result = self.generate_answer(prompt, **kwargs)
        return result["answer"] if isinstance(result, dict) and "answer" in result else result
