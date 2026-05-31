"""Local storage loader chunking educational knowledge files into embedding tensors."""
import asyncio
import sys
import os

# Append project path roots to path strings to permit runtime executing isolation bindings
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.rag.vector_store import vector_db

# Specialized baseline textbook dataset tracking absolute operational definitions
CORE_CS_DATASET = [
    # --- OPERATING SYSTEMS CORE KNOWLEDGE ---
    "Operating Systems: A Deadlock occurs when four conditions hold simultaneously: "
    "1. Mutual Exclusion (only one process can use a resource at a time), "
    "2. Hold and Wait (processes hold allocated resources while waiting for new ones), "
    "3. No Preemption (resources cannot be forcibly taken), "
    "4. Circular Wait (a closed chain of processes exists where each waits for a resource held by the next).",
    
    "Operating Systems: Virtual Memory paging algorithms include FIFO, Optimal Page Replacement (PR), "
    "and LRU (Least Recently Used). LRU replaces the page that has not been referenced for the longest period of time.",
    
    "Operating Systems: ACID properties in transaction processing stand for Atomicity (all or nothing executes), "
    "Consistency (state transitions remain legal), Isolation (concurrent executions do not interfere), "
    "and Durability (committed results survive crashes).",

    # --- COMPUTER NETWORKS CORE KNOWLEDGE ---
    "Computer Networks: The TCP 3-Way Handshake protocol requires three explicit segment steps: "
    "1. Client sends SYN (Synchronize Sequence Number packet), "
    "2. Server responds with SYN-ACK (Synchronize-Acknowledgment packet token), "
    "3. Client replies with ACK (Acknowledgment validation packet). Connection is then established.",
    
    "Computer Networks: The OSI Model contains 7 structural protocol abstraction layers: "
    "Physical, Data Link, Network (IP routing tracking), Transport (TCP/UDP multiplex lines), "
    "Session, Presentation, and Application (HTTP/FTP interface gateways).",
    
    "Computer Networks: DNS (Domain Name System) maps human-readable domain text names directly to numeric "
    "IP system routing vectors. It operates primarily over UDP protocol port 53 to optimize resolution latency bounds."
]

async def seed_knowledge_base():
    """Seeds compiled computer science data payloads into the FAISS index files layout."""
    print("[*] Launching system knowledge base automated seed pipeline...")
    if not CORE_CS_DATASET:
        print("[!] Dataset package layer empty. Terminating task execution.")
        return

    await vector_db.add_documents(CORE_CS_DATASET)
    print("[+] Core definitions processed, embedded, and locked to local storage indexes successfully.")

if __name__ == "__main__":
    # Initialize the async loop loop block execution matrix setup
    asyncio.run(seed_knowledge_base())