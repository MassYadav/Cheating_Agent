import os
from pathlib import Path

def populate_existing_repo():
    # Target the current directory directly since you already cloned the repo
    root_dir = Path(".")
    print(f"[*] Deploying system architecture into current repository directory...")

    workspace_blueprint = {
        # --- DEVICE A: STREAMING DAEMON PIPELINE ---
        root_dir / "device_a_client" / "requirements.txt": "mss>=9.0.0\nopencv-python-headless>=4.8.0\npyyaml>=6.0.1\n",
        root_dir / "device_a_client" / "config.yaml": (
            "capture:\n  target_fps: 2\n  grayscale_conversion: true\n"
            "network:\n  target_host: \"127.0.0.1\"\n  target_port: 8000\n  protocol: \"udp\"\n"
        ),
        root_dir / "device_a_client" / "src" / "__init__.py": "# Device A Capture Daemon Core Initialization\n",
        root_dir / "device_a_client" / "src" / "main.py": "\"\"\"Background runtime daemon orchestrating frame captures and transport bindings.\"\"\"\n",
        root_dir / "device_a_client" / "src" / "capture.py": "\"\"\"Direct OS Graphic Pipeline Abstraction layer handling native pixel stream access buffers.\"\"\"\n",
        root_dir / "device_a_client" / "src" / "transport.py": "\"\"\"Asynchronous network buffer worker processing low-latency binary payload drops.\"\"\"\n",

        # --- DEVICE B: COGNITIVE AGENT ENGINE & DATA STACK ---
        root_dir / "device_b_backend" / "Dockerfile": (
            "FROM python:3.11-slim\nWORKDIR /app\n"
            "COPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\nCMD [\"uvicorn\", \"src.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        ),
        root_dir / "device_b_backend" / "requirements.txt": (
            "fastapi>=0.100.0\nuvicorn>=0.22.0\nlanggraph>=0.0.10\nlangchain-core>=0.1.0\n"
            "ollama>=0.1.6\nfaiss-cpu>=1.7.4\npydantic>=2.0.0\nprometheus_client>=0.17.0\n"
        ),
        root_dir / "device_b_backend" / "config.py": "import os\n\nOLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')\nEMBEDDING_MODEL = 'nomic-embed-text'\nCOGNITIVE_MODEL = 'qwen2.5-coder:7b'\n",
        root_dir / "device_b_backend" / "src" / "__init__.py": "",
        root_dir / "device_b_backend" / "src" / "main.py": "\"\"\"FastAPI Gateway Server handling ingress screen streams and client state WebSockets.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "agent" / "__init__.py": "",
        root_dir / "device_b_backend" / "src" / "agent" / "state.py": "from typing import TypedDict, List, Optional\n\nclass AgentWorkspaceState(TypedDict):\n    raw_image_bytes: bytes\n    extracted_text: str\n    query_domain: str # CODING, FUNDAMENTALS, APTITUDE\n    detected_complexity: Optional[str]\n    generated_solution: Optional[str]\n    validation_logs: List[str]\n",
        root_dir / "device_b_backend" / "src" / "agent" / "graph.py": "\"\"\"LangGraph engine topology routing control structures through state transitions.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "agent" / "nodes" / "__init__.py": "",
        root_dir / "device_b_backend" / "src" / "agent" / "nodes" / "classifier.py": "\"\"\"Intent analyzer filtering query payloads across multi-label paths.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "agent" / "nodes" / "dsa_expert.py": "\"\"\"Algorithmic template mapper forcing optimized runtime Big-O complexity execution.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "agent" / "nodes" / "rag_engine.py": "\"\"\"Local semantic lookup module binding contextual textbook parameters.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "agent" / "nodes" / "self_critic.py": "\"\"\"Recursive validation block reviewing candidate code logic accuracy patterns.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "rag" / "__init__.py": "",
        root_dir / "device_b_backend" / "src" / "rag" / "indexer.py": "\"\"\"Local storage loader chunking educational knowledge files into embedding tensors.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "rag" / "vector_store.py": "\"\"\"Local FAISS vector operations manager indexing structured knowledge data bases.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "llm" / "__init__.py": "",
        root_dir / "device_b_backend" / "src" / "llm" / "client.py": "\"\"\"Non-blocking Ollama infrastructure connection layer pipelines.\"\"\"\n",
        root_dir / "device_b_backend" / "src" / "llm" / "templates.py": "\"\"\"System prompt dictionaries optimizing precise non-hallucinated syntax boundaries.\"\"\"\n",

        # --- DEVICE B: STREAMING USER INTERFACE SERVICE ---
        root_dir / "device_b_frontend" / "Dockerfile": "FROM node:18-alpine\nWORKDIR /app\nCOPY package.json .\nRUN npm install\nCOPY . .\nCMD [\"npm\", \"start\"]\n",
        root_dir / "device_b_frontend" / "package.json": "{\n  \"name\": \"device-b-frontend\",\n  \"version\": \"1.0.0\",\n  \"private\": true,\n  \"dependencies\": {\n    \"react\": \"^18.2.0\",\n    \"react-dom\": \"^18.2.0\",\n    \"socket.io-client\": \"^4.7.2\"\n  },\n  \"scripts\": {\n    \"start\": \"echo \\\"Frontend Mock Running\\\"\"\n  }\n}\n",
        root_dir / "device_b_frontend" / "tailwind.config.js": "module.exports = { content: ['./src/**/*.{js,jsx}'], theme: { extend: {} }, plugins: [] };\n",
        root_dir / "device_b_frontend" / "src" / "index.js": "import React from 'react';\nimport ReactDOM from 'react-dom';\nimport App from './App';\nReactDOM.render(<App />, document.getElementById('root'));\n",
        root_dir / "device_b_frontend" / "src" / "App.jsx": "import React from 'react';\nexport default function App() { return (<div>Workspace Dashboard Active</div>); }\n",
        root_dir / "device_b_frontend" / "src" / "components" / "CodePresenter.jsx": "import React from 'react';\nexport default function CodePresenter() { return null; }\n",
        root_dir / "device_b_frontend" / "src" / "components" / "ConceptCard.jsx": "import React from 'react';\nexport default function ConceptCard() { return null; }\n",
        root_dir / "device_b_frontend" / "src" / "components" / "StreamMonitor.jsx": "import React from 'react';\nexport default function StreamMonitor() { return null; }\n",

        # --- MONITORING & SYSTEM METRICS OBSERVABILITY ---
        root_dir / "telemetry" / "prometheus.yml": "global:\n  scrape_interval: 5s\nscrape_configs:\n  - job_name: 'assistant_metrics'\n    static_configs:\n      - targets: ['backend:8000']\n",
        root_dir / "telemetry" / "grafana" / "provisioning" / "dashboards" / "system_performance.json": "{\n  \"title\": \"System Performance Dashboard\",\n  \"panels\": []\n}\n"
    }

    for file_path, file_content in workspace_blueprint.items():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Avoid overwriting files you already pulled from GitHub (like README or gitignore)
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file_buffer:
                file_buffer.write(file_content)
            print(f"[+] Created: {file_path}")

    print("\n[+] Monorepo architecture successfully injected into your repository workspace.")

if __name__ == "__main__":
    populate_existing_repo()