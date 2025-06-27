"""
SGLang RAG Demo Package

A hands-on demo of a Retrieval-Augmented Generation (RAG) stack that pairs
a local FAISS vector index with calls to external LLMs (Groq or Together AI).
"""

__version__ = "0.1.0"
__author__ = "SGLang RAG Team"
__email__ = "team@sglang-rag.com"

from .cli import main, web_main

__all__ = ["main", "web_main"]
