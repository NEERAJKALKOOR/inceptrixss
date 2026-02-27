# 🚀 Cross-Application AI Text Rewriter

**A universal AI text improvement system that works in ANY application using standard copy-paste shortcuts.**

No caret tracking. No DOM manipulation. No app-specific APIs.  
Just pure keyboard shortcuts — like a real user.

---

## 🎯 What It Does

1. **Select text** in any application (browser, Word, Notepad, VS Code, chat boxes, etc.)
2. **Press `Ctrl + Space`**
3. **AI improves the text** and pastes it back automatically
4. **Your original clipboard is restored**

---

## ✨ Key Features

✅ **Universal**: Works in any app that supports Ctrl+C / Ctrl+V  
✅ **Non-invasive**: No window tracking, no caret position logic  
✅ **Clipboard-safe**: Automatically restores your original clipboard  
✅ **Zero configuration**: Works out-of-the-box in MOCK mode  
✅ **AI-powered**: Improves text quality, formality, and clarity  

---

## 🏗️ Architecture

```
User selects text
       ↓
   Ctrl+Space pressed
       ↓
System saves clipboard
       ↓
System simulates Ctrl+C → reads copied text
       ↓
Text sent to AI engine
       ↓
AI returns improved text
       ↓
System copies AI text → simulates Ctrl+V
       ↓
Original clipboard restored
```

**NO tracking of:**
- ❌ Caret position
- ❌ Window handles
- ❌ Application internals
- ❌ DOM elements

**ONLY uses:**
- ✅ Standard keyboard shortcuts (Ctrl+C, Ctrl+V)
- ✅ Clipboard API
- ✅ Global hotkey listener

---

## 🚀 Quick Start

### Option 1: Double-click the batch file (Easiest)

```batch
start_cross_app_ai.bat
```

This will:
- Install all dependencies automatically
- Launch the system
- Show instructions

### Option 2: Manual start

```bash
# Install dependencies
pip install -r requirements_cross_app.txt

# Run the system
python cross_app_ai_rewrite.py
```

---

## 📋 Requirements

- **Python 3.8+**
- **Windows** (tested on Windows 10/11)
- Dependencies (auto-installed):
  - `pyperclip` - clipboard management
  - `pynput` - global hotkey detection
  - `pyautogui` - keyboard simulation
  - `requests` - AI API calls

---

## 🎮 Usage

### Basic Flow

1. **Start the system**:
   ```bash
   python cross_app_ai_rewrite.py
   ```

2. **Open any application** (e.g., Chrome, Word, Notepad++)

3. **Type or select some text**:
   ```
   schedule a meeting
   ```

4. **Press `Ctrl + Space`**

5. **Watch it transform**:
   ```
   Please let me know your availability next week.
   ```

### Testing in Different Apps

#### Browser (Chrome/Edge/Firefox)
1. Open a textarea (e.g., Gmail compose)
2. Type: `need help with project`
3. Select the text
4. Press `Ctrl + Space`
5. Text is replaced with AI improvement

#### Microsoft Word
1. Open Word document
2. Type: `meeting tomorrow`
3. Select text
4. Press `Ctrl + Space`
5. Text is professionally rewritten

#### VS Code
1. Open any file
2. Type: `fix the bug`
3. Select text
4. Press `Ctrl + Space`
5. AI suggests improvement

#### Notepad
1. Open Notepad
2. Type anything
3. Select and press `Ctrl + Space`
4. Watch magic happen

---

## ⚙️ Configuration

### Mock Mode (Default)

By default, the system runs in **MOCK mode** — no backend required!

```python
MOCK_MODE = True
```

Mock responses are built-in for testing.

### Live AI Mode

To use the real AI backend:

1. Set `MOCK_MODE = False` in `cross_app_ai_rewrite.py`
2. Start the AI service:
   ```bash
   python -m uvicorn ai_engine.api_service:app --reload
   ```
3. Ensure Ollama is running (optional, depends on config)

---

## 🧪 Edge Cases Handled

### ✅ No Text Selected
If you press `Ctrl + Space` without selecting text:
- AI generates fresh contextual text
- Inserts at cursor position

### ✅ Clipboard Preserved
Original clipboard is always restored after operation.

### ✅ Empty Clipboard
If clipboard is empty, system handles gracefully.

### ✅ Timing Safety
- 150ms delay after Ctrl+C before reading clipboard
- 50ms delay before Ctrl+V
- Ensures reliable cross-app operation

---

## 🔧 Troubleshooting

### Issue: Nothing happens when I press Ctrl+Space

**Solution:**
- Make sure the Python script is running
- Check terminal for "Listening for Ctrl+Space..." message
- Try pressing keys slower (Ctrl first, then Space)

### Issue: Text doesn't paste correctly

**Solution:**
- Increase `COPY_DELAY` in the script (line 17):
  ```python
  COPY_DELAY = 0.2  # Increase to 200ms
  ```
- Ensure the target app has focus

### Issue: Original clipboard not restored

**Solution:**
- Wait 1-2 seconds after paste
- System restores clipboard after a small delay

---

## 🎯 Success Criteria (All Met ✅)

| Criterion | Status |
|-----------|--------|
| Works in browser | ✅ |
| Works in Word | ✅ |
| Works in VS Code | ✅ |
| Works in Notepad | ✅ |
| No caret position logic | ✅ |
| Clipboard restored safely | ✅ |
| Text inserted at correct location | ✅ |
| Reliable demo behavior | ✅ |

---

## 📝 Example Test Cases

### Test 1: Email Writing
```
Input:  "schedule a meeting"
Output: "Please let me know your availability next week."
```

### Test 2: Short Text Enhancement
```
Input:  "thanks"
Output: "Thanks - enhanced by AI"
```

### Test 3: No Selection
```
Input:  [no text selected]
Output: "Please let me know how I can assist you."
```

---

## 🔐 Security & Privacy

- ✅ All processing is local (in MOCK mode)
- ✅ No data sent to external servers (when MOCK_MODE=True)
- ✅ Clipboard content is temporary
- ✅ No logging of sensitive data

---

## 🛠️ Technical Implementation

### Core Components

1. **Hotkey Listener** (`pynput`)
   - Detects global `Ctrl + Space` combination
   - Non-blocking keyboard monitoring

2. **Clipboard Manager** (`pyperclip`)
   - Saves original clipboard
   - Copies AI output
   - Restores clipboard

3. **Keyboard Simulator** (`pyautogui`)
   - Simulates `Ctrl+C` to copy selected text
   - Simulates `Ctrl+V` to paste AI result

4. **AI Integration**
   - Mock mode for standalone testing
   - REST API mode for backend integration

### Timing Diagram

```
t=0ms:    Save clipboard, clear it
t=50ms:   Simulate Ctrl+C
t=200ms:  Read clipboard (COPY_DELAY)
t=250ms:  Send to AI
t=450ms:  Receive AI response
t=500ms:  Copy AI to clipboard
t=550ms:  Simulate Ctrl+V (PASTE_DELAY)
t=650ms:  Restore original clipboard
```

---

## 🚦 Exit Instructions

**To stop the system:**
- Press `Ctrl + Esc` in the terminal
- Or close the terminal window

---

## 📦 Files in This System

```
cross_app_ai_rewrite.py          # Main system script
requirements_cross_app.txt       # Python dependencies
start_cross_app_ai.bat          # Windows launcher
CROSS_APP_AI_README.md          # This file
```

---

## 🎓 Learning Points

### Why This Approach Works

1. **Universal Compatibility**
   - Every app understands Ctrl+C and Ctrl+V
   - No need for app-specific integrations

2. **Simplicity**
   - Just simulates what a user would do manually
   - No complex window tracking

3. **Reliability**
   - Standard keyboard shortcuts are battle-tested
   - Works consistently across Windows

### What We Explicitly Avoid

- ❌ **Window Handle Tracking**: Unreliable, breaks easily
- ❌ **Caret Position APIs**: Not available in most apps
- ❌ **DOM Manipulation**: Browser-specific, won't work in Word
- ❌ **Chrome Extensions**: Doesn't work outside browser
- ❌ **Accessibility APIs**: Overcomplicated, not universal

---

## 🎉 Success!

**You now have a universal AI text improvement system that works in ANY application!**

Just press `Ctrl + Space` and watch your text improve. ✨

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Ensure all dependencies are installed
3. Try MOCK mode first to verify functionality

---

## 📄 License

This system is part of the AI Keyboard project.

---

**One-Line Summary:**  
*"The system injects AI-generated text across applications by simulating standard copy-paste shortcuts, relying on each application's native input handling."*
