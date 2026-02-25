# UI Module - Always-On AI Keyboard

**Standalone UI & Interaction Module for Always-On AI Keyboard Project**

This module handles **user interaction and display only**. It does NOT implement keyboard hooks, screen capture, or AI logic. It integrates cleanly with:
- Keyboard layer (Role 1) via function calls
- AI engine (Role 2) via HTTP API

---

## 🎯 Features

### ✅ Ghost Text Suggestion System
- Display AI suggestions as **light-gray inline text**
- **Tab** to accept, **Esc** to reject
- Visual confidence indicators (🟢 High, 🟡 Medium, 🔴 Low)

### ✅ Transparent Overlay UI
- Always-on-top, non-intrusive window
- Does NOT steal focus or intercept typing
- Transparent background with rounded borders

### ✅ Push-to-Talk Voice Input
- Capture microphone input (Ctrl+Shift+V)
- Offline speech-to-text (using SpeechRecognition)
- Voice commands refine existing text

### ✅ Hybrid Voice + Text Refinement
- Voice modifies typed content
- Returns updated ghost text suggestions

### ✅ Clean Integration
- Function-based public API
- HTTP communication with AI engine
- Mock mode for testing without AI

---

## 📦 Installation

### 1. Install Dependencies

```powershell
pip install PyQt5 pyaudio SpeechRecognition
```

**Optional (for offline speech recognition):**
```powershell
pip install pocketsphinx
```

### 2. Verify Installation

```powershell
python -c "from ui_module import interface; print('✅ UI Module ready!')"
```

---

## 🚀 Quick Start

### Run Automated Demo (Mock Mode)

```powershell
python demo_ui_module.py
```

This demonstrates:
- Ghost text autocomplete
- Text refinement (rewrite, formalize, expand, summarize)
- Voice input simulation
- Confidence level visualization

### Run Interactive Demo

```powershell
python demo_interactive.py
```

Manual testing interface - type commands to test features.

---

## 🔌 Integration Guide

### For Keyboard Layer (Role 1)

The keyboard layer should call these functions when user types:

```python
from ui_module import interface

# 1. Initialize UI module (once at startup)
controller = interface.initialize(mock_mode=False)  # False = use real AI

# 2. When user types text, request AI suggestion
response = interface.request_ai_suggestion(
    text="I would like to",
    action="autocomplete",  # or: rewrite, formalize, expand, summarize
    app="email",
    context={"user_style": "professional"}
)
# Ghost text automatically displayed!

# 3. When user presses Tab
accepted_text = interface.accept_suggestion()
# Insert accepted_text into the application

# 4. When user presses Esc or types
interface.reject_suggestion()

# 5. For voice input (when user presses Ctrl+Shift+V)
interface.capture_voice_and_refine(
    current_text="schedule meeting",
    on_complete=lambda refined: print(f"Refined: {refined}")
)
```

### For AI Engine (Role 2)

The AI engine should send responses in this exact format:

```python
{
    "api_version": "v1",
    "result_text": "Please let me know your availability next week.",
    "confidence": 0.92,
    "intent": "rewrite",
    "status": "success"
}
```

The UI module will automatically display this as ghost text.

**External AI Engine Integration:**

```python
from ui_module import interface

# AI engine sends response directly
ai_response = {
    "api_version": "v1",
    "result_text": "Suggested completion...",
    "confidence": 0.88,
    "intent": "autocomplete",
    "status": "success"
}

interface.display_suggestion(ai_response)
```

---

## 📡 Public Interface (API)

### Core Functions

```python
# Initialize UI module
controller = interface.initialize(mock_mode: bool = True) -> UIController

# Display AI suggestion
interface.display_suggestion(ai_response: dict)

# Accept suggestion (returns accepted text)
interface.accept_suggestion() -> str | None

# Reject suggestion
interface.reject_suggestion()

# Voice input + refinement
interface.capture_voice_and_refine(
    current_text: str = "",
    on_complete: Callable[[str], None] = None
)

# Request AI suggestion (convenience method)
interface.request_ai_suggestion(
    text: str,
    action: str = "autocomplete",
    app: str = "general",
    context: dict = None
) -> dict
```

### Signals (for event-driven integration)

```python
controller = interface.get_controller()

# Connect to signals
controller.suggestion_accepted.connect(lambda text: print(f"Accepted: {text}"))
controller.suggestion_rejected.connect(lambda: print("Rejected"))
controller.voice_captured.connect(lambda text: print(f"Voice: {text}"))
```

---

## ⚙️ Configuration

Environment variables (optional):

```powershell
# UI Settings
$env:OVERLAY_OPACITY="0.95"        # Window transparency (0.0 - 1.0)
$env:UI_MOCK_MODE="False"          # Use real AI engine

# AI Engine
$env:AI_ENGINE_URL="http://localhost:8000/process_text"

# Voice
$env:VOICE_ENABLED="True"
$env:PUSH_TO_TALK_KEY="ctrl+shift+v"
```

Or configure in `ui_module/config.py`:

```python
MOCK_MODE = False  # Switch to real AI
AI_ENGINE_URL = "http://localhost:8000/process_text"
```

---

## 🔄 Switching from Mock to Real AI

### Option 1: Environment Variable

```powershell
$env:UI_MOCK_MODE="False"
python demo_ui_module.py
```

### Option 2: Code

```python
controller = interface.initialize(mock_mode=False)
```

### Option 3: Config File

Edit `ui_module/config.py`:
```python
MOCK_MODE = False
```

**Make sure the AI engine is running:**
```powershell
uvicorn ai_engine.api_service:app --reload
```

---

## 🏗️ Architecture

```
ui_module/
├── __init__.py              # Module initialization
├── config.py                # Configuration settings
├── interface.py             # Public API (main entry point)
├── ghost_overlay.py         # Ghost text overlay window
├── voice_input.py           # Voice capture & speech-to-text
└── ai_integration.py        # AI engine communication

Integration Points:
├── Keyboard Layer → interface.py (function calls)
└── AI Engine → HTTP API (JSON responses)
```

---

## 📋 Module Boundaries (What This Module Does NOT Do)

❌ **NO** keyboard hooks or OS-level input capture  
❌ **NO** screen reading or OCR  
❌ **NO** AI inference or LLM logic  
❌ **NO** direct window manipulation of other apps  

✅ **ONLY** displays AI responses  
✅ **ONLY** handles user interaction (accept/reject)  
✅ **ONLY** captures voice input  
✅ **ONLY** communicates via function calls or HTTP  

---

## 🧪 Testing

### Test Ghost Text Display

```python
from ui_module import interface

controller = interface.initialize(mock_mode=True)
controller.show()

# Show ghost suggestion
interface.request_ai_suggestion("I would like to", "autocomplete")

# Accept it
accepted = interface.accept_suggestion()
print(f"Accepted: {accepted}")

controller.run()
```

### Test Voice Input

```python
interface.capture_voice_and_refine(
    current_text="schedule meeting",
    on_complete=lambda result: print(f"Refined: {result}")
)
```

### Test with Real AI Engine

1. Start AI engine: `uvicorn ai_engine.api_service:app --reload`
2. Set mock mode to False
3. Run demo: `python demo_ui_module.py`

---

## 🎨 Customization

### Change Ghost Text Color

Edit `ui_module/config.py`:
```python
GHOST_TEXT_COLOR = "#999999"  # Medium gray
```

### Adjust Confidence Thresholds

```python
HIGH_CONFIDENCE = 0.90   # Green indicator
MEDIUM_CONFIDENCE = 0.75  # Yellow indicator
# Below 0.75 = Red indicator
```

### Customize Overlay Position

Edit `ui_module/ghost_overlay.py`:
```python
self.setGeometry(100, 100, 600, 100)  # (x, y, width, height)
```

---

## 🔧 Troubleshooting

### "PyQt5 not found"
```powershell
pip install PyQt5
```

### "pyaudio not found"
```powershell
pip install pyaudio
```

If pyaudio installation fails on Windows:
```powershell
pip install pipwin
pipwin install pyaudio
```

### "Speech recognition not working"

For **offline** mode:
```powershell
pip install pocketsphinx
```

For **online** mode (requires internet):
- Already works with default SpeechRecognition

### "UI window not showing"

Make sure to call:
```python
controller.show()
controller.run()  # Starts event loop
```

---

## 📊 Success Criteria

✅ **UI can run independently** - Yes (demo_ui_module.py)  
✅ **AI responses displayed without modification** - Yes (standard JSON format)  
✅ **Accept/reject works seamlessly** - Yes (Tab/Esc)  
✅ **Voice input refines existing text** - Yes (hybrid voice+text)  
✅ **Swapping AI engines doesn't break UI** - Yes (HTTP interface)  

---

## 🎯 Integration Examples

### Example 1: Simple Autocomplete

```python
from ui_module import interface

# Initialize
ui = interface.initialize(mock_mode=False)
ui.show()

# User types "I would like to"
response = interface.request_ai_suggestion("I would like to", "autocomplete")

# Ghost text appears
# User presses Tab
accepted = interface.accept_suggestion()

# Insert accepted text into app
print(f"Insert: {accepted}")

ui.run()
```

### Example 2: Voice Refinement

```python
# User types
current = "schedule meeting"

# User presses Ctrl+Shift+V and says "make it formal"
interface.capture_voice_and_refine(
    current_text=current,
    on_complete=lambda refined: insert_text(refined)
)
```

### Example 3: External AI Integration

```python
# Your custom AI engine
def my_ai_engine(text):
    result = my_model.generate(text)
    return {
        "api_version": "v1",
        "result_text": result,
        "confidence": 0.9,
        "intent": "autocomplete",
        "status": "success"
    }

# Display in UI
ai_response = my_ai_engine("Hello")
interface.display_suggestion(ai_response)
```

---

## 📝 License

Part of the Always-On AI Keyboard project for Hackathon Inceptrix.

---

## 🤝 Contributing

This module is designed for **clean separation of concerns**:
- Keep keyboard logic separate
- Keep AI logic separate
- This module = display + interaction only

---

## 📞 Support

Issues? Check:
1. Dependencies installed (`pip install -r requirements_ui.txt`)
2. AI engine running (`uvicorn ai_engine.api_service:app --reload`)
3. Mock mode enabled for testing (`UI_MOCK_MODE=True`)

---

**Built for Hackathon Inceptrix 2026** 🚀
