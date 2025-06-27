#!/usr/bin/env python3
"""
Command-line interface for the SGLang RAG system with options for interactive queries and batch processing
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from config import config
from rag_system import RAGSystem


def main():
    """Parses command line arguments and runs interactive or batch query mode"""
    parser = argparse.ArgumentParser(
        description="SGLang RAG Demo - Professional RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sglang-rag                        # Interactive demo
  sglang-rag --query "What is RAG?" # Single query
  sglang-rag --build-index          # Rebuild vector index
  sglang-rag --stats                # Show system statistics
        """,
    )

    parser.add_argument("--query", "-q", type=str, help="Ask a single question")

    parser.add_argument(
        "--provider",
        "-p",
        type=str,
        choices=["groq", "together"],
        default=config.default_provider,
        help="LLM provider to use",
    )

    parser.add_argument(
        "--build-index", "-b", action="store_true", help="Force rebuild of vector index"
    )

    parser.add_argument("--stats", "-s", action="store_true", help="Show system statistics")

    parser.add_argument(
        "--docs-dir", "-d", type=str, default=config.documents_dir, help="Documents directory path"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    parser.add_argument(
        "--multi-perspective", "-m", action="store_true", 
        help="Use SGLang multi-perspective analysis"
    )

    args = parser.parse_args()

    # Initialize RAG system
    print(f"[*] Initializing {config.app_name} v{config.app_version}")

    rag = RAGSystem(
        docs_dir=args.docs_dir, vector_store_path=f"{config.vector_index_dir}/knowledge_base"
    )

    # Build index
    rag.build_index(force_rebuild=args.build_index)

    if args.stats:
        print("\n[i] System Statistics:")
        rag._show_stats()
        return

    if args.query:
        print(f"\n[?] Processing query: {args.query}")
        
        if args.multi_perspective:
            print("[*] Using SGLang multi-perspective analysis...")
            result = rag.generate_multi_perspective_answer(args.query, provider=args.provider)
            
            print("\n[+] Synthesized Answer:")
            print(result["answer"])
            
            if args.verbose:
                print("\n[+] Individual Perspectives:")
                for perspective, analysis in result["perspectives"].items():
                    print(f"\n--- {perspective.upper()} PERSPECTIVE ---")
                    print(analysis)
                    
                print(f"\n[i] Sources ({len(result['sources'])}):")
                for i, source in enumerate(result["sources"], 1):
                    print(f"   {i}. {source['file']} (score: {source['score']:.3f})")
        else:
            result = rag.generate_answer(args.query, provider=args.provider)

            print("\n[+] Answer:")
            print(result["answer"])

            if args.verbose:
                print(f"\n[i] Sources ({len(result['sources'])}):")
                for i, source in enumerate(result["sources"], 1):
                    print(f"   {i}. {source['file']} (score: {source['score']:.3f})")
    else:
        # Interactive mode
        rag.interactive_demo()


def web_main():
    """Launches Streamlit application with the web interface components"""
    import subprocess

    print(f"[*] Starting {config.app_name} Web Interface")
    print(f"[*] Version: {config.app_version}")
    print(f"[*] Host: {config.web_host}")
    print(f"[*] Port: {config.web_port}")
    print()

    # Use the web app
    web_app_path = Path(__file__).parent.parent / "web" / "app.py"
    if not web_app_path.exists():
        print("[!] Web app not found. Please ensure src/web/app.py exists.")
        return

    try:
        subprocess.run(
            [
                "streamlit",
                "run",
                str(web_app_path),
                "--server.headless",
                "true",
                "--server.address",
                config.web_host,
                "--server.port",
                str(config.web_port),
            ]
        )
    except KeyboardInterrupt:
        print("\n[*] Web interface stopped by user")
    except FileNotFoundError:
        print("[!] Streamlit not found. Please install with: pip install streamlit")
        return


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
