import os

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
EMBEDDING_MODEL = 'nomic-embed-text'
COGNITIVE_MODEL = 'qwen2.5-coder:7b'


import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyHttpUrl

class SystemSettings(BaseSettings):
    """
    Enterprise-grade system settings manager.
    Validates environment variables dynamically at runtime initialization.
    """
    # System Environment
    ENV: str = Field(default="development", description="Runtime environment topology")
    DEBUG: bool = Field(default=False, description="Global debug flag toggle")
    
    # Local Inference Settings (Ollama / vLLM)
    OLLAMA_HOST: str = Field(
        default="http://localhost:11434", 
        description="Local boundary network URL for the open-source LLM engine"
    )
    COGNITIVE_MODEL: str = Field(
        default="qwen2.5-coder:7b", 
        description="Primary model for complex algorithm synthesis and code translation"
    )
    EMBEDDING_MODEL: str = Field(
        default="nomic-embed-text", 
        description="Lightweight local embedding tensor generator"
    )
    
    # Vector Database Engine Storage Paths
    FAISS_INDEX_PATH: str = Field(
        default="./local_faiss_index", 
        description="Persistent disk layout directory for CS Fundamentals knowledge cache"
    )
    
    # System Engineering Latency Thresholds
    MAX_AGENT_LOOPS: int = Field(
        default=5, 
        description="Circuit-breaker threshold preventing infinite recursive agent reasoning cycles"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate a single source of truth configuration token for the backend lifecycle
settings = SystemSettings()