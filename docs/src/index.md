# SGLang RAG Demo

A document retrieval and question answering system built with SGLang structured prompts.

## Overview

This system uses semantic search with language models to answer questions based on your documents.

## Key Features

- Vector search using FAISS for document similarity
- SGLang structured prompt templates
- Web interface for document querying
- Multi-perspective analysis capabilities
- Command-line interface
- Performance benchmarking tools

## Quick Start

### Installation

```bash
pip install -e .
```

### Usage

```bash
# CLI
sglang-rag --query "What is the vacation policy?"

# Web interface  
sglang-web
```

### Web Interface

```bash
python web.py
```

Navigate to http://localhost:8080 to access the interactive dashboard.

## Architecture

The system consists of several key components:

- **Document Processor**: Handles text chunking and preprocessing
- **Vector Store**: FAISS-based similarity search with embeddings
- **LLM Providers**: Integration with multiple language model APIs
- **RAG Pipeline**: Orchestrates retrieval and generation

See the [Architecture Overview](architecture/overview.md) for detailed information.

## Performance

Recent benchmarks show:

- **1K documents**: ~45ms average query latency
- **10K documents**: ~120ms average query latency  
- **Throughput**: 15-25 queries per second

See [Performance Guide](guides/performance.md) for optimization tips.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.
