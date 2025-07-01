"""
LLM Provider Management
Unified interface for different LLM providers (Groq, Together AI, etc.)
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
from together import Together

# Load environment variables
load_dotenv(Path(".env"), override=True)


class LLMProvider:
    """Unified interface for different LLM providers"""

    def __init__(self):
        self.groq_client: Optional[Groq] = None
        self.together_client: Optional[Together] = None
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize available LLM clients"""
        # Initialize Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            self.groq_client = Groq(api_key=groq_key)
            print("[+] Groq client initialized")

        # Initialize Together AI
        together_key = os.getenv("TOGETHER_API_KEY")
        if together_key:
            self.together_client = Together(api_key=together_key)
            print("[+] Together AI client initialized")

    def generate_response(self, prompt: str, provider: str = "groq", max_tokens: int = 500) -> str:
        """Generate response using specified provider, with single fallback (no recursion)"""
        tried = set()
        providers_to_try = [provider, "together" if provider == "groq" else "groq"]
        for prov in providers_to_try:
            if prov in tried:
                continue
            tried.add(prov)
            try:
                if prov == "groq" and self.groq_client:
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama3-8b-8192",
                        max_tokens=max_tokens,
                        temperature=0.3,
                    )
                    return response.choices[0].message.content
                elif prov == "together" and self.together_client:
                    response = self.together_client.chat.completions.create(
                        model="meta-llama/Llama-3-8b-chat-hf",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=0.3,
                    )
                    return response.choices[0].message.content
            except Exception as e:
                print(f"[!] Error with {prov}: {e}")
                continue
        return f"[!] All providers failed or are not configured."

    def is_available(self, provider: str) -> bool:
        """Check if a provider is available"""
        if provider == "groq":
            return self.groq_client is not None
        elif provider == "together":
            return self.together_client is not None
        return False

    def list_available_providers(self) -> list:
        """List all available providers"""
        providers = []
        if self.groq_client:
            providers.append("groq")
        if self.together_client:
            providers.append("together")
        return providers
