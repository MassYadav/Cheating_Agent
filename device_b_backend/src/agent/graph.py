"""LangGraph engine topology routing control structures through state transitions."""
import logging
from langgraph.graph import StateGraph, END
from src.agent.state import AgentWorkspaceState
from src.agent.nodes.classifier import classification_node
from src.agent.nodes.dsa_expert import dsa_expert_node
from src.agent.nodes.rag_engine import rag_engine_node
from src.agent.nodes.self_critic import self_critic_node
from config import settings

logger = logging.getLogger("backend.agent.graph")

def routing_conditional_edge(state: AgentWorkspaceState) -> str:
    """
    Evaluates runtime memory space vectors and decides the path forward.
    Acts as a dynamic traffic cop between specialized AI node clusters.
    """
    domain = state.get("query_domain", "UNKN").upper()
    
    if domain == "CODING":
        return "route_to_dsa"
    elif domain == "FUNDAMENTALS":
        return "route_to_rag"
    else:
        # Default fallback route processing for Aptitude / Logical puzzles
        return "route_to_generic_reasoner"

def validation_conditional_edge(state: AgentWorkspaceState) -> str:
    """
    Acts as a systemic circuit breaker. Checks the code self-critic output:
    If flaws exist, it reroutes backward; if perfect, it shuts down the graph pipeline.
    """
    logs = state.get("validation_logs", [])
    current_loops = state.get("loop_count", 0)
    
    # Circuit breaker condition to prevent infinite token budget expenditure
    if current_loops >= settings.MAX_AGENT_LOOPS:
        logger.warning(f"Maximum compilation loop guard constraint reached ({settings.MAX_AGENT_LOOPS}). Forcing output break.")
        return "terminate_workflow"
        
    if logs and "PASSED" in logs[-1]:
        return "terminate_workflow"
    
    logger.info("Self-Critic detected code syntax anomalies or complexity sub-optimality. Cycling back.")
    return "recalculate_dsa_node"

# ------------------------------------------------------------------------
# Graph Compilation Phase
# ------------------------------------------------------------------------

# 1. Initialize State Graph Workspace Engine with explicit state definitions
workflow_builder = StateGraph(AgentWorkspaceState)

# 2. Register Processing Nodes to the Global Topology
workflow_builder.add_node("intent_classifier", classification_node)
workflow_builder.add_node("dsa_solution_generator", dsa_expert_node)
workflow_builder.add_node("rag_knowledge_retriever", rag_engine_node)
workflow_builder.add_node("automated_self_critic", self_critic_node)

# 3. Establish Core Static Workflow Sequences
workflow_builder.set_entry_point("intent_classifier")

# 4. Integrate High-Performance Multi-Path Conditional Routing Logic
workflow_builder.add_conditional_edges(
    "intent_classifier",
    routing_conditional_edge,
    {
        "route_to_dsa": "dsa_solution_generator",
        "route_to_rag": "rag_knowledge_retriever",
        "route_to_generic_reasoner": "dsa_solution_generator" # Maps to general model fallback
    }
)

# 5. Connect Task Managers to the Validation Layer
workflow_builder.add_edge("rag_knowledge_retriever", "automated_self_critic")
workflow_builder.add_edge("dsa_solution_generator", "automated_self_critic")

# 6. Apply Feedback Loops for Real-Time Self-Correction Lifecycle Management
workflow_builder.add_conditional_edges(
    "automated_self_critic",
    validation_conditional_edge,
    {
        "terminate_workflow": END,
        "recalculate_dsa_node": "dsa_solution_generator"
    }
)

# Compile the execution pipeline topology into a running thread-safe instance
compiled_agentic_pipeline = workflow_builder.compile()
