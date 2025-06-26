# SGLang RAG System
A retrieval-augmented generation system that combines vector search with language model generation using SGLang structured prompts.



## Quick Start



### CLI Usage
```bash
python main.py
```


### Web Interface
```bash
python web.py
```



## Installation

```bash
pip install -r requirements.txt
```



For development:
```bash
pip install -r requirements-dev.txt
```



## Project Structure
See `docs/PROJECT_STRUCTURE.md` for detailed project organization.



## Features
- Vector-based document search using FAISS with cosine similarity
- SGLang structured prompts for consistent response generation
- Streamlit web interface for document queries
- Asynchronous document processing
- Unit tests for core components
- Performance benchmarking for response times



## Documentation
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Project Summary](docs/PROJECT_SUMMARY.md)
- [Structure Comparison](docs/STRUCTURE_COMPARISON.md)
- [Final Status](docs/FINAL_STATUS.md)
- [Changelog](docs/CHANGELOG.md)

### Full Documentation Site

Build and serve the complete documentation:

```bash
python scripts/build_docs.py --serve
```

Or build static docs:

```bash
python scripts/build_docs.py
```



## License

Apache License 2.0

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.