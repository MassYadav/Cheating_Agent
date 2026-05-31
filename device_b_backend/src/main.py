import logging
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from src.agent.graph import agent_graph

# Configure structured runtime logging schemas
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("backend.main")

# ============================================================
# SELF-CONTAINED API DATA MODELS (Replaces src.schemas)
# ============================================================
class ProcessRequest(BaseModel):
    problem_statement: str
    constraints: Optional[str] = None
    sample_cases: Optional[List[str]] = None

class ProcessResponse(BaseModel):
    status: str
    domain_evaluated: str
    payload: str

# ============================================================
# CORE FASTAPI GATEWAY REBOOT
# ============================================================
app = FastAPI(
    title="Core Cognitive Processing Cluster Node",
    version="2.0.0"
)

# Allow unrestricted cross-origin local network communication handshakes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def system_health_check_handshake():
    return {
        "status": "ONLINE",
        "runtime_environment": "development",
        "active_cognitive_engine": "qwen2.5-coder:7b"
    }

@app.post("/api/v1/process", response_model=ProcessResponse)
async def process_telemetry_stream(payload: ProcessRequest):
    logger.info("Ingress data frame received via HTTP route processing line.")
    
    # Initialize state configuration mapping matching graph expectations
    initial_state = {
        "parsed_payload": payload,
        "retrieved_context_snippets": [],
        "candidate_solution_draft": "",
        "verification_errors": None,
        "execution_cycles": 1
    }
    
    try:
        # Asynchronously invoke our optimized single-pass linear graph
        final_state = await agent_graph.ainvoke(initial_state)
        computed_output = final_state.get("candidate_solution_draft", "Processing error generated empty payloads.")
        
        return ProcessResponse(
            status="SUCCESS",
            domain_evaluated="OPTIMIZED_ENGINE",
            payload=computed_output
        )
    except Exception as runtime_fault:
        logger.error(f"Application router processing pipeline collapsed: {str(runtime_fault)}")
        raise HTTPException(status_code=500, detail=f"Internal Cognitive Core Exception: {str(runtime_fault)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)