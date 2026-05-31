"""FastAPI Gateway Server handling ingress screen streams and client state WebSockets."""
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from config import settings
from src.agent.state import ExtractedQuerySchema, AgentWorkspaceState
from src.agent.graph import compiled_agentic_pipeline

# Configure uniform high-throughput systems logging layout
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("backend.main")

# Initialize web framework container
app = FastAPI(
    title="Edge-Native Cognitive Assistant Core Backend",
    version="1.0.0",
    debug=settings.DEBUG
)

# Apply global cross-origin resource sharing (CORS) rules for cross-device visibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits edge-devices/smartphones to read streams natively
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StreamInputRequest(BaseModel):
    """Network validation wrapper matching the internal pydantic schema layout."""
    problem_statement: str
    constraints: Optional[str] = None
    sample_cases: Optional[str] = None

@app.get("/health")
async def system_health_ping_check():
    """System heartbeat checkpoint endpoint tracking cluster connectivity status."""
    return {
        "status": "ONLINE",
        "runtime_environment": settings.ENV,
        "active_cognitive_engine": settings.COGNITIVE_MODEL
    }

@app.post("/api/v1/process")
async def process_incoming_stream_payload(request: StreamInputRequest):
    """
    HTTP REST Ingress endpoint. Processes captured screen payloads 
    synchronously through the local state machine framework.
    """
    try:
        logger.info("Ingress data frame received via HTTP route processing line.")
        
        # Build strict execution state footprint memory allocation map
        initial_state: AgentWorkspaceState = {
            "raw_image_bytes": None,
            "parsed_payload": ExtractedQuerySchema(
                problem_statement=request.problem_statement,
                constraints=request.constraints,
                sample_cases=request.sample_cases
            ),
            "query_domain": "UNKN",
            "detected_complexity": None,
            "target_programming_language": "Java",
            "retrieved_context_snippets": [],
            "candidate_solution_draft": None,
            "final_polished_output": None,
            "validation_logs": [],
            "loop_count": 0
        }
        
        # Run async compute matrices against compiled LangGraph execution graph
        final_computed_state = await compiled_agentic_pipeline.ainvoke(initial_state)
        
        return {
            "domain_evaluated": final_computed_state.get("query_domain"),
            "execution_loops": final_computed_state.get("loop_count"),
            "validation_history": final_computed_state.get("validation_logs"),
            "payload": final_computed_state.get("final_polished_output")
        }
        
    except Exception as system_fault:
        logger.error(f"Critical execution error inside gateway processing pipeline: {str(system_fault)}")
        raise HTTPException(status_code=500, detail="Internal AI Engine Processing Failure")

@app.websocket("/ws/stream")
async def real_time_websocket_stream_gateway(websocket: WebSocket):
    """
    High-frequency WebSocket channel routing real-time state 
    matrices smoothly to edge display monitors or companion smartphones.
    """
    await websocket.accept()
    logger.info("Persistent duplex WebSocket channel connected from external display node client.")
    
    try:
        while True:
            # Sit in non-blocking wait loop waiting for async incoming frames
            client_raw_bytes = await websocket.receive_bytes()
            
            # Placeholder for future live-stream binary manipulation blocks
            # Directly routes diagnostic confirm signals back down the line to client pipe
            await websocket.send_json({
                "status": "FRAME_ACK",
                "bytes_processed": len(client_raw_bytes),
                "telemetry_state": "READY"
            })
            
    except WebSocketDisconnect:
        logger.warning("Active WebSocket connection disconnected from edge device.")
    except Exception as socket_fault:
        logger.error(f"WebSocket interface encountered a runtime failure sequence: {str(socket_fault)}")
        await websocket.close()