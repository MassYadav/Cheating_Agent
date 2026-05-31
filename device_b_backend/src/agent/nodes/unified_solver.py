import logging
from src.agent.state import AgentWorkspaceState
from src.llm.client import inference_driver
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
    Minimizes localized CPU pre-fill latency boundaries by combining evaluation steps.
    """
    logger.info("Initializing high-performance consolidated solver pipeline...")

    payload = state.get("parsed_payload")
    if not payload or not payload.problem_statement:
        logger.warning("Null context frame submitted to processing array.")
        return state

    raw_query = payload.problem_statement

    # 1. High-speed local similarity index lookup (Sub-millisecond FAISS retrieval)
    logger.info("Executing parallel vector matrix background lookup...")
    retrieved_contexts = await vector_db.similarity_search(query=raw_query, top_k=2)

    grounding_context = ""
    if retrieved_contexts:
        grounding_context = "\n[VERIFIED DATABASE CONTEXT]\n" + "\n".join(retrieved_contexts) + "\n"
        state["retrieved_context_snippets"] = retrieved_contexts

    # 2. Formulate consolidated runtime execution prompt
    execution_prompt = f"{grounding_context}Target Input Problem:\n{raw_query}"

    logger.info("Dispatching unified computational matrix directly to local model inference driver...")
    try:
        raw_response = await inference_driver.generate_response(
            system_prompt=CONSOLIDATED_SYSTEM_PROMPT,
            user_prompt=execution_prompt
        )
        state["candidate_solution_draft"] = raw_response
        logger.info("Consolidated structural optimization cycle successfully executed.")
    except Exception as hardware_fault:
        logger.error(f"Unified solver node encountered an inference failure: {str(hardware_fault)}")
        state["candidate_solution_draft"] = "System Fault: Local optimization loop processing error."

    return state