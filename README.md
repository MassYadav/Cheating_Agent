# Cheating_Agent

## NexusStream: Distributed Cross-Device Multi-Agent Context Orchestrator

`Cheating_Agent` is a localized multi-agent intelligence platform designed to extract, orchestrate, synthesize, and stream high-density technical screen data across distributed hardware boundaries in real time.

The architecture separates:
- **Device A**: Data ingestion client
- **Device B**: Cognitive computation graph server
- **Mobile Dashboard**: Air-gapped browser interface for secure result delivery

This separation reduces the local processing footprint, preserves execution isolation, and supports secure cross-device interaction.

---

## 🧠 System Architecture

```text
[Monitor Screen Workspace]
          │
          ▼  (Sub-millisecond capture)
   [Device A: Client Core] ──(Async HTTP POST)──► [Device B: FastAPI Gateway]
          │                                       │
   (Debounce guard)                       (FAISS similarity search)
          │                                       ▼
   [Smartphone Browser] ◄──(WebSockets stream)── [Single-Pass LangGraph Node]
```

### Components

- **Ingestion Client**: Captures screen content and sends text payloads to the backend.
- **Backend Server**: Receives requests, performs vector retrieval, and runs a compact inference graph.
- **Dashboard Interface**: Streams results back to a mobile browser using WebSockets.

---

## ⚙️ Technology Stack

| Layer | Component | Technologies | Goal |
|---|---|---|---|
| Ingestion | Device A client | Python, `pynput`, `mss`, EasyOCR | Fast frame capture and text extraction |
| Orchestration | Backend API | FastAPI, AsyncIO, Uvicorn | High-concurrency request handling |
| Cognitive Engine | Inference graph | LangGraph, Ollama, `qwen2.5-coder` | Single-pass reasoning and code synthesis |
| Streaming UI | Browser interface | WebSockets, HTML5, CSS3 | Low-latency full-duplex updates |

---

## 🚀 Key Engineering Optimizations

1. **Single-Pass Cognitive Compilation**
   - Combines domain detection, code generation, and semantic self-critique in one inference pass.
   - Eliminates sequential multi-node LLM execution, reducing end-to-end latency.

2. **Debounce Execution Guard**
   - Prevents duplicate processing when rapid input events arrive.
   - Uses an asynchronous lock pattern to keep the ingestion worker stable under fast hotkey input.

3. **Text Overlap Deduplication**
   - Merges overlapping OCR frames using suffix/prefix intersection logic.
   - Removes duplicate lines and content noise from the assembled context window.

---

## 📈 Roadmap

- [ ] Native compiled client: migrate Device A from Python to Go for a small, zero-dependency binary.
- [ ] Multi-tenant proxy architecture: enable BYOK encryption and cloud endpoint integration.
- [ ] Clipboard automation: auto-inject generated code into the host clipboard after completion.

---

## 📌 Notes

This repository is intended for advanced experimentation with distributed local inference, vector grounding, and real-time streaming over isolated device topologies.

Use this README as the primary reference for the project architecture and key optimizations.
