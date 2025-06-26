# Project Organization

This document describes the organizational principles behind the SGLang RAG Demo project structure.

## Root Level Philosophy

The root directory follows the "essential files only" principle:

### Core Files (Must Stay at Root)
- `README.md` - First thing users see, project overview
- `LICENSE` - Legal requirement for open source
- `pyproject.toml` - Modern Python packaging standard
- `requirements*.txt` - Dependency management (pip standard)
- `.gitignore` - Version control configuration
- `.env.example` - Environment template for users

### Entry Points (Must Stay at Root)
- `main.py` - CLI interface entry point
- `web.py` - Web interface entry point

### Hidden Configuration
- `.env` - Local environment (gitignored)
- `.github/` - CI/CD and repository configuration
- `.venv/` - Virtual environment (gitignored)

## Directory Structure

### Source Code Organization
```
src/
├── rag_system/          # Core RAG functionality
├── sglang/              # SGLang integration  
├── web/                 # Web interface components
└── config.py            # Configuration management
```

### Development Support
```
tests/                   # All testing code
scripts/                 # Utility and build scripts
notebooks/               # Analysis and demos
docs/                    # All documentation
config/                  # Configuration files
data/                    # Data and results
```

## Documentation Consolidation

All documentation is now centralized in `docs/`:
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
