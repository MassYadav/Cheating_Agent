"""Intent analyzer filtering query payloads across multi-label paths."""
import logging
from src.agent.state import AgentWorkspaceState, ExtractedQuerySchema
from src.llm.client import inference_driver
from src.llm.templates import CLASSIFICATION_PROMPT

logger = logging.getLogger("backend.agent.nodes.classifier")

async def classification_node(state: AgentWorkspaceState) -> AgentWorkspaceState:
    """
    Asynchronous intent analysis node.
    Parses the raw input data stream and routes the workflow state vector.
    """
    logger.info("Initializing context classification node execution loop...")
    
    # Track the loop iteration to prevent infinite processing cycles
    current_loops = state.get("loop_count", 0)
    state["loop_count"] = current_loops + 1
    
    # Fallback default text payload if the stream inputs are empty
    input_text = "Standard system health ping check query."
    
    # In a live frame scenario, OCR/Vision text parsing populates this space.
    # For initial integration validation, we pull from the available payload data.
    if state.get("parsed_payload"):
        input_text = state["parsed_payload"].problem_statement
    else:
        # Mock structured data schema block if first-time empty instantiation initialization
        state["parsed_payload"] = ExtractedQuerySchema(
            problem_statement="Given a graph, detect if a cycle exists using DFS.",
            constraints="N <= 10^5, E <= 10^5",
            sample_cases="Input: [[1,2],[2,3],[3,1]] -> Output: true"
        )
        input_text = state["parsed_payload"].problem_statement

    # Dispatch request down to our local asynchronous model driver
    raw_classification_response = await inference_driver.generate_completion(
        system_prompt=CLASSIFICATION_PROMPT,
        user_prompt=input_text
    )

    # Sanitize and validate the string return packet bounds
    validated_domain = "UNKN"
    if raw_classification_response:
        cleaned_token = raw_classification_response.strip().upper()
        if cleaned_token in ["CODING", "FUNDAMENTALS", "APTITUDE", "UNKN"]:
            validated_domain = cleaned_token

    logger.info(f"Classification classification boundary mapping completed: Matrix -> [{validated_domain}]")
    
    # Update and mutate the graph state memory map safely
    state["query_domain"] = validated_domain
    state["target_programming_language"] = "Java" # Explicit project preference initialization
    
    return state