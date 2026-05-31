import logging
import httpx
from src.agent.state import AgentWorkspaceState
from src.rag.vector_store import vector_db

logger = logging.getLogger("backend.agent.nodes.unified_solver")

# High-density industrial prompt instructing the model to parallel-process tasks internally
CONSOLIDATED_SYSTEM_PROMPT = """You are an elite, 25-year veteran competitive programming coach and computer science systems architect. 
Your objective is to analyze the raw text input provided via screen extraction and produce an un-bypassable, highly optimized solution.

You must perform the following tasks internally within a single processing loop:
1. IDENTIFY DOMAIN: Categorize the input instantly into [CODING] (Data Structures & Algorithms) or [THEORY] (OS, DBMS, Computer Networks).
2. CORE SYNTHESIS:
   - If [CODING]: Generate a clean, production-grade Java solution. The code must hit the absolute lowest theoretical Time Complexity (TC) and Space Complexity (SC). Use optimal DSA approaches (e.g., Two-Pointer techniques, Monotonic Stacks, Sliding Windows, Bit Manipulation, or Dynamic Programming).
   - If [THEORY]: Pull core concepts instantly from your knowledge base to provide a highly precise, definitive answer. Avoid fluff.
3. INTERNAL CRITIC: Before printing, dry-run your solution mentally against extreme edge cases (null inputs, out-of-bounds metrics, massive array scales). Self-correct any syntax errors instantly.

Provide your output using this exact structural template:
[DOMAIN: INSERT CATEGORY HERE]
### Problem Analysis
- **Core Strategy**: Brief, high-level structural approach breakdown.
- **Time Complexity**: Optimal big-O mathematical analysis.
- **Space Complexity**: Optimal memory footprint optimization analysis.

### Implementation
```java
// Complete, clean, highly optimized Java code with concise system comments
"""
async def unified_solver_node(state: AgentWorkspaceState) -> AgentWorkspaceState:
    """
    Single-Pass High-Performance Cognitive Inference Engine.
    Communicates directly with the Ollama container subsystem via async HTTP streams.
    """
    logger.info("Initializing high-performance consolidated solver pipeline...")

    payload = state.get("parsed_payload")
    if not payload or not payload.problem_statement:
        logger.warning("Null context frame submitted to processing array.")
        return state

    raw_query = payload.problem_statement

    # 1. High-speed local similarity index lookup (Sub-millisecond FAISS retrieval)
    logger.info("Executing parallel vector matrix background lookup...")
    try:
        retrieved_contexts = await vector_db.similarity_search(query=raw_query, top_k=2)
    except Exception as e:
        logger.warning(f"Vector lookup bypassed or uninitialized: {str(e)}")
        retrieved_contexts = []

    grounding_context = ""
    if retrieved_contexts:
        grounding_context = "\n[VERIFIED DATABASE CONTEXT]\n" + "\n".join(retrieved_contexts) + "\n"
        state["retrieved_context_snippets"] = retrieved_contexts

    # 2. Formulate consolidated runtime execution prompt
    execution_prompt = f"{grounding_context}Target Input Problem:\n{raw_query}"

    logger.info("Dispatching optimized matrix request directly to local Ollama API engine...")
    try:
        # Bypassing the abstract wrapper class and hitting the live daemon directly on port 11434
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5-coder:7b",
                    "prompt": execution_prompt,
                    "system": CONSOLIDATED_SYSTEM_PROMPT,
                    "stream": False
                }
            )

            if response.status_code == 200:
                raw_response = response.json().get("response", "Empty response matrix array generated.")
                state["candidate_solution_draft"] = raw_response
                logger.info("Consolidated structural optimization cycle successfully executed.")
            else:
                logger.error(f"Ollama server returned an invalid state code: {response.status_code}")
                state["candidate_solution_draft"] = f"Server Error: Ollama engine returned status {response.status_code}"

    except Exception as hardware_fault:
        logger.error(f"Unified solver node encountered an network inference failure: {str(hardware_fault)}")
        state["candidate_solution_draft"] = "System Fault: Local optimization loop processing error."

    return state

