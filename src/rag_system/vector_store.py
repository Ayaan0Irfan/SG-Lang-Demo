"""
Vector Store Implementation
FAISS-based vector storage with semantic search capabilities
"""

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
from sentence_transformers import SentenceTransformer


@dataclass
class DocumentChunk:
    """Represents a chunk of text from a document"""

    id: str
    text: str
    source_file: str
    chunk_index: int
    metadata: Dict


class VectorStore:
    """FAISS-based vector store for semantic search"""

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        self.chunks: List[DocumentChunk] = []
        self.is_built = False

    def add_documents(self, documents: List[DocumentChunk]):
        """Add documents to the vector store"""
        print(f"[*] Generating embeddings for {len(documents)} document chunks...")

        # Extract text for embedding
        texts = [doc.text for doc in documents]

        # Generate embeddings in batches for efficiency
        embeddings = self.embedding_model.encode(
            texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True
        )

        # Add to FAISS index
        self.index.add(embeddings.astype("float32"))
        self.chunks.extend(documents)
        self.is_built = True

        print(f"[+] Added {len(documents)} chunks to vector store")
        print(f"[i] Total vectors in index: {self.index.ntotal}")

    def search(self, query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """Search for relevant documents"""
        if not self.is_built:
            raise ValueError("Vector store not built. Add documents first.")

        # Generate query embedding
        query_embedding = self.embedding_model.encode([query], normalize_embeddings=True)

        # Search in FAISS index
        scores, indices = self.index.search(query_embedding.astype("float32"), top_k)

        # Return chunks with scores
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # Valid result
                results.append((self.chunks[idx], float(score)))

        return results

    def save(self, filepath: str):
        """Save vector store to disk"""
        save_dir = Path(filepath).parent
        save_dir.mkdir(exist_ok=True, parents=True)

        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.faiss")

        # Save chunks and metadata
        with open(f"{filepath}.pkl", "wb") as f:
            pickle.dump(
                {
                    "chunks": self.chunks,
                    "dimension": self.dimension,
                    "model_name": "all-MiniLM-L6-v2",
                },
                f,
            )
        print(f"[+] Vector store saved to {filepath}")

    def load(self, filepath: str):
        """Load vector store from disk"""
        # Load FAISS index
        self.index = faiss.read_index(f"{filepath}.faiss")

        # Load chunks and metadata
        with open(f"{filepath}.pkl", "rb") as f:
            data = pickle.load(f)
            self.chunks = data["chunks"]
            self.dimension = data["dimension"]

        self.is_built = True
        print(f"[+] Vector store loaded from {filepath}")
