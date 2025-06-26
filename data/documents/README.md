# Company Knowledge Base - Sample Documents

This directory contains sample documents for demonstrating the RAG system capabilities.

## Document Categories

### 📋 Policy Documents
- `company_handbook.txt` - HR policies and procedures
- `api_documentation.txt` - Technical API reference

### 🔧 Technical Guides  
- `troubleshooting_guide.txt` - Common issues and solutions
- `ai_ml_guide.txt` - AI/ML best practices

### 📚 Research Materials
- `research_papers.txt` - Academic paper summaries

## Usage

These documents are automatically indexed by the RAG system on startup. You can:

1. **Query via CLI**: `python main.py "What is the vacation policy?"`
2. **Query via Web**: `python web.py` then browse to http://localhost:8080
3. **Add new documents**: Place `.txt` files in this directory and restart

## Document Format

Documents should be plain text (.txt) files with clear section headers for optimal chunking and retrieval.
