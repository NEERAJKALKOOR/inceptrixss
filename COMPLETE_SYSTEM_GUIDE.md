# 🚀 AI Keyboard - Complete System Documentation

## Architecture Overview

The AI Keyboard is built with a **three-role modular architecture**:

### **Role 1: Keyboard Layer** (NEW ✨)
**Location:** `keyboard_layer/`
- **Purpose:** OS-level keyboard integration
- **Components:**
  - `keyboard_hook.py`: Global hotkey detection, keystroke capture
  - `text_manager.py`: Active window detection, text insertion/replacement
  - `integration.py`: Main service coordinator
  - `config.py`: Hotkey and behavior configuration

### **Role 2: AI Engine** (Existing)
**Location:** `ai_engine/`
- **Purpose:** Text processing and AI suggestions
- **Components:**
  - `api_service.py`: FastAPI REST server
  - `llm_runner.py`: Ollama integration
  - `prompt_builder.py`: 5 optimized prompt templates
  - `context_manager.py`: Conversation history

### **Role 3: UI Module** (Existing)
**Location:** `ui_module/`
- **Purpose:** User interface and interaction
- **Components:**
  - `ghost_overlay.py`: Transparent ghost text display
  - `voice_input.py`: Whisper voice transcription
  - `ai_integration.py`: HTTP client for AI engine
  - `interface.py`: Public API

---

## Installation

### 1. Install All Dependencies

```powershell
# Core AI Engine
pip install -r requirements.txt

# UI Module (PyQt5, Whisper)
pip install -r requirements_ui.txt

# Keyboard Layer (pynput, pyautogui)
pip install -r requirements_keyboard.txt
```

### 2. Install ffmpeg (for Whisper)
Already installed via winget. Verify:
```powershell
ffmpeg -version
```

### 3. Start Ollama (for AI)
```powershell
ollama serve
# In another terminal:
ollama run llama3.2
```

---

## Usage

### **Option 1: Quick Start (Recommended)**

```powershell
.\start_ai_keyboard.bat
```

This automatically:
1. Starts AI engine server
2. Launches keyboard service
3. Initializes UI overlay

### **Option 2: Manual Start**

**Terminal 1 - AI Engine:**
```powershell
uvicorn ai_engine.api_service:app --reload
```

**Terminal 2 - Keyboard Service:**
```powershell
python run_ai_keyboard.py
```

Choose mode:
- **1 = FULL MODE** - Real AI + Whisper voice
- **2 = MOCK MODE** - Testing without AI server

---

## Hotkeys

| Hotkey | Action |
|--------|--------|
| **Ctrl+Space** | Request AI suggestion for current text |
| **Ctrl+Shift+V** | Voice input (push-to-talk) |
| **Tab** | Accept ghost text suggestion |
| **Esc** | Reject ghost text suggestion |

### Auto-Trigger
- AI automatically suggests completions after 0.5s of typing pause
- Only triggers in text editors/apps (configurable)

---

## Features

### 1. **Real-Time Autocomplete**
- Type anywhere → AI suggests completions
- Ghost text appears inline with confidence %
- Tab to accept, Esc to reject

### 2. **Voice Refinement**
- Press Ctrl+Shift+V, speak your refinement
- Whisper transcribes (99+ languages, offline)
- AI refines your text based on voice input

### 3. **Context-Aware**
- Detects active application
- Uses conversation history for better suggestions
- 5 prompt templates: autocomplete, formalize, expand, summarize, rewrite

### 4. **Privacy-First**
- 100% offline capable (Ollama + Whisper)
- No data leaves your machine
- RAM-only context storage

### 5. **Cross-App Support**
- Works in: VS Code, Notepad, Word, Excel, Chrome, Slack, Discord, etc.
- Automatic app detection
- Seamless text insertion

---

## Configuration

### Keyboard Layer Settings
**File:** `keyboard_layer/config.py`

```python
# Change hotkeys
ACTION_KEY = "ctrl+space"  # AI trigger
VOICE_KEY = "ctrl+shift+v"  # Voice input

# Auto-trigger behavior
MIN_TEXT_LENGTH = 3  # Min chars before AI
DEBOUNCE_TIME = 0.5  # Wait time (seconds)

# Debug mode
DEBUG_MODE = True  # Enable logging
```

### UI Module Settings  
**File:** `ui_module/config.py`

```python
# Ghost text appearance
OVERLAY_OPACITY = 0.8
FONT_SIZE = 12

# Voice model
WHISPER_MODEL = "base"  # tiny/base/small/medium
```

### AI Engine Settings
**File:** `ai_engine/config.py`

```python
# LLM configuration
MOCK_MODE = "False"  # Use real AI
OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434"
```

---

## Testing

### Test Individual Components

**1. Test Keyboard Hook:**
```powershell
python test_keyboard_layer.py
```
- Type text, press hotkeys
- Verify detection

**2. Test Voice (Whisper):**
```powershell
python test_voice_whisper.py
```
- Record voice, check transcription

**3. Test UI Module:**
```powershell
python demo_ui_module.py
```
- See ghost text, Tab/Esc handling

**4. Test Integration:**
```powershell
python demo_integration.py
```
- Full system simulation

---

## Troubleshooting

### AI Engine Won't Start
```powershell
# Check Ollama is running
ollama list

# Start Ollama
ollama serve
```

### No Ghost Text Appearing
- Check UI module initialized: Look for "✅ UI Module initialized"
- Verify PyQt5 installed: `python -c "import PyQt5"`

### Voice Not Working
- Verify Whisper: `python -c "import whisper; print('OK')"`
- Check ffmpeg: `ffmpeg -version`
- Test microphone: Check Windows sound settings

### Hotkeys Not Detected
- Run as administrator (may be required for some apps)
- Check `keyboard_layer/config.py` for hotkey conflicts
- Enable debug: `set KEYBOARD_DEBUG=true`

### Text Insertion Fails
- Some apps block automation (security)
- Try different insertion method in `text_manager.py`
- Check pyautogui/pyperclip installed

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USER TYPES IN ANY APP                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  ROLE 1: KEYBOARD LAYER (keyboard_layer/)                  │
│  ├─ keyboard_hook.py    → Captures keystrokes              │
│  ├─ text_manager.py     → Detects app, inserts text        │
│  └─ integration.py      → Coordinates all roles            │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  ROLE 3: UI MODULE (ui_module/)                            │
│  ├─ ghost_overlay.py    → Shows transparent suggestions    │
│  ├─ voice_input.py      → Whisper voice transcription      │
│  └─ interface.py        → Public API                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  ROLE 2: AI ENGINE (ai_engine/)                            │
│  ├─ api_service.py      → FastAPI REST server              │
│  ├─ llm_runner.py       → Ollama LLM integration           │
│  ├─ prompt_builder.py   → 5 optimized templates            │
│  └─ context_manager.py  → Conversation history             │
└─────────────────────────────────────────────────────────────┘
```

---

## Files Created

### Keyboard Layer (NEW)
- `keyboard_layer/__init__.py`
- `keyboard_layer/config.py`
- `keyboard_layer/keyboard_hook.py` (200 lines)
- `keyboard_layer/text_manager.py` (150 lines)
- `keyboard_layer/integration.py` (300 lines)

### Main Entry Points
- `run_ai_keyboard.py` - Main service launcher
- `start_ai_keyboard.bat` - Quick start script
- `test_keyboard_layer.py` - Component testing

### Dependencies
- `requirements_keyboard.txt` - Keyboard layer deps

---

## Production Deployment

### Run as Windows Service (Future)
```powershell
# Install as service
python run_ai_keyboard.py --install-service

# Start service
net start AIKeyboard
```

### Auto-Start on Boot
1. Press `Win+R`, type `shell:startup`
2. Create shortcut to `start_ai_keyboard.bat`
3. Reboot to test

---

## Security & Privacy

✅ **Offline-First:** All processing happens locally
✅ **No Telemetry:** Zero data collection
✅ **RAM-Only Context:** No persistent storage of typed text
✅ **Open Source:** Full code transparency
✅ **Configurable:** Disable features as needed

---

## Performance

- **Latency:** ~200ms AI response (depends on Ollama model)
- **Memory:** ~500MB (base Whisper + Ollama)
- **CPU:** Minimal when idle, spikes during AI calls
- **Background:** Non-blocking, doesn't interfere with typing

---

## Next Steps

1. ✅ **Test the system:** `python run_ai_keyboard.py`
2. ⚙️ **Customize hotkeys:** Edit `keyboard_layer/config.py`
3. 🎨 **Adjust ghost text:** Edit `ui_module/config.py`
4. 🤖 **Change AI model:** Edit `ai_engine/config.py`
5. 🚀 **Deploy:** Set up auto-start

---

## Support

**Issues:**
- Keyboard not detecting: Check admin privileges
- AI not responding: Verify Ollama running
- Voice fails: Install/check ffmpeg

**Debug Mode:**
```powershell
set KEYBOARD_DEBUG=true
python run_ai_keyboard.py
```

---

**🎉 Your AI-powered keyboard is ready! Happy typing!**
