#!/usr/bin/env python3
"""
Command-line interface for the SGLang RAG system with options for interactive queries and batch processing
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_system import RAGSystem
from config import config


def main():
    """Parses command line arguments and runs interactive or batch query mode"""
    parser = argparse.ArgumentParser(
        description="SGLang RAG Demo - Professional RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive demo
  python main.py --query "What is RAG?"  # Single query
  python main.py --build-index     # Rebuild vector index
  python main.py --stats           # Show system statistics
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Ask a single question"
    )
    
    parser.add_argument(
        "--provider", "-p",
        type=str,
        choices=["groq", "together"],
        default=config.default_provider,
        help="LLM provider to use"
    )
    
    parser.add_argument(
        "--build-index", "-b",
        action="store_true",
        help="Force rebuild of vector index"
    )
    
    parser.add_argument(
        "--stats", "-s",
        action="store_true",
        help="Show system statistics"
    )
    
    parser.add_argument(
        "--docs-dir", "-d",
        type=str,
        default=config.documents_dir,
        help="Documents directory path"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize RAG system
    print(f"[*] Initializing {config.app_name} v{config.app_version}")
    
    rag = RAGSystem(
        docs_dir=args.docs_dir,
        vector_store_path=f"{config.vector_index_dir}/knowledge_base"
    )
    
    # Build index
    rag.build_index(force_rebuild=args.build_index)
    
    if args.stats:
        print("\n[i] System Statistics:")
        rag._show_stats()
        return
    
    if args.query:
        print(f"\n[?] Processing query: {args.query}")
        result = rag.generate_answer(args.query, provider=args.provider)
        
        print(f"\n[+] Answer:")
        print(result['answer'])
        
        if args.verbose:
            print(f"\n[i] Sources ({len(result['sources'])}):")
            for i, source in enumerate(result['sources'], 1):
                print(f"   {i}. {source['file']} (score: {source['score']:.3f})")
    else:
        # Interactive mode
        rag.interactive_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
