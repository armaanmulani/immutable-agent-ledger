# Autonomous AI Agent Middleware & State Controller

A deterministic, schema-constrained Python middleware layer powered by **Gemini** that integrates with an immutable cryptographic state ledger deployed on **Google Cloud Run**.

---

## System Architecture

```text
[User Prompt]
      │
      ▼
[1. State Grounding & Context Injection] ◄── [Fetch Latest Block Hash from Ledger]
      │
      ▼
[2. Gemini Reasoning Engine] ──────────────► Strict JSON Schema (Pydantic)
      │
      ▼
[3. Tool Dispatcher & Execution] ──────────► Web Search / Calculation / System Info
      │
      ▼
[4. State Transition & Commit] ────────────► Cloud Run Ledger (/api/ledger/commit)
      │
      ▼
[5. Response Synthesis] ───────────────────► Natural Language User Output

```

---

## Key Features

* **Deterministic Action Mapping:** Enforces structured outputs via Pydantic models (`schemas.py`), completely eliminating unstructured LLM hallucinations.
* **Cryptographic Context Grounding:** Queries the ledger before every reasoning step and injects only validated block state into Gemini's system instructions to prevent context drift and history poisoning.
* **Tool Sandboxing:** Isolated execution engine (`tools.py`) with low-latency search querying and strict timeout boundaries.
* **Asynchronous State Ledger Client:** Non-blocking HTTP client (`ledger_client.py`) interfacing with the live Spring Boot Cloud Run backend for state verification and block appending.
* **Multi-Turn Interactive REPL:** Real-time conversational agent loop in `main.py` executing autonomous action loops and synthesizing output per turn.

---

## File Structure

```text
python_middleware/
├── schemas.py          # Pydantic data schemas for actions & parameters
├── tools.py            # Sandboxed tool dispatcher and execution functions
├── ledger_client.py    # Asynchronous REST client for the Cloud Run ledger
├── main.py             # REPL entry point, context injection & synthesis engine
├── requirements.txt    # Python dependencies
└── README.md           # Subsystem documentation

```

---

## Setup & Running

### 1. Prerequisites

* Python 3.10+
* Google Gemini API Key

### 2. Environment Configuration

Create a `.env` file inside `python_middleware/`:

```env
GEMINI_API_KEY=your_gemini_api_key_here

```

### 3. Install Dependencies

```bash
python -m venv .venv
# On Windows:
source .venv/Scripts/activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

```

### 4. Start the Agent REPL

```bash
python main.py

```