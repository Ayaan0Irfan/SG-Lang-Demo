"""
Document Processing Module
Text processing, chunking, and document management utilities
"""

import hashlib
from pathlib import Path
from typing import Dict, List

from .vector_store import DocumentChunk


class DocumentProcessor:
    """Process documents into chunks for vector storage"""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_documents(self, docs_dir: str) -> List[DocumentChunk]:
        """Load and chunk all documents from directory"""
        try:
            docs_path = Path(docs_dir)
            all_chunks = []

            print(f"[*] Loading documents from {docs_dir}")

            if not docs_path.exists():
                print(f"[!] Documents directory {docs_dir} does not exist.")
                return []

            txt_files = list(docs_path.glob("*.txt"))
            if not txt_files:
                print(f"[!] No .txt documents found in {docs_dir}. Please add documents and try again.")
                return []

            for file_path in txt_files:
                try:
                    print(f"[*] Processing {file_path.name}...")

                    with open(file_path, encoding="utf-8") as f:
                        content = f.read()

                    if not content.strip():
                        print(f"   [!] Warning: {file_path.name} is empty, skipping...")
                        continue

                    # Split into chunks
                    chunks = self._chunk_text(content, file_path.name)
                    all_chunks.extend(chunks)

                    print(f"   [+] Created {len(chunks)} chunks from {file_path.name}")

                except Exception as e:
                    print(f"   [!] Error processing {file_path.name}: {e}")
                    continue

            print(f"[i] Total chunks created: {len(all_chunks)})")
            return all_chunks

        except Exception as e:
            print(f"[!] Error loading documents: {e}")
            return []

    def _chunk_text(self, text: str, source_file: str) -> List[DocumentChunk]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            # Create unique ID for chunk
            chunk_id = hashlib.md5(f"{source_file}_{i}_{chunk_text[:50]}".encode()).hexdigest()[:12]

            chunk = DocumentChunk(
                id=chunk_id,
                text=chunk_text,
                source_file=source_file,
                chunk_index=len(chunks),
                metadata={
                    "word_count": len(chunk_words),
                    "char_count": len(chunk_text),
                    "start_word": i,
                    "end_word": i + len(chunk_words),
                },
            )
            chunks.append(chunk)

            # Stop if we've covered all words
            if i + self.chunk_size >= len(words):
                break

        return chunks

    def preprocess_text(self, text: str) -> str:
        """Basic text preprocessing"""
        # Remove extra whitespace
        text = " ".join(text.split())

        # Basic cleanup (can be extended)
        text = text.replace("\n", " ").replace("\r", " ")

        return text

    def get_document_stats(self, chunks: List[DocumentChunk]) -> Dict:
        """Get statistics about processed documents"""
        if not chunks:
            return {}

        total_chars = sum(chunk.metadata["char_count"] for chunk in chunks)
        total_words = sum(chunk.metadata["word_count"] for chunk in chunks)

        files = list(set(chunk.source_file for chunk in chunks))

        return {
            "total_chunks": len(chunks),
            "total_characters": total_chars,
            "total_words": total_words,
            "unique_files": len(files),
            "files": files,
            "avg_chunk_size": total_words / len(chunks) if chunks else 0,
        }
