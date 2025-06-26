# SGLang RAG System

A professional-grade Retrieval-Augmented Generation (RAG) system with SGLang integration.

## Overview

This system combines semantic search capabilities with large language models to provide accurate, context-aware responses based on your document corpus.

## Key Features

- **Vector Search**: FAISS-based semantic similarity search with cosine distance
- **SGLang Integration**: Structured prompt templates for consistent responses  
- **Streamlit Dashboard**: Interactive web interface for document querying
- **Async Processing**: Concurrent document processing and query handling
- **Unit Tests**: Test coverage for vector store and LLM providers
- **Performance Benchmarks**: Response time metrics and throughput analysis

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### CLI Usage

```bash
python main.py "What is the vacation policy?"
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
