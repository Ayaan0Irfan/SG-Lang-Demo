"""
Configuration Management
Load and manage application settings
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """Application configuration manager"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._load_environment()
        
    def _load_environment(self):
        """Load environment variables from .env files"""
        # Load main .env file
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
        
        # Load settings.env
        settings_file = self.config_dir / "settings.env"
        if settings_file.exists():
            load_dotenv(settings_file)
    
    @property
    def app_name(self) -> str:
        return os.getenv("APP_NAME", "SGLang RAG Demo")
    
    @property
    def app_version(self) -> str:
        return os.getenv("APP_VERSION", "1.0.0")
    
    @property
    def data_dir(self) -> str:
        return os.getenv("DATA_DIR", "data")
    
    @property
    def documents_dir(self) -> str:
        return os.getenv("DOCUMENTS_DIR", "data/documents")
    
    @property
    def vector_index_dir(self) -> str:
        return os.getenv("VECTOR_INDEX_DIR", "data/vector_index")
    
    @property
    def embedding_model(self) -> str:
        return os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    @property
    def chunk_size(self) -> int:
        return int(os.getenv("CHUNK_SIZE", "500"))
    
    @property
    def chunk_overlap(self) -> int:
        return int(os.getenv("CHUNK_OVERLAP", "50"))
    
    @property
    def top_k_results(self) -> int:
        return int(os.getenv("TOP_K_RESULTS", "3"))
    
    @property
    def default_provider(self) -> str:
        return os.getenv("DEFAULT_PROVIDER", "groq")
    
    @property
    def max_tokens(self) -> int:
        return int(os.getenv("MAX_TOKENS", "500"))
    
    @property
    def temperature(self) -> float:
        return float(os.getenv("TEMPERATURE", "0.3"))
    
    @property
    def max_concurrent_calls(self) -> int:
        return int(os.getenv("MAX_CONCURRENT_CALLS", "5"))
    
    @property
    def web_host(self) -> str:
        return os.getenv("WEB_HOST", "localhost")
    
    @property
    def web_port(self) -> int:
        return int(os.getenv("WEB_PORT", "8080"))
    
    @property
    def debug_mode(self) -> bool:
        return os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all configuration settings"""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "data_dir": self.data_dir,
            "documents_dir": self.documents_dir,
            "vector_index_dir": self.vector_index_dir,
            "embedding_model": self.embedding_model,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "top_k_results": self.top_k_results,
            "default_provider": self.default_provider,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "max_concurrent_calls": self.max_concurrent_calls,
            "web_host": self.web_host,
            "web_port": self.web_port,
            "debug_mode": self.debug_mode
        }


# Global config instance
config = Config()
