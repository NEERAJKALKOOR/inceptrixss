# Always-On AI Keyboard - Complete System

## 🎯 Project Overview

A **modular, privacy-first AI keyboard assistant** with three distinct components working together:

1. **AI Engine** (`ai_engine/`) - Local LLM processing ✅ COMPLETE
2. **UI Module** (`ui_module/`) - Display & interaction ✅ COMPLETE  
3. **Keyboard Layer** - OS input capture ⚠️ NOT IMPLEMENTED

This README covers the **AI Engine**. For UI Module docs, see [`ui_module/README.md`](ui_module/README.md).

## Overview

The Always-On AI Keyboard Engine is an integratable, standalone, offline-first AI module. It provides a local AI intelligence layer designed to be seamlessly integrated with customized keyboard layers and UI overlays. The core purpose of this module is to receive text alongside application contextual data and reliably process it using locally executed Large Language Models (LLMs).

This project strictly adheres to separation of concerns: the AI engine implements **no** OS-level keyboard hooks, **no** screen capture mechanisms, and **no** UI elements. It exposes a single, stable HTTP JSON API for language-agnostic interaction with any frontend client.

## Features

- **Local & Offline-First Processing:** Designed to leverage local inference engines like Ollama to guarantee data privacy and zero internet dependency.
- **Context Management:** Maintains transient, RAM-only situational context per application to provide highly relevant AI responses.
- **Intent Detection and Routing:** Intelligently maps client requests to specific rewriting strategies (e.g., rewrite, formalize, expand, summarize, autocomplete).
- **In-Memory Operation:** Ensures user data is never persisted to disk.
- **Mock Mode / Test Driven:** Built-in deterministic mock mode for robust integration testing without requiring a heavy GPU or running an LLM server.
- **Extensible Architecture:** Neatly separated layers (`context_manager`, `intent_detector`, `prompt_builder`, `llm_runner`, `api_service`).

## System Requirements

- **Python 3.9+**
- **Ollama** (if running in real LLM mode) with models such as `llama3`.

## Folder Structure

```
├── ai_engine/              ✅ AI processing (backend)
│   ├── __init__.py           # Module initialization
│   ├── api_service.py        # FastAPI endpoints and orchestration
│   ├── config.py             # Environment configurations
│   ├── context_manager.py    # RAM-only context storage per app
│   ├── intent_detector.py    # Input intent validation
│   ├── llm_runner.py         # Mock & Ollama local inference integration
│   ├── prompt_builder.py     # Context-aware prompt construction
│   └── schemas.py            # Pydantic models for stable API contracts
│
├── ui_module/              ✅ Display & interaction (frontend)
│   ├── interface.py          # Public API
│   ├── ghost_overlay.py      # Ghost text overlay window
│   ├── voice_input.py        # Voice capture
│   ├── ai_integration.py     # AI communication
│   ├── config.py             # UI configuration
│   └── README.md             # UI documentation
│
├── requirements.txt          # AI engine dependencies
├── requirements_ui.txt       # UI module dependencies
├── test_client.py            # AI engine test
├── test_all_features.py      # Comprehensive AI tests
├── demo_ui_module.py         # UI demo
├── demo_integration.py       # Full system demo
└── README.md                 # This file
```

## How to Run the Service

1. **Install Dependencies**
   Navigate to the project root and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI Server**
   Start the application using `uvicorn`:
   ```bash
   uvicorn ai_engine.api_service:app --reload
   ```
   The service will start on `http://127.0.0.1:8000`. 
   Swagger documentation will be automatically accessible at `http://127.0.0.1:8000/docs`.

## Integration Contract

### Endpoint
`POST http://localhost:8000/process_text`

### Input Payload (JSON)
The API accepts strictly formatted JSON parameters containing text inputs, desired actions, and the operating context.

```json
{
  "api_version": "v1",
  "text": "schedule a meeting",
  "app": "email",
  "action": "rewrite",
  "context": {
    "previous_text": "",
    "user_style": "formal"
  }
}
```

### Output Payload (JSON)
The API responds with the processed text synchronously. Time metrics and deterministic confidence are also provided.

```json
{
  "api_version": "v1",
  "result_text": "Please let me know your availability next week.",
  "confidence": 0.92,
  "latency_ms": 420
}
```

## How to Enable Mock Mode

The module includes a `Mock Mode` that provides deterministic responses without needing a local LLM, allowing rapid UI and client-level integration testing.

Mock mode is enabled by default via the configuration. It returns exact matches for testing intents and specific strings like "schedule a meeting" -> "Please let me know your availability next week.".

You can toggle it via Environment Variables in terminal before starting the Python service:

**Windows (PowerShell):**
```powershell
$env:MOCK_MODE="False"
$env:MOCK_MODE="False"
$env:OLLAMA_MODEL="llama3.2"
uvicorn ai_engine.api_service:app --reload
```

**Linux/macOS:**
```bash
export MOCK_MODE=False
export OLLAMA_MODEL=llama3.2
uvicorn ai_engine.api_service:app --reload
```

When `MOCK_MODE` is disabled (`False`), `llm_runner.py` will automatically attempt to connect to an active local instance of Ollama at `http://localhost:11434/api/generate`.

## API Endpoints

### 1. Process Text (Main Endpoint)
`POST /process_text`

Processes text with AI using one of 5 actions: rewrite, formalize, expand, summarize, autocomplete.

### 2. Refine Text (Iterative Refinement)
`POST /refine_text`

Allows users to refine previous AI outputs based on feedback - enabling an iterative refinement loop.

**Example:**
```json
{
  "api_version": "v1",
  "app": "email",
  "original_text": "need meeting",
  "previous_output": "We need to schedule a meeting",
  "feedback": "Make it more formal and polite"
}
```

### 3. Clear Context
`DELETE /clear_context/{app_name}`

Clears conversation history for a specific app.

### 4. Health Check
`GET /health`

Returns server health status and current mode (mock/ollama).

## Run the Example Clients

While the server is running, test different features:

**Basic Test:**
```bash
python test_client.py
```

**All 5 Prompt Templates:**
```bash
python test_all_features.py
```

**Iterative Refinement Loop:**
```bash
python test_refinement.py
```

**Autocomplete Suggestions:**
```bash
python test_autocomplete.py
```

## All Requirements Satisfied

### ✅ 1. Context Manager (RAM-only)
- Thread-safe in-memory storage in [`context_manager.py`](ai_engine/context_manager.py)
- Maintains last 5 interactions per app
- Zero disk persistence

### ✅ 2. Prompt Templates
Enhanced templates in [`prompt_builder.py`](ai_engine/prompt_builder.py) for all 5 actions:
- **Rewrite**: Improve clarity and flow
- **Formalize**: Professional tone transformation
- **Expand**: Add details and context
- **Summarize**: Extract key points
- **Autocomplete**: Intelligent continuation

### ✅ 3. Local LLM Integration
- Ollama integration in [`llm_runner.py`](ai_engine/llm_runner.py)
- Mock mode for testing without GPU
- Automatic fallback handling

### ✅ 4. Iterative Refinement Loop
- `/refine_text` endpoint for feedback-based refinement
- Uses conversation history from context manager
- Enables multi-pass improvement workflow

### ✅ 5. Latency & Model Optimization
- Dynamic model selection based on task complexity
- Reduced timeouts (15s instead of 30s)
- Token limits: 150 for autocomplete, 500 for complex tasks
- Temperature and top_p tuning for quality/speed balance
