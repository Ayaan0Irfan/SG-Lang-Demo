"""
SGLang Implementation Package
Structured prompts, parallel processing, and advanced RAG patterns
"""

__version__ = "1.0.0"

from .parallel_processing import ParallelProcessor
from .structured_prompts import StructuredPrompts

__all__ = ["StructuredPrompts", "ParallelProcessor"]
