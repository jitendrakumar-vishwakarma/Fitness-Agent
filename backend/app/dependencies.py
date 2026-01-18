"""
Dependency injection for database, LLM, and authentication
"""

from functools import lru_cache
from app.config import settings
from app.tools.db import SupabaseClient
from app.tools.llm import LLMClient


@lru_cache()
def get_db_client() -> SupabaseClient:
    """Get Supabase database client"""
    return SupabaseClient(url=settings.SUPABASE_URL, key=settings.SUPABASE_KEY)


@lru_cache()
def get_llm_client() -> LLMClient:
    """Get LLM client (Gemini, OpenAI, Groq, or Ollama)"""

    provider = settings.LLM_PROVIDER.lower()

    # Select appropriate API key based on provider
    api_key_map = {
        "gemini": settings.GEMINI_API_KEY,
        "openai": settings.OPENAI_API_KEY,
        "groq": settings.GROQ_API_KEY,
        "ollama": None,  # Ollama doesn't need API key
    }

    api_key = api_key_map.get(provider)

    # Get model name (use Ollama model if provider is Ollama)
    model = settings.OLLAMA_MODEL if provider == "ollama" else settings.LLM_MODEL

    # Get base URL for Ollama
    base_url = settings.OLLAMA_BASE_URL if provider == "ollama" else None

    return LLMClient(
        provider=provider,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )
