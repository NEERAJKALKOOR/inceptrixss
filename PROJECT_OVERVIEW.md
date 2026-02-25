# Always-On AI Keyboard - Complete System

This project implements a **modular, privacy-first AI keyboard assistant** with three distinct components:

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ALWAYS-ON AI KEYBOARD                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Role 1:    │    │   Role 2:    │    │   Role 3:    │ │
│  │  Keyboard    │───▶│  AI Engine   │───▶│  UI Module   │ │
│  │   Layer      │    │   (Local)    │    │  (Display)   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│       ▲ ▲                   ▲                     │         │
│       │ │                   │                     │         │
│       │ │                   │                     ▼         │
│       │ └───────────────────┴─────────────  User Sees      │
│       │                                      Ghost Text     │
│       └─────────────────────────────────── Tab/Esc Input   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Components

### 1. **AI Engine** (`ai_engine/`) - LOCAL INFERENCE ✅ COMPLETE
- **Purpose:** Text processing using local LLMs (Ollama)
- **Features:**
  - 5 prompt templates (rewrite, formalize, expand, summarize, autocomplete)
  - RAM-only context manager (no disk persistence)
  - Iterative refinement loop
  - Model selection optimization
  - Mock mode for testing
- **Interface:** HTTP REST API
- **Privacy:** 100% offline, no cloud calls

**Status:** ✅ Fully implemented and tested

### 2. **UI Module** (`ui_module/`) - DISPLAY & INTERACTION ✅ COMPLETE
- **Purpose:** User interaction and display ONLY
- **Features:**
  - Ghost text overlay (transparent, always-on-top)
  - Accept/Reject (Tab/Esc)
  - Push-to-talk voice input
  - Hybrid voice + text refinement
  - Confidence visualization
  - Mock mode for testing
- **Interface:** Python function calls
- **Privacy:** No keyboard hooks, no screen access

**Status:** ✅ Fully implemented with demos

### 3. **Keyboard Layer** (NOT IMPLEMENTED)
- **Purpose:** OS-level input capture and window management
- **Features:**
  - Global keyboard hooks
  - Active window detection
  - Text injection
  - Hotkey handling
- **Interface:** Calls UI Module + AI Engine
- **Privacy:** Local only, no telemetry

**Status:** ⚠️ Not implemented (out of scope for UI module task)

## 🚀 Quick Start

### Complete System Demo (Mock Mode)

```powershell
# 1. Install all dependencies
pip install -r requirements.txt
pip install -r requirements_ui.txt

# 2. Run integration demo (all components in mock mode)
python demo_integration.py
```

### Full System with Real AI

```powershell
# Terminal 1: Start AI engine
uvicorn ai_engine.api_service:app --reload

# Terminal 2: Run UI integration with real AI
python demo_integration.py --real-ai
```

### Test Individual Components

**AI Engine:**
```powershell
python test_all_features.py      # Test all 5 prompt templates
python test_refinement.py        # Test iterative refinement
```

**UI Module:**
```powershell
python demo_ui_module.py         # Automated UI demo
python demo_interactive.py       # Interactive testing
```

## 📊 Feature Matrix

| Feature | AI Engine | UI Module | Integration |
|---------|-----------|-----------|-------------|
| **Ghost Text Display** | - | ✅ | ✅ |
| **Accept/Reject (Tab/Esc)** | - | ✅ | ✅ |
| **Voice Input** | - | ✅ | ✅ |
| **Autocomplete** | ✅ | ✅ | ✅ |
| **Rewrite** | ✅ | ✅ | ✅ |
| **Formalize** | ✅ | ✅ | ✅ |
| **Expand** | ✅ | ✅ | ✅ |
| **Summarize** | ✅ | ✅ | ✅ |
| **Iterative Refinement** | ✅ | ✅ | ✅ |
| **Context Awareness** | ✅ | ✅ | ✅ |
| **Confidence Scoring** | ✅ | ✅ | ✅ |
| **Offline Mode** | ✅ | ✅ | ✅ |
| **Mock Mode** | ✅ | ✅ | ✅ |

## 🔌 Integration Examples

### Example 1: Simple Autocomplete Flow

```python
from ui_module import interface
from ai_engine.ai_integration import ai_integration

# Initialize
ui = interface.initialize(mock_mode=False)
ui.show()

# User types (would come from keyboard layer)
user_text = "I would like to"

# Get AI suggestion
ai_response = ai_integration.process_text(user_text, "autocomplete")

# Display ghost text
interface.display_suggestion(ai_response)

# User presses Tab
accepted = interface.accept_suggestion()
print(f"Insert into app: {accepted}")

ui.run()
```

### Example 2: Voice Refinement Flow

```python
# User types
current_text = "schedule meeting"

# User presses Ctrl+Shift+V and says "make it formal"
interface.capture_voice_and_refine(
    current_text=current_text,
    on_complete=lambda refined: insert_into_app(refined)
)
```

### Example 3: Iterative Refinement

```python
# First suggestion
response1 = ai_integration.process_text("need meeting", "formalize")
interface.display_suggestion(response1)

# User feedback: "make it more polite"
response2 = ai_integration.refine_with_voice(
    original_text="need meeting",
    voice_input="make it more polite",
    previous_output=response1['result_text']
)
interface.display_suggestion(response2)
```

## 🛡️ Privacy & Security

- ✅ **100% Offline**: All AI processing local (Ollama)
- ✅ **No Cloud**: Zero external API calls
- ✅ **RAM-only**: No disk persistence
- ✅ **No Telemetry**: No data collection
- ✅ **No Screen Capture**: UI module doesn't read screen
- ✅ **No Keylogging**: UI module doesn't capture keystrokes

## 📁 Project Structure

```
hackathon-inceptrix/
├── ai_engine/              ✅ AI processing (Role 2)
│   ├── api_service.py      - FastAPI endpoints
│   ├── llm_runner.py       - Ollama integration
│   ├── prompt_builder.py   - 5 prompt templates
│   ├── context_manager.py  - RAM-only context
│   └── ...
│
├── ui_module/              ✅ Display & interaction (Role 3)
│   ├── interface.py        - Public API
│   ├── ghost_overlay.py    - Ghost text window
│   ├── voice_input.py      - Voice capture
│   ├── ai_integration.py   - AI communication
│   └── README.md           - Full documentation
│
├── demo_integration.py     ✅ Full system demo
├── demo_ui_module.py       ✅ UI-only demo
├── demo_interactive.py     ✅ Interactive testing
│
├── test_all_features.py    ✅ AI engine tests
├── test_refinement.py      ✅ Refinement tests
├── test_autocomplete.py    ✅ Autocomplete tests
│
├── requirements.txt        - AI engine deps
├── requirements_ui.txt     - UI module deps
└── README.md              - This file
```

## 🎯 Task Completion Status

### ✅ AI Engine (Role 2) - COMPLETE
- [x] Context manager (RAM-only)
- [x] 5 prompt templates
- [x] Local LLM integration (Ollama)
- [x] Iterative refinement loop
- [x] Latency optimization
- [x] Mock mode
- [x] Full test suite

### ✅ UI Module (Role 3) - COMPLETE
- [x] Ghost text overlay
- [x] Accept/Reject (Tab/Esc)
- [x] Voice input (push-to-talk)
- [x] Hybrid voice + text refinement
- [x] Confidence visualization
- [x] Clean public API
- [x] Mock mode
- [x] Integration demos
- [x] Full documentation

### ⚠️ Keyboard Layer (Role 1) - NOT IMPLEMENTED
- [ ] OS keyboard hooks
- [ ] Active window detection
- [ ] Text injection
- [ ] Hotkey handling
- **Note:** Out of scope for current task (UI module only)

## 📚 Documentation

- **AI Engine:** See [readme.md](readme.md) and [REQUIREMENTS_CHECKLIST.md](REQUIREMENTS_CHECKLIST.md)
- **UI Module:** See [ui_module/README.md](ui_module/README.md) and [UI_MODULE_QUICKSTART.md](UI_MODULE_QUICKSTART.md)
- **Integration:** See [demo_integration.py](demo_integration.py)

## 🧪 Testing

### Run All Tests

```powershell
# AI Engine tests
python test_all_features.py
python test_refinement.py

# UI Module tests
python demo_ui_module.py
python demo_interactive.py

# Integration test
python demo_integration.py
```

### Test with Real AI

```powershell
# Start AI engine
uvicorn ai_engine.api_service:app --reload

# Run integration
python demo_integration.py --real-ai
```

## 🔧 Configuration

### AI Engine
```powershell
$env:MOCK_MODE="False"              # Use real Ollama
$env:OLLAMA_MODEL="llama3.2"        # Model to use
```

### UI Module
```powershell
$env:UI_MOCK_MODE="False"           # Use real AI
$env:AI_ENGINE_URL="http://localhost:8000/process_text"
$env:OVERLAY_OPACITY="0.95"
$env:VOICE_ENABLED="True"
```

## 🎓 For Hackathon Judges

### What This Demonstrates

1. **Clean Architecture**: Three distinct roles with clear boundaries
2. **Privacy-First**: 100% offline, local processing
3. **Modular Design**: Swap components without breaking system
4. **Rich Interaction**: Ghost text, voice, iterative refinement
5. **Production-Ready**: Mock modes, error handling, documentation

### How to Evaluate

1. **Run Demos:**
   ```powershell
   python demo_integration.py
   ```

2. **Test Features:**
   - Ghost text appears as you "type"
   - Tab accepts suggestions
   - Esc rejects
   - Voice input refines text
   - Confidence indicators work

3. **Check Integration:**
   - UI works independently
   - AI works independently
   - They integrate cleanly via HTTP + function calls

4. **Verify Privacy:**
   - All code local
   - No external API calls (in offline mode)
   - RAM-only storage

## 🏆 Success Criteria

✅ **AI Engine:**
- [x] Context manager (RAM-only)
- [x] 5 prompt templates
- [x] Local LLM integration
- [x] Iterative refinement
- [x] Latency optimization

✅ **UI Module:**
- [x] Ghost text system
- [x] Accept/reject seamless
- [x] Voice input
- [x] Hybrid refinement
- [x] Clean boundaries
- [x] Modular design

✅ **System Integration:**
- [x] Components work independently
- [x] Clean interfaces
- [x] Easy to swap components
- [x] Demo-ready

## 🚀 Next Steps (Future Work)

1. **Keyboard Layer Implementation:**
   - Global keyboard hooks (pynput/keyboard)
   - Active window detection
   - Text injection

2. **Enhanced Features:**
   - Multi-language support
   - Custom prompt templates
   - User preferences

3. **Performance:**
   - Caching
   - Streaming responses
   - GPU optimization

---

**Built for Hackathon Inceptrix 2026** 🎯

**Team:** Neeraj & AI Assistant  
**Date:** February 25, 2026  
**Status:** UI Module & AI Engine Complete ✅
