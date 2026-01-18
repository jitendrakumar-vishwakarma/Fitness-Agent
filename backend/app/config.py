"""
Configuration and environment settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Fitness AI Agent"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8501"

    # Database
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # LLM - Supports: gemini, openai, groq, ollama
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    LLM_PROVIDER: str = "gemini"  # Options: "gemini", "openai", "groq", "ollama"
    LLM_MODEL: str = "gemini-pro"  # Model name for the selected provider

    # Ollama Settings (for local LLM)
    OLLAMA_BASE_URL: str = "http://localhost:11434"  # Ollama server URL
    OLLAMA_MODEL: str = "llama3.2"  # Default Ollama model

    # Google APIs
    GOOGLE_CALENDAR_CREDENTIALS: str = ""
    GOOGLE_FIT_CREDENTIALS: str = ""

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Also search in parent directory
        extra = "ignore"


settings = Settings(_env_file=[".env", "../.env"])
