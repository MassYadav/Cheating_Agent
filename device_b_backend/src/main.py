import logging
import sys
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from src.agent.graph import agent_graph

# Configure professional structured runtime logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("backend.main")

# ============================================================
# DATA MODEL SCHEMAS
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
# WEBSOCKET REAL-TIME BROADCAST MANAGER
# ============================================================
class MobileDashboardManager:
    """Manages active smartphone and secondary device browser push-notification sockets."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"[+] Mobile client paired. Active sockets: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"[-] Mobile client disconnected. Remaining: {len(self.active_connections)}")

    async def broadcast_solution(self, message: str):
        """Pushes the synthesized code payload instantly to all connected phone screens."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to push message over dead socket lane: {str(e)}")

broadcast_hub = MobileDashboardManager()

# ============================================================
# APP INITIALIZATION
# ============================================================
app = FastAPI(title="Core Cognitive Processing Hub", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MOBILE DASHBOARD UI (Ultra-Clean Responsive Dark Mode HTML)
# ============================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dashboard Core</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 15px;
            display: flex;
            flex-direction: column;
            height: 100vh;
            box-sizing: border-box;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #21262d;
            padding-bottom: 8px;
            margin-bottom: 10px;
        }
        .status {
            font-size: 11px;
            text-transform: uppercase;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 10px;
            letter-spacing: 0.5px;
        }
        .online { background-color: #238636; color: #ffffff; }
        .offline { background-color: #da3633; color: #ffffff; }
        .content-area {
            flex: 1;
            overflow-y: auto;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        }
        .placeholder {
            color: #8b949e;
            text-align: center;
            margin-top: 40%;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <h3 style="margin:0; font-size:16px; color:#58a6ff;">Cognitive Stream</h3>
        <div id="status-badge" class="status offline">Connecting</div>
    </div>
    <div id="output-pane" class="content-area">
        <div class="placeholder">Awaiting target system hotkey dispatch trigger...</div>
    </div>

    <script>
        const outputPane = document.getElementById('output-pane');
        const statusBadge = document.getElementById('status-badge');
        
        function connectStreamingSocket() {
            // Automatically determines server host dynamically across network boundaries
            const wsUrl = `ws://${window.location.host}/ws/stream`;
            const socket = new WebSocket(wsUrl);

            socket.onopen = () => {
                statusBadge.textContent = 'Standby';
                statusBadge.className = 'status online';
            };

            socket.onmessage = (event) => {
                // Instantly injects incoming Markdown/Java payloads into display layer
                outputPane.innerHTML = event.data;
                outputPane.scrollTop = 0; // Auto-scroll to top of new answer
            };

            socket.onclose = () => {
                statusBadge.textContent = 'Dropped';
                statusBadge.className = 'status offline';
                // Safe exponential backoff reconnection protocol loop
                setTimeout(connectStreamingSocket, 3000);
            };
        }
        
        // Boot connection layer immediately
        connectStreamingSocket();
    </script>
</body>
</html>
"""

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_mobile_dashboard():
    """Serves the remote dark-mode system monitoring front-end console to browsers."""
    return DASHBOARD_HTML

@app.get("/health")
async def system_health_check_handshake():
    return {"status": "ONLINE"}

# ============================================================
# WEBSOCKET ROUTE ENDPOINT
# ============================================================
@app.websocket("/ws/stream")
async def websocket_streaming_endpoint(websocket: WebSocket):
    """Establishes persistent bidirectional telemetry synchronization lanes."""
    await broadcast_hub.connect(websocket)
    try:
        while True:
            # Keeps connection channel alive and listening for client heartbeat signals
            await websocket.receive_text()
    except WebSocketDisconnect:
        broadcast_hub.disconnect(websocket)

# ============================================================
# DATA INGRESS TERMINAL
# ============================================================
@app.post("/api/v1/process", response_model=ProcessResponse)
async def process_telemetry_stream(payload: ProcessRequest):
    logger.info("Ingress data frame received via HTTP route processing line.")
    
    initial_state = {
        "parsed_payload": payload,
        "retrieved_context_snippets": [],
        "candidate_solution_draft": "",
        "verification_errors": None,
        "execution_cycles": 1
    }
    
    try:
        # Execute your optimized single-pass linear LangGraph workflow loop
        final_state = await agent_graph.ainvoke(initial_state)
        computed_output = final_state.get("candidate_solution_draft", "Error processing empty matrix payload arrays.")
        
        # WEBSOCKET BROADCAST: Instantly pushes the answer straight to your connected phone browser
        await broadcast_hub.broadcast_solution(computed_output)
        
        return ProcessResponse(
            status="SUCCESS",
            domain_evaluated="OPTIMIZED_ENGINE",
            payload="Payload pushed out to remote broadcast matrices successfully."
        )
    except Exception as runtime_fault:
        logger.error(f"Application router processing pipeline collapsed: {str(runtime_fault)}")
        raise HTTPException(status_code=500, detail=f"Internal Cognitive Core Exception: {str(runtime_fault)}")