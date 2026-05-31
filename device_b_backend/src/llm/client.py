"""Non-blocking Ollama infrastructure connection layer pipelines."""
import logging
from typing import Optional, Dict, Any
import ollama
from ollama import AsyncClient
from config import settings

logger = logging.getLogger("backend.llm.client")

class LocalInferenceDriver:
    """
    Asynchronous driver wrapper for local open-source LLM engines.
    Optimized for high-throughput, low-latency node execution loops.
    """
    def __init__(self):
        # Initialize the asynchronous client bound to our type-validated host configuration
        self.client = AsyncClient(host=settings.OLLAMA_HOST)
        self.cognitive_model = settings.COGNITIVE_MODEL
        self.embedding_model = settings.EMBEDDING_MODEL

    async def generate_completion(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Executes a non-blocking inference sequence against the active cognitive model.
        """
        try:
            logger.info(f"Dispatching inference matrix payload to local model: {self.cognitive_model}")
            
            response = await self.client.generate(
                model=self.cognitive_model,
                system=system_prompt,
                prompt=user_prompt,
                options={
                    "temperature": 0.1,  # Lower temperature strictly enforces deterministic reasoning bounds
                    "top_p": 0.9,
                    "seed": 42           # Sets fixed seed for repeatable architectural validation runs
                }
            )
            return response.get('response', '').strip()
            
        except Exception as error:
            logger.error(f"Inference failure occurred inside LocalInferenceDriver execution block: {str(error)}")
            return None

    async def generate_embeddings(self, text_payload: str) -> Optional[Any]:
        """
        Transforms text arrays into semantic vector tensors for local RAG operations.
        """
        try:
            response = await self.client.embeddings(
                model=self.embedding_model,
                prompt=text_payload
            )
            return response.get('embedding')
        except Exception as error:
            logger.error(f"Failed to extract vector embeddings locally: {str(error)}")
            return None

# Instantiate a thread-safe singleton instance for global backend reuse
inference_driver = LocalInferenceDriver()