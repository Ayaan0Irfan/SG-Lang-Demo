# SGLang RAG Demo

A comprehensive Retrieval-Augmented Generation (RAG) system showcasing **SGLang** structured prompts and parallel processing capabilities.

## 🌟 Features

### SGLang Integration
- **Structured Prompts**: Template-based prompt engineering for consistent, organized outputs
- **Multi-Perspective Analysis**: Analyze queries from technical, business, and user perspectives
- **Parallel Processing**: Async and concurrent execution for LLM operations
- **Synthesis**: Combine multiple perspectives into comprehensive answers

### RAG Capabilities
- **Document Processing**: Automatic chunking and embedding of text documents
- **Vector Search**: FAISS-based similarity search for relevant document retrieval
- **Multi-Provider LLM**: Support for Groq and Together AI with automatic fallback
- **Web Interface**: Professional Streamlit-based web UI
- **CLI Interface**: Interactive command-line interface with SGLang features

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "SG Lang Demo"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

4. **Set up API keys**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Usage

#### 🔥 SGLang Multi-Perspective Analysis

```bash
# Multi-perspective analysis via CLI
sglang-rag --query "What is API authentication?" --multi-perspective --verbose

# Interactive mode with SGLang commands
sglang-rag
# Then use: multi: What is machine learning?
```

#### 💻 Web Interface

```bash
sglang-web
# Opens at http://localhost:8501
```

#### 🧪 Quick Demo

```bash
python scripts/quick_demo.py
```

## 📁 Project Structure

```
├── src/
│   ├── sglang/                    # SGLang implementation
│   │   ├── structured_prompts.py  # Template-based prompts
│   │   └── parallel_processing.py # Async operations
│   ├── rag_system/               # Core RAG pipeline
│   │   ├── rag_pipeline.py       # Main pipeline with SGLang
│   │   ├── document_processor.py # Document chunking
│   │   ├── vector_store.py       # FAISS vector operations
│   │   └── llm_providers.py      # Multi-provider LLM client
│   ├── web/                      # Streamlit web interface
│   └── sglang_demo/              # CLI interface
├── scripts/                      # Utility scripts
├── data/                         # Documents and vector index
├── tests/                        # Test suite
└── docs/                         # Documentation
```

## 🎯 SGLang Examples

### Structured Prompts

The system uses SGLang's structured prompt templates for consistent outputs:

```python
# Example output format:
"""
1. DIRECT ANSWER: [Clear, direct response]
2. SUPPORTING EVIDENCE: [Quotes from context]
3. CONFIDENCE LEVEL: [High/Medium/Low]
"""
```

### Multi-Perspective Analysis

Query the same question from different viewpoints:

- **Technical**: Implementation details, architecture, specifications
- **Business**: Costs, benefits, strategic considerations
- **User**: Usability, practical applications, experience

### Parallel Processing

```python
# SGLang parallel processing for multiple LLM calls
processor = ParallelProcessor(max_concurrent=5)
results = await processor.execute_parallel(tasks)
```

## 🛠️ Configuration

### Environment Variables

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key_here
TOGETHER_API_KEY=your_together_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional

# System Settings
DEFAULT_PROVIDER=groq
MAX_TOKENS=500
TEMPERATURE=0.3
TOP_K_RESULTS=3
```

### LLM Providers

- **Groq**: Primary provider (fast inference)
- **Together AI**: Fallback provider
- **OpenAI**: Optional for embeddings

## 📊 Performance Features

- **Caching**: Embedding and response caching
- **Async Processing**: Non-blocking operations
- **Batching**: Efficient bulk operations
- **Rate Limiting**: Respectful API usage

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Building Documentation

```bash
python scripts/build_docs.py
```

### Performance Benchmarking

```bash
python scripts/benchmark_retrieval.py
```

## 📈 Example Outputs

### Standard Query
```
[?] Query: What is the vacation policy?
[+] Answer: According to company policy, employees have unlimited PTO with minimum 3 weeks recommended per year...
```

### SGLang Multi-Perspective
```
[?] Multi-perspective Query: What is API authentication?

--- TECHNICAL PERSPECTIVE ---
API authentication uses Bearer tokens in Authorization headers...

--- BUSINESS PERSPECTIVE ---
Authentication provides security and access control, reducing liability...

--- USER PERSPECTIVE ---
Users need clear documentation and simple integration steps...

[+] Synthesized Answer:
API authentication combines technical security measures with business value...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- **SGLang**: For structured prompting capabilities
- **FAISS**: For efficient vector similarity search
- **Streamlit**: For the web interface
- **Groq & Together AI**: For LLM inference
