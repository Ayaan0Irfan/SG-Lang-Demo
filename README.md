# SGLang RAG Demo

A document retrieval and question answering system built with SGLang structured prompts.

## Features

- Document processing and vector search using FAISS
- Multi-perspective query analysis (technical, business, user viewpoints)
- Structured prompt templates for consistent responses
- Web interface and command-line interface
- Support for multiple LLM providers (Groq, Together AI)
- Parallel processing for faster responses

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sglang-rag-demo.git
   cd sglang-rag-demo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Build the document index:
   ```bash
   python scripts/build_index.py
   ```

## Usage

### Command Line Interface

```bash
# Basic query
sglang-rag --query "What is API authentication?"

# Multi-perspective analysis
sglang-rag --query "What is machine learning?" --multi-perspective

# Interactive mode
sglang-rag
```

### Web Interface

```bash
sglang-web
# Opens at http://localhost:8501
```

### Quick Demo

```bash
python scripts/quick_demo.py
```

## Project Structure

```
├── src/
│   ├── sglang_helpers/           # SGLang utilities
│   │   ├── structured_prompts.py # Prompt templates
│   │   └── parallel_processing.py # Async operations
│   ├── rag_system/              # Core RAG components
│   │   ├── rag_pipeline.py      # Main pipeline
│   │   ├── document_processor.py # Document processing
│   │   ├── vector_store.py      # Vector storage
│   │   └── llm_providers.py     # LLM client
│   ├── web/                     # Web interface
│   └── sglang_demo/             # CLI interface
├── scripts/                     # Utility scripts
├── data/                        # Documents and vector index
├── tests/                       # Tests
└── docs/                        # Documentation
```

## How it Works

### Structured Prompts

The system uses SGLang templates for consistent output formatting:

```python
# Output format:
"""
1. DIRECT ANSWER: [Clear response]
2. SUPPORTING EVIDENCE: [Relevant quotes]
3. CONFIDENCE LEVEL: [High/Medium/Low]
"""
```

### Multi-Perspective Analysis

Analyzes queries from three viewpoints:
- **Technical**: Implementation details and architecture
- **Business**: Costs, benefits, and strategy
- **User**: Practical applications and experience

### Parallel Processing

Processes multiple LLM calls concurrently for faster responses.

## Configuration

Set up these environment variables in your `.env` file:

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Settings
DEFAULT_PROVIDER=groq
MAX_TOKENS=500
TEMPERATURE=0.3
TOP_K_RESULTS=3
```

## Development

### Running Tests

```bash
pytest tests/
```

### Building Vector Index

```bash
python scripts/build_index.py
```

### Performance Benchmarking

```bash
python scripts/benchmark_retrieval.py
```

## License

Apache 2.0 License

## Dependencies

- FAISS for vector similarity search
- Groq and OpenAI for language models
- Streamlit for web interface
- SGLang for structured prompting
