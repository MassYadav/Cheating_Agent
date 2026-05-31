from langgraph.graph import StateGraph, END
from src.agent.state import AgentWorkspaceState
from src.agent.nodes.unified_solver import unified_solver_node

def compile_optimized_workflow():
    """
    Compiles a low-overhead, compressed state graph topology.
    Cuts structural node switching complexity down to a single processing edge.
    """
    workflow = StateGraph(AgentWorkspaceState)
    
    # Register our newly engineered unified solver node
    workflow.add_node("unified_solver", unified_solver_node)
    
    # Define an absolute linear execution vector path straight from start to end
    workflow.set_entry_point("unified_solver")
    workflow.add_edge("unified_solver", END)
    
    compiled_graph = workflow.compile()
    return compiled_graph

# Export the runtime graph module engine signature
agent_graph = compile_optimized_workflow()