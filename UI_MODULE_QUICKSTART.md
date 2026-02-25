# UI Module - Quick Reference Guide

## 🚀 Installation & Setup

```powershell
# Install UI dependencies
pip install -r requirements_ui.txt

# Verify installation
python -c "from ui_module import interface; print('✅ Ready!')"
```

## 🎮 Running Demos

### 1. Automated Demo (Mock Mode - No AI Needed)
```powershell
python demo_ui_module.py
```
Shows all features automatically in sequence.

### 2. Interactive Demo
```powershell
python demo_interactive.py
```
Manual testing - type commands to test features.

### 3. Integration Demo (Mock Mode)
```powershell
python demo_integration.py
```
Simulates keyboard layer + UI + AI integration.

### 4. Integration with Real AI
```powershell
# Terminal 1: Start AI engine
uvicorn ai_engine.api_service:app --reload

# Terminal 2: Run integration with real AI
python demo_integration.py --real-ai
```

## 📡 Public API - Quick Reference

```python
from ui_module import interface

# Initialize (do once)
ui = interface.initialize(mock_mode=True)  # False = real AI
ui.show()

# Display AI suggestion
interface.display_suggestion({
    "api_version": "v1",
    "result_text": "suggested text",
    "confidence": 0.92,
    "intent": "autocomplete",
    "status": "success"
})

# Accept suggestion (Tab key)
accepted = interface.accept_suggestion()

# Reject suggestion (Esc key)
interface.reject_suggestion()

# Voice input
interface.capture_voice_and_refine(
    current_text="text to refine",
    on_complete=lambda result: print(result)
)

# Request AI suggestion (convenience)
response = interface.request_ai_suggestion(
    text="I would like to",
    action="autocomplete",  # or: rewrite, formalize, expand, summarize
    app="email"
)

# Run event loop
ui.run()
```

## 🔧 Configuration

```powershell
# Use real AI instead of mock
$env:UI_MOCK_MODE="False"

# Change AI endpoint
$env:AI_ENGINE_URL="http://localhost:8000/process_text"

# Adjust overlay opacity
$env:OVERLAY_OPACITY="0.95"
```

## 🎯 Integration Points

### Keyboard Layer Calls:
- `interface.request_ai_suggestion()` when user types
- `interface.accept_suggestion()` when Tab pressed
- `interface.reject_suggestion()` when Esc pressed
- `interface.capture_voice_and_refine()` when Ctrl+Shift+V pressed

### AI Engine Provides:
```json
{
  "api_version": "v1",
  "result_text": "AI generated text",
  "confidence": 0.92,
  "intent": "autocomplete",
  "status": "success"
}
```

## 🐛 Troubleshooting

**PyQt5 not found:**
```powershell
pip install PyQt5
```

**pyaudio installation fails:**
```powershell
pip install pipwin
pipwin install pyaudio
```

**UI window not showing:**
- Make sure to call `ui.show()` and `ui.run()`

**AI connection error:**
- Check AI engine is running: `uvicorn ai_engine.api_service:app --reload`
- Or use mock mode: `interface.initialize(mock_mode=True)`

## 📁 File Structure

```
ui_module/
├── interface.py         ← Main public API (start here!)
├── ghost_overlay.py     ← Ghost text window
├── voice_input.py       ← Voice capture
├── ai_integration.py    ← AI communication
└── config.py           ← Configuration

Demos:
├── demo_ui_module.py      ← Automated demo
├── demo_interactive.py    ← Interactive testing
└── demo_integration.py    ← Full integration demo
```

## ✅ Success Checklist

- [x] Ghost text displays correctly
- [x] Tab accepts, Esc rejects
- [x] Voice input works (mock or real)
- [x] Confidence indicators show
- [x] Integrates with AI engine
- [x] Mock mode works without AI
- [x] No focus stealing
- [x] Always-on-top overlay

---

**Need help?** Check the full [README](ui_module/README.md) for detailed documentation.
