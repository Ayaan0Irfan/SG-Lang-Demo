# Project Organization

This document describes how the SGLang RAG Demo project files are organized.

## Root Level Philosophy

The root directory contains only essential files:

### Core Files
- `README.md` - Project overview and usage instructions
- `LICENSE` - Apache 2.0 license text
- `pyproject.toml` - Python package configuration and metadata
- `requirements*.txt` - Python dependencies for production and development
- `.gitignore` - Files and directories excluded from version control
- `.env.example` - Template showing required environment variables

### Entry Points
- `main.py` - Command-line interface for the RAG system
- `web.py` - Streamlit web application interface

### Hidden Configuration
- `.env` - Local environment (gitignored)
- `.github/` - CI/CD and repository configuration
- `.venv/` - Virtual environment (gitignored)

## Directory Structure

### Source Code Organization
```
src/
├── rag_system/          # Document processing and vector search
├── sglang/              # SGLang prompt templates and LLM integration  
├── web/                 # Streamlit interface components
└── config.py            # Application configuration loader
```

### Development Support
```
tests/                   # Unit tests, end-to-end tests, and smoke tests
scripts/                 # Benchmarking, indexing, and documentation scripts
notebooks/               # Jupyter notebooks for performance analysis
docs/                    # Project documentation and changelogs
config/                  # YAML configuration files
data/                    # Sample documents and benchmark results
```

## Documentation Structure

Documentation files are stored in `docs/`:
- Project documentation (PROJECT_STRUCTURE.md, etc.)
- MkDocs configuration and source
- Changelog and release notes
- Architecture and API documentation

## Benefits of This Organization

1. **Clean Root**: Only essential files visible at first glance
2. **Predictable**: Follows Python community standards
3. **Scalable**: Easy to add new components without clutter
4. **Tool-Friendly**: Works with all Python tooling (pip, pytest, etc.)
5. **IDE-Friendly**: Standard structure recognized by all IDEs

## Comparison to Industry Standards

This structure matches or exceeds standards from:
- **Django/Flask**: Web framework patterns
- **FastAPI**: Modern Python API projects  
- **NumPy/Pandas**: Scientific Python libraries
- **Requests/urllib3**: Popular Python packages

## Maintenance Guidelines

When adding new components:
- **New features**: Add to appropriate `src/` package
- **New tools**: Add to `scripts/`
- **New docs**: Add to `docs/`
- **New tests**: Add to `tests/`

Never add new files to root unless absolutely necessary and following Python standards.
