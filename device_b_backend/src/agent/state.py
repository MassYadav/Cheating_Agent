
from typing import TypedDict, List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExtractedQuerySchema(BaseModel):
    """Structured operational definition parsed from raw contextual feeds."""
    problem_statement: str = Field(description="The primary question or task description text extracted.")
    constraints: Optional[str] = Field(default=None, description="Time complexity parameters, spatial limits, or data scale values.")
    sample_cases: Optional[str] = Field(default=None, description="Optional baseline test cases provided within the problem window.")

class AgentWorkspaceState(TypedDict):
    """
    Global memory allocation matrix for the LangGraph execution flow.
    Tracks state vectors through deterministic and stochastic reasoning layers.
    """
    # Raw Data Pipelines
    raw_image_bytes: Optional[bytes]
    parsed_payload: Optional[ExtractedQuerySchema]
    
    # Dynamic Classification Vector
    query_domain: str  # Strictly routed across: "CODING", "FUNDAMENTALS", "APTITUDE", "UNKN"
    
    # Optimization & Reasoning Layer Parameters
    detected_complexity: Optional[str]  # e.g., O(N), O(N log N) bounds
    target_programming_language: str   # e.g., "Java", "Python"
    
    # Execution Output Channel Structures
    retrieved_context_snippets: List[str]
    candidate_solution_draft: Optional[str]
    final_polished_output: Optional[str]
    
    # Evaluator Observability Log Array
    validation_logs: List[str]
    loop_count: int