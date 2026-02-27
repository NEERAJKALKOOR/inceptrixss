# Unified AI Keyboard - Complete System Guide

## 🎯 What This System Does

This is the **complete implementation** that satisfies all three objectives:

1. **Text Selection → AI → Replace (Ctrl+Space)**
   - Select text in any application
   - Press `Ctrl+Space`
   - AI processes it and automatically pastes the result

2. **AI Suggestions in Bottom-Right Popup**
   - AI results appear in a popup window at the bottom-right
   - Press `Tab` to accept and paste
   - Press `Esc` to reject

3. **Voice Input → Transcribe → Paste (Ctrl+Shift+V)**
   - Press `Ctrl+Shift+V` to start recording
   - Press `Ctrl+Shift+V` again to stop
   - Transcribed text appears in popup
   - Press `Tab` to paste the transcription

---

## 🚀 Quick Start

### Option 1: Run with Start Script (Easiest)

```batch
start_unified_keyboard.bat
```

### Option 2: Run Directly

```powershell
python unified_ai_keyboard.py
```

---

## 📋 System Requirements

### Required Python Packages

```powershell
pip install pyperclip pynput PyQt5
```

### Optional (for Real Voice Recognition)

```powershell
pip install openai-whisper pyaudio
```

**Note:** Without Whisper, voice will use mock mode (for testing)

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl + Space** | Text Selection → AI → Replace |
| **Ctrl + Shift + V** | Start/Stop Voice Recording |
| **Tab** | Accept suggestion from popup |
| **Esc** | Reject suggestion from popup |
| **Ctrl + Esc** | Exit the program |

---

## 🧪 Testing the System

### Test 1: Text Selection + AI Rewrite

1. Open Notepad (or any text editor)
2. Type: `hello world`
3. Select the text
4. Press `Ctrl+Space`
5. Watch the AI rewrite and paste automatically
6. See the suggestion in the bottom-right popup

### Test 2: Voice Input (Mock Mode)

1. Make sure Notepad is open
2. Press `Ctrl+Shift+V` to start recording
3. Press `Ctrl+Shift+V` again to stop (or wait 3 seconds in mock mode)
4. See the transcribed text in the popup
5. Press `Tab` to paste it into Notepad

### Test 3: Popup Interaction

1. After any AI operation, the popup appears bottom-right
2. Press `Tab` to accept and paste
3. Or press `Esc` to reject
4. Popup auto-hides after 15 seconds

---

## ⚙️ Configuration

Edit `unified_ai_keyboard.py` to change settings:

```python
# Line 21-24
MOCK_MODE = True  # Set to False to use real AI engine
VOICE_MOCK_MODE = True  # Set to False to use real Whisper
AI_API_URL = "http://localhost:8000/process_text"
COOLDOWN_SECONDS = 1.0
```

### Using Real AI (Not Mock)

1. Start the AI engine:
   ```powershell
   uvicorn ai_engine.api_service:app --reload
   ```

2. Set `MOCK_MODE = False` in `unified_ai_keyboard.py`

3. Run the keyboard:
   ```powershell
   python unified_ai_keyboard.py
   ```

### Using Real Voice Recognition

1. Install Whisper (one-time):
   ```powershell
   pip install openai-whisper
   ```

2. Set `VOICE_MOCK_MODE = False` in `unified_ai_keyboard.py`

3. First run will download Whisper model (~140MB for base model)

---

## 🏗️ Architecture

```
unified_ai_keyboard.py (Main Controller)
├── popup_suggestion_window.py (Bottom-right popup UI)
├── pynput (Keyboard hooks + control)
├── pyperclip (Clipboard management)
├── PyQt5 (Popup window framework)
└── ui_module/voice_input.py (Voice recording + Whisper)
```

---

## 🐛 Troubleshooting

### Issue: Popup doesn't appear

**Solution:** Make sure PyQt5 is installed:
```powershell
pip install PyQt5
```

### Issue: Voice recording fails

**Solution:** 
- Check if `pyaudio` is installed
- Voice will automatically fall back to mock mode if unavailable
- For real voice, install: `pip install pyaudio openai-whisper`

### Issue: Paste doesn't work

**Solution:**
- Make sure the target app (Notepad, Word, etc.) has focus
- Try clicking into the app window first
- Some apps (like terminals) may block scripted paste

### Issue: Ctrl+Space conflicts with other software

**Solution:**
- Change the hotkey in `unified_ai_keyboard.py` (line 75-77)
- Example: Use `Ctrl+Alt+Space` instead

### Issue: AI responses are generic (mock mode)

**Solution:**
- This is expected in mock mode (for testing)
- To use real AI, start the AI engine and set `MOCK_MODE = False`

---

## 📊 Features Overview

| Feature | Status | Notes |
|---------|--------|-------|
| Text Selection → AI | ✅ Working | Auto-pastes immediately |
| Bottom-Right Popup | ✅ Working | Shows all AI suggestions |
| Tab to Accept | ✅ Working | Also pastes the text |
| Esc to Reject | ✅ Working | Closes popup |
| Voice Recording | ✅ Working | Mock and real modes |
| Voice Transcription | ✅ Working | Uses Whisper (optional) |
| Cross-App Support | ✅ Working | Works in Notepad, Word, browsers, etc. |
| Mock Mode Testing | ✅ Working | No AI/voice dependencies |

---

## 🎓 How It Works

### 1. Text Selection Flow

```
User selects text → Presses Ctrl+Space
→ Keyboard hook captures event
→ Sends Ctrl+C to copy text
→ Reads clipboard
→ Sends to AI (mock or real)
→ Shows result in popup
→ Auto-pastes with Ctrl+V
→ Restores original clipboard
```

### 2. Voice Input Flow

```
User presses Ctrl+Shift+V → Starts recording
→ Microphone captures audio
→ User presses Ctrl+Shift+V again → Stops recording
→ Whisper transcribes (or mock)
→ Shows text in popup
→ User presses Tab → Pastes transcription
```

### 3. Popup Interaction Flow

```
AI generates suggestion
→ Popup appears bottom-right
→ User sees suggestion with confidence indicator
→ Tab = Accept + Paste
→ Esc = Reject + Close
→ Auto-hides after 15 seconds
```

---

## 🔐 Privacy

- **100% Local**: All processing happens on your machine
- **No Cloud Calls**: Mock mode uses no external services
- **Optional AI**: Real AI uses local Ollama (no data sent to cloud)
- **Optional Voice**: Whisper runs locally (no audio sent to cloud)

---

## 📚 Files Created

1. **`unified_ai_keyboard.py`** - Main controller (combines all features)
2. **`popup_suggestion_window.py`** - Bottom-right popup UI
3. **`start_unified_keyboard.bat`** - Easy start script
4. **`UNIFIED_KEYBOARD_GUIDE.md`** - This guide

---

## 🎉 Next Steps

1. **Test in Mock Mode** (no dependencies)
   ```powershell
   python unified_ai_keyboard.py
   ```

2. **Add Real AI** (optional)
   - Start AI engine: `uvicorn ai_engine.api_service:app --reload`
   - Set `MOCK_MODE = False`

3. **Add Real Voice** (optional)
   - Install Whisper: `pip install openai-whisper`
   - Set `VOICE_MOCK_MODE = False`

4. **Customize**
   - Change hotkeys
   - Adjust popup position
   - Modify AI prompts

---

## 📞 Support

If something doesn't work:
1. Check the console output for errors
2. Try mock mode first (for testing)
3. Make sure all dependencies are installed
4. Test in Notepad before trying other apps

---

**You now have a complete AI keyboard system that satisfies all three objectives!** 🎊
