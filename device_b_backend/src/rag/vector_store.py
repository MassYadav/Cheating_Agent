"""Local FAISS vector operations manager indexing structured knowledge data bases."""
import os
import json
import logging
import numpy as np
import faiss
from typing import List, Dict, Any
from config import settings
from src.llm.client import inference_driver

logger = logging.getLogger("backend.rag.vector_store")

class LocalVectorDB:
    """
    High-performance native FAISS vector engine.
    Handles embedding storage and sub-millisecond semantic similarity searches.
    """
    def __init__(self):
        self.index_dir = settings.FAISS_INDEX_PATH
        self.index_file = os.path.join(self.index_dir, "base_matrix.index")
        self.metadata_file = os.path.join(self.index_dir, "metadata.json")
        self.index = None
        self.metadata: Dict[str, str] = {}
        
        # Auto-initialize the index layout context
        self._initialize_database_layer()

    def _initialize_database_layer(self):
        """Creates or loads existing index mappings from persistent disk space."""
        os.makedirs(self.index_dir, exist_ok=True)
        
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            try:
                logger.info("Loading existing FAISS index vector map from disk storage matrix...")
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, "r", encoding="utf-8") as file_buffer:
                    self.metadata = json.load(file_buffer)
            except Exception as error:
                logger.error(f"Failed to read existing index files: {str(error)}. Resetting db.")
                self._create_empty_index()
        else:
            self._create_empty_index()

    def _create_empty_index(self):
        """Instantiates a clean IndexFlatL2 matrix based on standard 768-dimension vectors."""
        # nomic-embed-text outputs 768 dimensional dense vector allocations
        dimension = 768
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = {}
        logger.info("Initialized brand new empty local FAISS execution matrix.")

    async def add_documents(self, documents: List[str]):
        """Transforms documents into vector embeddings and appends them into storage mapping safely."""
        if not documents:
            return

        embeddings_list = []
        start_id = self.index.ntotal

        for document in documents:
            if not document.strip():
                continue
            # Extract vector array via local inference driver pipeline
            vector = await inference_driver.generate_embeddings(document)
            if vector:
                embeddings_list.append(vector)
                # Map vector item offsets directly back to source text structures
                self.metadata[str(len(embeddings_list) - 1 + start_id)] = document

        if embeddings_list:
            vector_matrix = np.array(embeddings_list).astype("float32")
            self.index.add(vector_matrix)
            self._save_state_to_disk()
            logger.info(f"Successfully processed and appended {len(embeddings_list)} documents into database vector space.")

    def _save_state_to_disk(self):
        """Serializes current binary arrays and lookup json documents down to file schemas."""
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "w", encoding="utf-8") as file_buffer:
            json.dump(self.metadata, file_buffer, ensure_ascii=False, indent=2)
        logger.info("State synchronization to disk storage layer completed safely.")

    async def similarity_search(self, query: str, top_k: int = 3) -> List[str]:
        """Performs optimized similarity searches and returns top text matches."""
        if self.index.ntotal == 0:
            logger.warning("Attempted vector search against an empty database matrix.")
            return []

        query_vector = await inference_driver.generate_embeddings(query)
        if not query_vector:
            return []

        # Convert query input data into native floating-point structure formats
        query_matrix = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_matrix, top_k)

        matched_results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            doc_str = self.metadata.get(str(idx))
            if doc_str:
                matched_results.append(doc_str)

        return matched_results

# Initialize engine token for system dependency distribution routing
vector_db = LocalVectorDB()