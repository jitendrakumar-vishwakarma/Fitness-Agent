"""
LLM client for Gemini, OpenAI, Groq, and Ollama
"""

from typing import Optional, Dict, Any
import google.generativeai as genai
from openai import AsyncOpenAI
import httpx
import json


class LLMClient:
    """Unified LLM client supporting Gemini, OpenAI, Groq, and Ollama"""

    def __init__(
        self,
        provider: str,
        api_key: str = None,
        model: str = None,
        base_url: str = None,
    ):
        """
        Initialize LLM client

        Args:
            provider: "gemini", "openai", "groq", or "ollama"
            api_key: API key (not needed for Ollama)
            model: Model name
            base_url: Base URL for Ollama (default: http://localhost:11434)
        """
        self.provider = provider.lower()
        self.model = model
        self.base_url = base_url

        if self.provider == "gemini":
            if not api_key:
                raise ValueError("API key required for Gemini")
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model or "gemini-pro")

        elif self.provider == "openai":
            if not api_key:
                raise ValueError("API key required for OpenAI")
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = model or "gpt-3.5-turbo"

        elif self.provider == "groq":
            if not api_key:
                raise ValueError("API key required for Groq")
            # Groq uses OpenAI-compatible API
            self.client = AsyncOpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            self.model = model or "llama-3.1-70b-versatile"

        elif self.provider == "ollama":
            # Ollama runs locally, no API key needed
            self.base_url = base_url or "http://localhost:11434"
            self.model = model or "llama3.2"
            # Increase timeout for Ollama (can be slow on first run)
            self.client = httpx.AsyncClient(timeout=300.0)

        else:
            raise ValueError(
                f"Unsupported provider: {provider}. Choose from: gemini, openai, groq, ollama"
            )

    async def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None
    ) -> str:
        """Generate text from prompt"""

        if self.provider == "gemini":
            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text

        elif self.provider in ["openai", "groq"]:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        elif self.provider == "ollama":
            # Ollama API call
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                },
            }

            if max_tokens:
                payload["options"]["num_predict"] = max_tokens

            response = await self.client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")

    async def generate_json(
        self, prompt: str, schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate structured JSON output"""

        json_prompt = f"{prompt}\n\nRespond with valid JSON only."
        response = await self.generate(json_prompt, temperature=0.3)

        # Use robust cleaning utility
        from app.utils.output_parsers import clean_llm_response

        cleaned_response = clean_llm_response(response)

        return json.loads(cleaned_response)

    async def close(self):
        """Close the client connection (for Ollama)"""
        if self.provider == "ollama" and hasattr(self, "client"):
            await self.client.aclose()
