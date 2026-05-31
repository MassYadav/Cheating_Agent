"""Local semantic lookup module binding contextual textbook parameters."""
import logging
from src.agent.state import AgentWorkspaceState
from src.rag.vector_store import vector_db

logger = logging.getLogger("backend.agent.nodes.rag_engine")

async def rag_engine_node(state: AgentWorkspaceState) -> AgentWorkspaceState:
    """
    Asynchronous Knowledge Retrieval Node.
    Queries the live local vector database to pull absolute context facts with zero hallucination.
    """
    logger.info("Initializing semantic local retrieval search engine execution query...")
    
    payload = state.get("parsed_payload")
    if not payload:
        logger.warning("Empty payload dataset sent to RAG engine. Skipping vector retrieval.")
        return state

    # Query extraction from parsed screen capture text data stream
    query_string = payload.problem_statement
    logger.info(f"Extracting vector mapping segments matching token request query: '{query_string[:40]}...'")

    try:
        # Perform live native matrix search against local FAISS database files
        retrieved_contexts = await vector_db.similarity_search(query=query_string, top_k=2)
        
        if retrieved_contexts:
            logger.info(f"Matched {len(retrieved_contexts)} highly relevant context fragments from storage index.")
            state["retrieved_context_snippets"] = retrieved_contexts
            state["candidate_solution_draft"] = (
                f"Sourced Context Knowledge Grounding:\n" + "\n".join(retrieved_contexts)
            )
        else:
            logger.warning("Zero context vectors matched the input criteria. Passing execution chain upstream.")
            state["retrieved_context_snippets"] = []
            state["candidate_solution_draft"] = "System Notification: Zero direct knowledge base facts matched query bounds."
            
    except Exception as data_fault:
        logger.error(f"Failed to query semantic store components within graph loop execution: {str(data_fault)}")
        state["retrieved_context_snippets"] = []
        
    return state