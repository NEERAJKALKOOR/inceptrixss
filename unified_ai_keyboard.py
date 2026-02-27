"""
Unified AI Keyboard - Complete System
Combines all three objectives:
1. Text selection → AI → Replace (Ctrl+Space)
2. AI suggestions in bottom-right popup with Tab to accept
3. Voice recording → Transcribe → Tab to paste (Ctrl+Shift+V)
"""

import sys
import time
import threading
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Try to import PyQt5
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer, QObject, pyqtSignal
    from popup_suggestion_window import SuggestionPopup
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    QObject = object  # Fallback
    print("⚠️ PyQt5 not available. Install with: pip install PyQt5")
    sys.exit(1)

# Try to import voice module
try:
    from ui_module.voice_input import VoiceInputHandler
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


# Configuration
MOCK_MODE = False  # Set to True for mock mode (no AI required)
VOICE_MOCK_MODE = True  # Set to False to use real voice (requires Whisper)
AI_API_URL = "http://localhost:8000/process_text"
COOLDOWN_SECONDS = 0.5  # Reduced cooldown for faster re-triggering
PASTE_DELAY = 0.3


class AIKeyboardController(QObject):
    """Main controller that manages keyboard hooks, AI, voice, and UI"""
    
    # Qt signals for thread-safe UI updates
    show_popup_signal = pyqtSignal(str, float)
    hide_popup_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.kb = Controller()  # Keyboard controller
        self.current_keys = set()
        self.is_processing = False
        self.last_trigger = 0
        
        # Voice recording
        self.is_recording_voice = False
        self.is_recording_voice_f9 = False  # F9 voice recording state
        self.voice_text = ""
        self.voice_handler = None
        if VOICE_AVAILABLE and not VOICE_MOCK_MODE:
            try:
                self.voice_handler = VoiceInputHandler(mock_mode=False, model_size="base")
            except Exception as e:
                print(f"⚠️ Voice handler init failed: {e}")
                self.voice_handler = None
        
        # Popup window
        self.popup = None
        self.pending_paste_text = ""  # Text waiting to be pasted on Tab
        
        # Initialize Qt application (must be in main thread)
        self.app = None
        
    def init_ui(self):
        """Initialize Qt UI (must be called from main thread)"""
        if not PYQT_AVAILABLE:
            print("❌ PyQt5 not available. Cannot show popup.")
            return
        
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        self.popup = SuggestionPopup()
        self.popup.suggestion_accepted.connect(self.on_suggestion_accepted)
        self.popup.suggestion_rejected.connect(self.on_suggestion_rejected)
        
        # Connect signals
        self.show_popup_signal.connect(self._show_popup_slot)
        self.hide_popup_signal.connect(self._hide_popup_slot)
        
    def _show_popup_slot(self, text: str, confidence: float):
        """Qt slot to show popup (thread-safe)"""
        self.pending_paste_text = text
        if self.popup:
            try:
                self.popup.show_suggestion(text, confidence, auto_hide_ms=15000)
                print("    💡 Popup displayed - Press Tab to accept or Esc to reject")
            except Exception as e:
                print(f"    ⚠️ Popup error: {e}")
        
    def _hide_popup_slot(self):
        """Qt slot to hide popup (thread-safe)"""
        if self.popup:
            try:
                self.popup.hide_popup()
            except Exception as e:
                print(f"    ⚠️ Hide popup error: {e}")
        
    def on_suggestion_accepted(self, text: str):
        """Handle suggestion acceptance (Tab pressed)"""
        print(f"\n✅ Suggestion accepted: '{text[:50]}...'")
        self.paste_text(text)
        
    def on_suggestion_rejected(self):
        """Handle suggestion rejection (Esc pressed)"""
        print("\n❌ Suggestion rejected")
        self.pending_paste_text = ""
        
    def on_press(self, key):
        """Handle key press events"""
        if self.is_processing:
            return
        
        self.current_keys.add(key)
        
        # === HOTKEY 1: F9 - Voice Selection → Transcribe → Replace ===
        if key == Key.f9:
            self.trigger_f9_voice_replacement()
            self.current_keys.clear()
            return
        
        # === HOTKEY 2: Ctrl+Space - Text Selection → AI → Replace ===
        elif self.check_hotkey({Key.ctrl_l, Key.space}) or self.check_hotkey({Key.ctrl_r, Key.space}):
            self.trigger_text_ai_rewrite()
            
        # === HOTKEY 3: Ctrl+Shift+V - Voice Input ===
        # Check for KeyCode variants of 'v' and 'V'
        elif (Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys) and \
             (Key.shift in self.current_keys or Key.shift_l in self.current_keys or Key.shift_r in self.current_keys):
            # Check if 'v' or 'V' is pressed
            key_char = None
            try:
                if hasattr(key, 'char'):
                    key_char = key.char
            except:
                pass
            
            if key_char and key_char.lower() == 'v':
                self.trigger_voice_input()
                self.current_keys.clear()
                return
            
        # === Tab - Accept suggestion from popup ===
        elif key == Key.tab and self.pending_paste_text:
            print(f"\n✅ Tab pressed - Accepting suggestion")
            # Paste the pending text directly
            thread = threading.Thread(target=self._paste_pending_text)
            thread.daemon = True
            thread.start()
            self.hide_popup_signal.emit()
            return False  # Suppress Tab key
            
        # === Esc - Reject suggestion ===
        elif key == Key.esc and self.pending_paste_text:
            print(f"\n❌ Esc pressed - Rejecting suggestion")
            self.pending_paste_text = ""
            self.hide_popup_signal.emit()
            return False  # Suppress Esc key
            
        # === Ctrl+Esc - Exit program ===
        elif key == Key.esc and (Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys):
            print("\n👋 Exiting...")
            return False
    
    def on_release(self, key):
        """Handle key release"""
        self.current_keys.discard(key)
    
    def check_hotkey(self, hotkey_set):
        """Check if current keys match a hotkey combination"""
        return self.current_keys >= hotkey_set
    
    def trigger_text_ai_rewrite(self):
        """OBJECTIVE 1: Text selection → AI → Replace"""
        elapsed = time.time() - self.last_trigger
        if elapsed < COOLDOWN_SECONDS:
            print(f"⏳ Wait {COOLDOWN_SECONDS - elapsed:.1f}s before next trigger...")
            return
        
        print("\n" + "="*70)
        print("🔑 CTRL+SPACE - Text AI Rewrite")
        print("="*70)
        
        self.last_trigger = time.time()
        
        # Clear keys to prevent repeated triggers
        self.current_keys.clear()
        
        # Process in background thread
        thread = threading.Thread(target=self._process_text_ai)
        thread.daemon = True
        thread.start()
    
    def trigger_f9_voice_replacement(self):
        """NEW WORKFLOW: F9 → Voice → Replace selected text"""
        print(f"\n🎤 F9 Voice triggered (recording: {self.is_recording_voice_f9})")
        
        if self.is_recording_voice_f9:
            # Stop recording and transcribe, then replace
            print("🔴 Stopping recording...")
            self.current_keys.clear()
            
            thread = threading.Thread(target=self._stop_f9_voice_and_replace)
            thread.daemon = True
            thread.start()
        else:
            # Start recording
            print("\n" + "="*70)
            print("🎤 F9 - Voice Recording Started")
            print("="*70)
            print("🔴 Recording... Press F9 again to stop and replace selected text")
            print("   (In mock mode: will auto-stop after 3 seconds)")
            
            self.current_keys.clear()
            self.is_recording_voice_f9 = True
            
            # Start recording
            if self.voice_handler and not VOICE_MOCK_MODE:
                try:
                    self.voice_handler.start_recording()
                    print("✅ Voice handler started")
                except Exception as e:
                    print(f"❌ Error starting recording: {e}")
                    self.is_recording_voice_f9 = False
            else:
                # Mock mode - auto-stop after delay
                print("🧪 Mock mode - will auto-transcribe in 3 seconds...")
                def auto_stop():
                    time.sleep(3)
                    if self.is_recording_voice_f9:
                        self._stop_f9_voice_and_replace()
                
                thread = threading.Thread(target=auto_stop)
                thread.daemon = True
                thread.start()
    
    def trigger_voice_input(self):
        """OBJECTIVE 3: Voice recording → Transcribe → Show in popup"""
        print(f"\n🎤 Voice input triggered (recording: {self.is_recording_voice})")
        
        if self.is_recording_voice:
            # Stop recording and transcribe
            print("🔴 Stopping recording...")
            self.current_keys.clear()
            
            thread = threading.Thread(target=self._stop_voice_recording)
            thread.daemon = True
            thread.start()
        else:
            # Start recording
            print("\n" + "="*70)
            print("🎤 CTRL+SHIFT+V - Voice Input Started")
            print("="*70)
            print("🔴 Recording... Press Ctrl+Shift+V again to stop")
            print("   (In mock mode: will auto-stop after 3 seconds)")
            
            self.current_keys.clear()
            self.is_recording_voice = True
            
            # Start recording
            if self.voice_handler and not VOICE_MOCK_MODE:
                try:
                    self.voice_handler.start_recording()
                    print("✅ Voice handler started")
                except Exception as e:
                    print(f"❌ Error starting recording: {e}")
                    self.is_recording_voice = False
            else:
                # Mock mode - auto-stop after delay
                print("🧪 Mock mode - will auto-transcribe in 3 seconds...")
                def auto_stop():
                    time.sleep(3)
                    if self.is_recording_voice:
                        self._stop_voice_recording()
                
                thread = threading.Thread(target=auto_stop)
                thread.daemon = True
                thread.start()
    
    def _process_text_ai(self):
        """Background thread: Copy selected text → AI → Paste"""
        if self.is_processing:
            print("⚠️  Already processing a request...")
            return
        
        self.is_processing = True
        
        try:
            time.sleep(0.3)
            
            # Step 1: Save original clipboard
            print("1️⃣  Saving clipboard...")
            original_clip = pyperclip.paste()
            
            # Step 2: Copy selected text
            print("2️⃣  Copying selected text...")
            pyperclip.copy("")
            time.sleep(0.1)
            
            self.send_ctrl_c()
            time.sleep(0.25)
            
            copied = pyperclip.paste()
            if not copied:
                print("    ⚠️  No text selected")
                copied = ""
            else:
                print(f"    ✅ Copied: '{copied[:40]}...'")
            
            # Step 3: Send to AI (treat as QUESTION/PROMPT → get ANSWER)
            print("3️⃣  Asking AI about your selection...")
            
            # Build a direct prompt for the AI
            if not copied:
                ai_result = "Please select some text and press Ctrl+Space!"
            else:
                # Call AI with custom prompt for direct answers
                if MOCK_MODE:
                    ai_result = self.mock_ai(copied, action="answer")
                else:
                    # For real AI, construct a direct question/answer prompt
                    prompt_text = f"Answer this question or explain this topic in 2-3 sentences: {copied}"
                    ai_result = self.call_ai(prompt_text, action="expand")
                
            print(f"    ✅ AI response: '{ai_result[:40]}...'")
            
            # Step 4: Direct paste (no popup for text rewrite)
            print("4️⃣  Pasting AI result directly...")
            time.sleep(0.3)
            pyperclip.copy(ai_result)
            time.sleep(0.2)
            self.send_ctrl_v()
            print("    ✅ AI response pasted directly!")
            
            # Step 6: Restore clipboard
            time.sleep(0.3)
            pyperclip.copy(original_clip)
            
            print("\n" + "="*70)
            print("✅ ✅ ✅  COMPLETE! Check your app!")
            print("="*70)
            print("\n⏳ Ready for next trigger (Ctrl+Space)...\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Reset processing flag to allow immediate next execution
            time.sleep(0.2)
            self.is_processing = False
            print("⏳ Ready for next selection!\n")
    
    def _stop_f9_voice_and_replace(self):
        """Background thread: Stop F9 recording, transcribe, and replace selected text"""
        try:
            self.is_recording_voice_f9 = False
            
            # Stop recording and transcribe
            if self.voice_handler and not VOICE_MOCK_MODE:
                print("🔄 Transcribing...")
                transcribed = self.voice_handler.stop_recording_and_transcribe()
            else:
                # Mock transcription
                print("🎤 [MOCK] Simulating transcription...")
                time.sleep(1)
                transcribed = "This is a mock voice transcription replacing your selected text."
            
            print(f"\n🎤 Transcribed: '{transcribed}'")
            
            # Now paste to replace selected text
            print("4️⃣  Replacing selected text with transcription...")
            time.sleep(0.3)
            
            # Save original clipboard
            original_clip = pyperclip.paste()
            
            # Copy transcribed text to clipboard
            pyperclip.copy(transcribed)
            time.sleep(0.2)
            
            # Paste to replace selection
            self.send_ctrl_v()
            time.sleep(0.2)
            
            # Restore clipboard
            pyperclip.copy(original_clip)
            
            print("\n" + "="*70)
            print("✅ ✅ ✅  Voice text pasted! Check your app!")
            print("="*70)
            print("\n⏳ Ready for next F9 trigger...\n")
            
        except Exception as e:
            print(f"\n❌ Voice error: {e}")
            import traceback
            traceback.print_exc()
    
    def _stop_voice_recording(self):
        """Background thread: Stop recording and transcribe"""
        try:
            self.is_recording_voice = False
            
            # Stop recording and transcribe
            if self.voice_handler and not VOICE_MOCK_MODE:
                print("🔄 Transcribing...")
                transcribed = self.voice_handler.stop_recording_and_transcribe()
            else:
                # Mock transcription
                print("🎤 [MOCK] Simulating transcription...")
                time.sleep(1)
                transcribed = "This is a mock voice transcription. Press Tab to paste this text."
            
            print(f"\n🎤 Transcribed: '{transcribed}'")
            
            # Show in popup
            self.show_popup_signal.emit(transcribed, 0.85)
            print("\n💡 Suggestion shown in popup - Press Tab to paste!")
            
        except Exception as e:
            print(f"\n❌ Voice error: {e}")
            import traceback
            traceback.print_exc()
    
    def call_ai(self, text: str, action: str = "expand") -> str:
        """Call AI engine (mock or real)"""
        if MOCK_MODE:
            return self.mock_ai(text, action)
        
        # Real AI call
        import requests
        try:
            print(f"    🤖 Calling local AI engine ({action} mode)...")
            payload = {
                "text": text,
                "action": action,
                "app": "unified_keyboard",
                "context": {"previous_text": "", "user_style": "default"},
                "api_version": "v1"
            }
            
            response = requests.post(AI_API_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("result_text", text)
            else:
                print(f"    ⚠️ AI API error: {response.status_code}")
                return self.mock_ai(text, action)
                
        except requests.exceptions.ConnectionError:
            print(f"    ⚠️ Cannot connect to AI engine. Is it running?")
            print(f"    💡 Start it with: uvicorn ai_engine.api_service:app --reload")
            return self.mock_ai(text, action)
        except Exception as e:
            print(f"    ⚠️ AI call failed: {e}")
            return self.mock_ai(text, action)
    
    def mock_ai(self, text: str, action: str = "expand") -> str:
        """Mock AI for testing - treats text as question/prompt"""
        time.sleep(0.3)
        
        if not text:
            return "AI is ready! Select some text and press Ctrl+Space."
        
        text_lower = text.lower().strip()
        
        # Answer based on selected text (treating it as a question/topic)
        if "science" in text_lower:
            return "Science is the systematic study of the natural world through observation, experimentation, and analysis. It encompasses physics, chemistry, biology, and many other disciplines that help us understand how the universe works."
        elif "life" in text_lower:
            return "Life is the condition that distinguishes living organisms from inorganic matter, characterized by growth, reproduction, functional activity, and continual change. It's a complex phenomenon that scientists continue to study and understand."
        elif "ai" in text_lower or "artificial intelligence" in text_lower:
            return "Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems. It includes machine learning, natural language processing, and computer vision to enable computers to perform tasks that typically require human intelligence."
        elif "python" in text_lower:
            return "Python is a high-level, interpreted programming language created by Guido van Rossum. It's known for its simple, readable syntax and is widely used in web development, data science, automation, and artificial intelligence applications."
        elif "hello" in text_lower or "hi" in text_lower:
            return "Hello! I'm your AI assistant. I can help you with information, writing, and answering questions. Just select any text and press Ctrl+Space!"
        elif "?" in text:
            # It's a question
            return f"That's a great question about '{text}'. The answer involves understanding key concepts and their practical applications. Let me explain it in simple terms for better clarity."
        else:
            # Generic explanation for any topic
            return f"{text.capitalize()} is an important topic that encompasses various aspects and applications. It plays a significant role in its field and has multiple considerations to keep in mind."
    
    def send_ctrl_c(self):
        """Send Ctrl+C"""
        with self.kb.pressed(Key.ctrl):
            self.kb.press('c')
            time.sleep(0.05)
            self.kb.release('c')
    
    def send_ctrl_v(self):
        """Send Ctrl+V"""
        with self.kb.pressed(Key.ctrl):
            self.kb.press('v')
            time.sleep(0.05)
            self.kb.release('v')
    
    def _paste_pending_text(self):
        """Paste the pending text (called from Tab key)"""
        if not self.pending_paste_text:
            return
        
        text = self.pending_paste_text
        self.pending_paste_text = ""
        
        try:
            print(f"📋 Pasting from popup: '{text[:50]}...'")
            original_clip = pyperclip.paste()
            
            pyperclip.copy(text)
            time.sleep(PASTE_DELAY)
            self.send_ctrl_v()
            time.sleep(0.2)
            
            pyperclip.copy(original_clip)
            print("    ✅ Pasted successfully!")
        except Exception as e:
            print(f"    ❌ Paste error: {e}")
    
    def paste_text(self, text: str):
        """Paste text to active window"""
        try:
            print(f"📋 Pasting: '{text[:50]}...'")
            original_clip = pyperclip.paste()
            
            pyperclip.copy(text)
            time.sleep(PASTE_DELAY)
            self.send_ctrl_v()
            time.sleep(0.2)
            
            pyperclip.copy(original_clip)
            print("    ✅ Pasted successfully!")
        except Exception as e:
            print(f"    ❌ Paste error: {e}")
    
    def start(self):
        """Start the AI keyboard"""
        print("\n" + "="*70)
        print("🚀 UNIFIED AI KEYBOARD - ALL OBJECTIVES")
        print("="*70)
        print("\n✨ FEATURES:")
        print("   1️⃣  Voice Selection → Transcribe → Replace (F9)")
        print("       Hotkey: F9")
        print("       • Select any text or letter in any app")
        print("       • Press F9 to start voice recording")
        print("       • Press F9 again to stop & replace with transcription")
        print("       • Transcribed text replaces your selection automatically")
        print()
        print("   2️⃣  Text Selection → AI Rewrite (Direct Paste)")
        print("       Hotkey: Ctrl + Space")
        print("       • Select text in any app")
        print("       • Press Ctrl+Space")
        print("       • AI response pastes directly (no popup)")
        print()
        print("   3️⃣  Voice Input → Transcribe → Paste (with Popup)")
        print("       Hotkey: Ctrl + Shift + V")
        print("       • Press once to start recording")
        print("       • Press again to stop & transcribe")
        print("       • Tab to paste transcribed text")
        print()
        print("⚙️  MODE:", "🧪 MOCK (for testing)" if MOCK_MODE else "🤖 REAL AI")
        print("🛑 EXIT: Ctrl + Esc")
        print("\n⏳ Ready! Try it in Notepad, Word, VS Code, etc.")
        print("="*70 + "\n")
        
        # Initialize UI
        self.init_ui()
        
        # Start keyboard listener in background thread
        listener_thread = threading.Thread(target=self._run_keyboard_listener)
        listener_thread.daemon = True
        listener_thread.start()
        
        # Run Qt event loop
        sys.exit(self.app.exec_())
    
    def _run_keyboard_listener(self):
        """Run keyboard listener in background thread"""
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    controller = AIKeyboardController()
    try:
        controller.start()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
