# Scripts

This directory contains utility scripts for the SGLang RAG Demo project.

## Available Scripts

### `build_index.py`
Processes documents in `data/documents/` and creates a FAISS vector index for search.

**Usage:**
```bash
python scripts/build_index.py
```

### `quick_demo.py`
Runs predefined queries against the RAG system to demonstrate basic functionality.

**Usage:**
```bash
python scripts/quick_demo.py
```

### `benchmark_retrieval.py`
Performance benchmarking script that measures retrieval speed and accuracy.

**Usage:**
```bash
python scripts/benchmark_retrieval.py
```

### `build_docs.py`
Builds project documentation using the configured documentation generator.

**Usage:**
```bash
python scripts/build_docs.py
```

## Alternative Usage

Instead of running scripts directly, you can use the console commands after installing the package:

```bash
# Install the package
pip install -e .

# Use console commands
sglang-rag --help           # CLI interface
sglang-web                  # Web interface
```
