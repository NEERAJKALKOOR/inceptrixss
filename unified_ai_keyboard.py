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
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Try to import PyQt5
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer, QObject, pyqtSignal
    from popup_suggestion_window import SuggestionPopup
    from recording_status_popup import RecordingStatusPopup
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    QObject = object  # Fallback
    print("⚠️ PyQt5 not available. Install with: pip install PyQt5")
    sys.exit(1)

# Try to import voice module
try:
    from ui_module.voice_input import voice_handler  # Use the singleton that works!
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    voice_handler = None

# Import context detection and history management
try:
    from window_detector import window_detector, get_active_context
    from context_personas import get_persona_for_context, format_ai_prompt
    from suggestion_history import suggestion_history
    CONTEXT_FEATURES_AVAILABLE = True
    print("✅ Context detection & history enabled")
except ImportError as e:
    CONTEXT_FEATURES_AVAILABLE = False
    window_detector = None
    suggestion_history = None
    print(f"⚠️ Context features not available: {e}")
    print("   Install: pip install pywin32 psutil")


# Configuration
MOCK_MODE = False  # Set to True for mock mode (no AI required)
VOICE_MOCK_MODE = False  # Set to False to use real voice (requires Whisper)
AI_API_URL = "http://localhost:8000/process_text"
COOLDOWN_SECONDS = 0.5  # Reduced cooldown for faster re-triggering
PASTE_DELAY = 0.3


class AIKeyboardController(QObject):
    """Main controller that manages keyboard hooks, AI, voice, and UI"""
    
    # Qt signals for thread-safe UI updates
    show_popup_signal = pyqtSignal(str, float)
    hide_popup_signal = pyqtSignal()
    show_recording_signal = pyqtSignal()
    show_stopped_signal = pyqtSignal()
    show_processing_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.kb = Controller()  # Keyboard controller
        self.current_keys = set()
        self.is_processing = False
        self.last_trigger = 0
        
        # Voice recording
        self.is_recording_voice = False
        self.is_recording_voice_f9 = False  # F9 voice recording state
        self.is_recording_ctrl_f11 = False  # Ctrl+F11 voice with AI enhancement
        self.voice_text = ""
        
        # Use the singleton voice handler (same one used in test_voice_whisper.py)
        if VOICE_AVAILABLE:
            print("🎤 Voice: Using real Whisper (same as test_voice_whisper.py)")
            if voice_handler.mock_mode:
                print("⚠️  Voice handler in mock mode (missing dependencies)")
            else:
                print(f"✅ Voice handler ready - model: {voice_handler.model_size}")
        else:
            print("⚠️ Voice module not available - install requirements_ui.txt")
        
        # Popup windows
        self.popup = None
        self.recording_popup = None
        self.pending_paste_text = ""  # Text waiting to be pasted on Tab
        
        # Context detection and history
        self.current_context = "general"  # Detected app context
        self.current_app_name = "unknown"  # App name
        self.last_original_text = ""  # Store for history
        
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
        
        # Recording status popup
        self.recording_popup = RecordingStatusPopup()
        
        # Connect signals
        self.show_popup_signal.connect(self._show_popup_slot)
        self.hide_popup_signal.connect(self._hide_popup_slot)
        self.show_recording_signal.connect(self._show_recording_slot)
        self.show_stopped_signal.connect(self._show_stopped_slot)
        self.show_processing_signal.connect(self._show_processing_slot)
        
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
    
    def _show_recording_slot(self):
        """Qt slot to show recording status (thread-safe)"""
        if self.recording_popup:
            try:
                self.recording_popup.show_recording()
            except Exception as e:
                print(f"    ⚠️ Recording popup error: {e}")
    
    def _show_stopped_slot(self):
        """Qt slot to show stopped recording status (thread-safe)"""
        if self.recording_popup:
            try:
                self.recording_popup.show_stopped()
            except Exception as e:
                print(f"    ⚠️ Stopped popup error: {e}")
    
    def _show_processing_slot(self):
        """Qt slot to show processing status (thread-safe)"""
        if self.recording_popup:
            try:
                self.recording_popup.show_processing()
            except Exception as e:
                print(f"    ⚠️ Processing popup error: {e}")
        
    def on_suggestion_accepted(self, text: str):
        """Handle suggestion acceptance (Tab pressed)"""
        print(f"\n✅ Suggestion accepted: '{text[:50]}...'")
        self.paste_text(text)
        
        # Mark in history as accepted
        if CONTEXT_FEATURES_AVAILABLE and suggestion_history:
            suggestion_history.mark_accepted(True)
        
    def on_suggestion_rejected(self):
        """Handle suggestion rejection (Esc pressed)"""
        print("\n❌ Suggestion rejected")
        self.pending_paste_text = ""
        
        # Mark in history as rejected
        if CONTEXT_FEATURES_AVAILABLE and suggestion_history:
            suggestion_history.mark_accepted(False)
    
    def show_previous_suggestion(self):
        """Navigate to previous suggestion in history (Ctrl+Shift+Up)"""
        if not CONTEXT_FEATURES_AVAILABLE or not suggestion_history:
            print("⚠️ History feature not available")
            return
        
        previous = suggestion_history.get_previous()
        
        if previous:
            print(f"\n⬅️  Previous suggestion:")
            print(f"   Original: '{previous['original_text'][:40]}...'")
            print(f"   Context: {previous['context']}")
            print(f"   Action: {previous['action']}")
            print(f"   💡 Showing in popup - Press Tab to use")
            
            # Show in popup
            self.pending_paste_text = previous['suggestion']
            self.show_popup_signal.emit(previous['suggestion'], 0.75)
        else:
            print("⬅️  Already at oldest suggestion")
    
    def show_next_suggestion(self):
        """Navigate to next suggestion in history (Ctrl+Shift+Down)"""
        if not CONTEXT_FEATURES_AVAILABLE or not suggestion_history:
            print("⚠️ History feature not available")
            return
        
        next_item = suggestion_history.get_next()
        
        if next_item:
            print(f"\n➡️  Next suggestion:")
            print(f"   Original: '{next_item['original_text'][:40]}...'")
            print(f"   Context: {next_item['context']}")
            print(f"   Action: {next_item['action']}")
            print(f"   💡 Showing in popup - Press Tab to use")
            
            # Show in popup
            self.pending_paste_text = next_item['suggestion']
            self.show_popup_signal.emit(next_item['suggestion'], 0.75)
        else:
            print("➡️  Back to current suggestion / No more in history")
        
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
        
        # === HOTKEY 1B: F11 - Check for Ctrl+F11 (Voice + AI) ===
        if key == Key.f11:
            # Check if Ctrl is pressed → Ctrl+F11 (Voice + AI)
            if Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys:
                self.trigger_ctrl_f11_voice_ai()
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
        
        # === NEW: Ctrl+Shift+Up - Previous suggestion from history ===
        elif (Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys) and \
             (Key.shift in self.current_keys or Key.shift_l in self.current_keys or Key.shift_r in self.current_keys) and \
             key == Key.up:
            if CONTEXT_FEATURES_AVAILABLE and suggestion_history:
                self.show_previous_suggestion()
                self.current_keys.clear()
                return False  # Suppress arrow key
        
        # === NEW: Ctrl+Shift+Down - Next suggestion from history ===
        elif (Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys) and \
             (Key.shift in self.current_keys or Key.shift_l in self.current_keys or Key.shift_r in self.current_keys) and \
             key == Key.down:
            if CONTEXT_FEATURES_AVAILABLE and suggestion_history:
                self.show_next_suggestion()
                self.current_keys.clear()
                return False  # Suppress arrow key
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
    
    def trigger_ctrl_f11_voice_ai(self):
        """NEW: Ctrl+F11 → Voice → Transcribe → AI Enhance → Paste"""
        print(f"\n🎤✨ Ctrl+F11 Voice+AI triggered (is_recording_ctrl_f11: {self.is_recording_ctrl_f11})")
        print(f"    voice_handler.is_recording: {voice_handler.is_recording if voice_handler else 'N/A'}")
        
        if self.is_recording_ctrl_f11:
            # Stop recording, transcribe, send to AI, and paste
            print("🔴 Stopping recording...")
            self.current_keys.clear()
            
            thread = threading.Thread(target=self._stop_ctrl_f11_voice_ai_replace)
            thread.daemon = True
            thread.start()
        else:
            # Start recording
            print("\n" + "="*70)
            print("🎤✨ Ctrl+F11 - Voice + AI Enhancement")
            print("="*70)
            
            if voice_handler and voice_handler.mock_mode:
                print("🧪 MOCK MODE: Will auto-transcribe + AI enhance in 3 seconds...")
            else:
                print("🔴 RECORDING FROM MICROPHONE")
                print("   🗣️  SPEAK NOW - Your voice will be transcribed and AI-enhanced")
                print("   🔴 Press Ctrl+F11 again when finished speaking")
            
            self.current_keys.clear()
            self.is_recording_ctrl_f11 = True
            
            # Start recording
            if VOICE_AVAILABLE and voice_handler and not voice_handler.mock_mode:
                try:
                    print(f"🔍 Before start_recording: voice_handler.is_recording={voice_handler.is_recording}")
                    voice_handler.start_recording()
                    time.sleep(0.2)
                    print(f"✅ Microphone active - voice_handler.is_recording={voice_handler.is_recording}")
                    self.show_recording_signal.emit()
                except Exception as e:
                    print(f"❌ Error starting recording: {e}")
                    self.is_recording_ctrl_f11 = False
            else:
                # Mock mode
                def auto_stop():
                    time.sleep(3)
                    if self.is_recording_ctrl_f11:
                        self._stop_ctrl_f11_voice_ai_replace()
                
                thread = threading.Thread(target=auto_stop)
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
            
            if voice_handler.mock_mode:
                print("🧪 MOCK MODE: Will auto-transcribe in 3 seconds...")
            else:
                print("🔴 RECORDING FROM MICROPHONE")
                print("   🗣️  SPEAK NOW - Say what you want to replace the selection with")
                print("   🔴 Press F9 again when finished speaking")
            
            self.current_keys.clear()
            self.is_recording_voice_f9 = True
            
            # Debug: Check voice_handler status before recording
            print(f"🔍 DEBUG Start: VOICE_AVAILABLE={VOICE_AVAILABLE}, voice_handler exists={voice_handler is not None}, mock_mode={voice_handler.mock_mode if voice_handler else 'N/A'}")
            
            # Start recording using singleton voice_handler
            if VOICE_AVAILABLE and voice_handler and not voice_handler.mock_mode:
                try:
                    print(f"🔍 DEBUG Before start: is_recording={voice_handler.is_recording}")
                    voice_handler.start_recording()
                    time.sleep(0.2)  # Give it a moment to start
                    print(f"✅ Microphone active - is_recording={voice_handler.is_recording}")
                    
                    # Show recording popup
                    self.show_recording_signal.emit()
                except Exception as e:
                    print(f"❌ Error starting recording: {e}")
                    print("   💡 Check microphone permissions and try again")
                    self.is_recording_voice_f9 = False
            else:
                # Mock mode - auto-stop after delay
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
            
            # Start recording using singleton voice_handler
            if VOICE_AVAILABLE and not voice_handler.mock_mode:
                try:
                    voice_handler.start_recording()
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
            
            # NEW: Detect context from active window
            if CONTEXT_FEATURES_AVAILABLE and window_detector:
                window_info = window_detector.get_active_window_info()
                self.current_context = window_info['context']
                self.current_app_name = window_info['process']
                print(f"🎯 Context detected: {self.current_context} ({self.current_app_name})")
            else:
                self.current_context = "general"
                self.current_app_name = "unknown"
            
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
                self.last_original_text = copied  # Store for history
            
            # Step 3: Send to AI (treat as QUESTION/PROMPT → get ANSWER)
            print(f"3️⃣  Asking AI about your selection... (context: {self.current_context})")
            
            # Build a direct prompt for the AI
            if not copied:
                ai_result = "Please select some text and press Ctrl+Space!"
            else:
                # Call AI with context-aware prompt
                if MOCK_MODE:
                    ai_result = self.mock_ai(copied, action="answer", context=self.current_context)
                else:
                    # For real AI, use context-aware prompt
                    ai_result = self.call_ai(copied, action="expand", context=self.current_context)
                
                # Store in history
                if CONTEXT_FEATURES_AVAILABLE and suggestion_history:
                    suggestion_history.add(
                        suggestion=ai_result,
                        context=self.current_context,
                        action="expand",
                        original_text=copied
                    )
                    stats = suggestion_history.get_stats()
                    print(f"    📜 History: {stats['total']} total, {stats['acceptance_rate']:.0%} accepted")
                
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
    
    def _stop_ctrl_f11_voice_ai_replace(self):
        """Background thread: Stop Ctrl+F11, transcribe, AI enhance, and paste"""
        try:
            print("🔴 Stopping recording & transcribing...")
            
            # Stop recording and transcribe
            if VOICE_AVAILABLE and voice_handler and not voice_handler.mock_mode:
                print("🔄 Processing audio with Whisper AI...")
                self.show_processing_signal.emit()
                
                transcribed = voice_handler.stop_recording_and_transcribe()
                
                if not transcribed or transcribed.startswith("["):
                    print("⚠️  Could not transcribe audio. Please try again.")
                    return
            else:
                # Mock transcription
                print("🎤 [MOCK] Simulating transcription...")
                time.sleep(1)
                transcribed = "hello this is a test message"
            
            print(f"\n✅ Transcribed: '{transcribed}'")
            
            # Detect context
            detected_context = "general"
            if CONTEXT_FEATURES_AVAILABLE:
                window_info = window_detector.get_active_window_info()
                detected_context = window_info['context']
                print(f"📍 Detected context: {detected_context} ({window_info['process']})")
            
            # Choose action based on context
            # For code: use "expand" to generate full implementation
            # For others: use "rewrite" to improve the text
            action = "expand" if detected_context == "code" else "rewrite"
            
            # Send to AI for enhancement
            print(f"🤖 Enhancing with AI (action: {action})...")
            ai_enhanced = self.call_ai(transcribed, action=action, context=detected_context)
            
            print(f"\n✨ AI Output: '{ai_enhanced}'")
            
            # Hide popups before pasting
            if self.recording_popup:
                try:
                    self.recording_popup.hide()
                except:
                    pass
            
            time.sleep(0.8)
            
            # Click to restore focus
            try:
                print("📍 Clicking to restore focus...")
                pyautogui.click()
                time.sleep(0.2)
            except Exception as e:
                print(f"⚠️ Could not click: {e}")
            
            # Paste AI-enhanced text directly (no popup)
            original_clip = pyperclip.paste()
            pyperclip.copy(ai_enhanced)
            time.sleep(0.3)
            self.send_ctrl_v()
            time.sleep(0.3)
            pyperclip.copy(original_clip)
            
            print("\n" + "="*70)
            print("✅ ✅ ✅  AI-Enhanced voice text pasted!")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ Ctrl+F11 error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Always reset state to allow next use
            self.is_recording_ctrl_f11 = False
            print("⏳ Ctrl+F11 ready for next use\n")
    
    def _stop_f9_voice_and_replace(self):
        """Background thread: Stop F9 recording, transcribe, and replace selected text"""
        try:
            self.is_recording_voice_f9 = False
            
            # Debug: Check voice_handler status
            print(f"🔍 DEBUG Stop: VOICE_AVAILABLE={VOICE_AVAILABLE}, voice_handler={voice_handler is not None}, mock_mode={voice_handler.mock_mode if voice_handler else 'N/A'}")
            print(f"🔍 DEBUG: voice_handler.is_recording={voice_handler.is_recording if voice_handler else 'N/A'}")
            
            # Stop recording and transcribe using singleton voice_handler
            if VOICE_AVAILABLE and voice_handler and not voice_handler.mock_mode:
                print("🔄 Processing audio with Whisper AI...")
                
                # Show processing popup
                self.show_processing_signal.emit()
                
                transcribed = voice_handler.stop_recording_and_transcribe()
                print(f"🔍 DEBUG: Transcription result = '{transcribed}'")
                
                if not transcribed or transcribed.startswith("["):
                    print("⚠️  Could not transcribe audio. Please try again.")
                    print("   Make sure you spoke clearly into the microphone.")
                    return
            else:
                # Mock transcription - this should NOT run if voice is working
                print("🎤 [MOCK] Simulating transcription...")
                print(f"   Why mock? VOICE_AVAILABLE={VOICE_AVAILABLE}, voice_handler exists={voice_handler is not None}, mock_mode={voice_handler.mock_mode if voice_handler else 'N/A'}")
                time.sleep(1)
                transcribed = "This is a mock voice transcription replacing your selected text."
            
            print(f"\n✅ Transcribed: '{transcribed}'")
            
            # Now paste to replace selected text
            print("📝 Replacing selected text with transcription...")
            
            # Hide all popups FIRST to ensure focus returns to target app
            if self.recording_popup:
                try:
                    self.recording_popup.hide()
                except:
                    pass
            
            # Give time for focus to return and clipboard to be ready
            time.sleep(0.8)
            
            # Click to restore focus to target window
            try:
                print("📍 Clicking to restore focus...")
                pyautogui.click()
                time.sleep(0.2)
            except Exception as e:
                print(f"⚠️ Could not click: {e}")
            
            # Save original clipboard
            original_clip = pyperclip.paste()
            
            # Copy transcribed text to clipboard
            pyperclip.copy(transcribed)
            time.sleep(0.3)
            
            # Paste to replace selection - send Ctrl+V
            print("⏬ Sending Ctrl+V to paste...")
            self.send_ctrl_v()
            time.sleep(0.3)
            
            # Restore clipboard
            pyperclip.copy(original_clip)
            
            # NOW show success popup after paste is complete
            self.show_stopped_signal.emit()
            
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
            
            # Stop recording and transcribe using singleton voice_handler
            if VOICE_AVAILABLE and not voice_handler.mock_mode:
                print("🔄 Transcribing...")
                transcribed = voice_handler.stop_recording_and_transcribe()
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
    
    def call_ai(self, text: str, action: str = "expand", context: str = "general") -> str:
        """Call AI engine (mock or real) with context awareness"""
        if MOCK_MODE:
            return self.mock_ai(text, action, context)
        
        # Get context-aware persona
        if CONTEXT_FEATURES_AVAILABLE:
            persona = get_persona_for_context(context)
            print(f"    🎭 Using persona: {persona['name']}")
        
        # Real AI call
        import requests
        try:
            print(f"    🤖 Calling local AI engine ({action} mode, context: {context})...")
            
            # Build context-aware prompt if available
            if CONTEXT_FEATURES_AVAILABLE:
                enhanced_text = format_ai_prompt(text, action, context)
            else:
                enhanced_text = f"Answer this question or explain this topic in 2-3 sentences: {text}"
            
            payload = {
                "text": enhanced_text,
                "action": action,
                "app": self.current_app_name,
                "context": {"detected_context": context, "user_style": "default"},
                "api_version": "v1"
            }
            
            response = requests.post(AI_API_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("result_text", text)
            else:
                print(f"    ⚠️ AI API error: {response.status_code}")
                return self.mock_ai(text, action, context)
                
        except requests.exceptions.ConnectionError:
            print(f"    ⚠️ Cannot connect to AI engine. Is it running?")
            print(f"    💡 Start it with: uvicorn ai_engine.api_service:app --reload")
            return self.mock_ai(text, action, context)
        except Exception as e:
            print(f"    ⚠️ AI call failed: {e}")
            return self.mock_ai(text, action, context)
    
    def mock_ai(self, text: str, action: str = "expand", context: str = "general") -> str:
        """Mock AI for testing - context-aware responses"""
        time.sleep(0.3)
        
        if not text:
            return "AI is ready! Select some text and press Ctrl+Space."
        
        text_lower = text.lower().strip()
        
        # Context-aware transformations
        if context == "email":
            # Professional email style
            if "hey" in text_lower or "hi" in text_lower:
                return "Dear [Name],\n\nI hope this message finds you well."
            elif "thx" in text_lower or "thanks" in text_lower:
                return "Thank you for your time and consideration. I appreciate your prompt response."
            elif "can we meet" in text_lower or "meeting" in text_lower:
                return "Dear [Name],\n\nI hope this message finds you well. I would like to schedule a meeting at your earliest convenience. Please let me know your availability.\n\nBest regards"
            else:
                return f"Dear [Name],\n\n{text.capitalize()}. I look forward to your response.\n\nBest regards"
        
        elif context == "code":
            # Code-related responses
            if "function" in text_lower or "def" in text_lower:
                return '''def process_data(data: list) -> dict:
    """
    Process input data and return results.
    
    Args:
        data: Input data to process
    
    Returns:
        Processed results as dictionary
    """
    result = {}
    # Implementation here
    return result'''
            elif "class" in text_lower:
                return '''class DataProcessor:
    """Main data processing class."""
    
    def __init__(self):
        self.data = []
    
    def process(self):
        """Process the data."""
        pass'''
            else:
                return f"# {text}\n# TODO: Implement this functionality\npass"
        
        elif context == "chat":
            # Casual messaging style
            if "okay" in text_lower or "ok" in text_lower:
                return "sounds good! 👍"
            elif "thank" in text_lower:
                return "no problem! 😊"
            elif "yes" in text_lower:
                return "yeah definitely! ✅"
            else:
                return f"{text.lower()} 😊"
        
        elif context == "document":
            # Formal document style
            return f"{text.capitalize()}. This represents a significant consideration that warrants careful examination and thorough analysis. The implications of this matter extend across multiple dimensions and require comprehensive understanding."
        
        # General fallback - treat as question/topic
        elif "science" in text_lower:
            return "Science is the systematic study of the natural world through observation, experimentation, and analysis. It encompasses physics, chemistry, biology, and many other disciplines that help us understand how the universe works."
        elif "ai" in text_lower or "artificial intelligence" in text_lower:
            return "Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems. It includes machine learning, natural language processing, and computer vision to enable computers to perform tasks that typically require human intelligence."
        elif "?" in text:
            return f"That's a great question about '{text}'. The answer involves understanding key concepts and their practical applications. Let me explain it in simple terms for better clarity."
        else:
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
        print("   1️⃣  Voice → Transcribe (Direct)")
        print("       Hotkey: F9")
        print("       • Press F9 to start recording")
        print("       • Press F9 again to stop & paste transcription")
        print("       • Raw transcription, no AI processing")
        print()
        print("   2️⃣  Voice → AI Enhanced (Smart)")
        print("       Hotkey: Ctrl + F11 🆕")
        print("       • Press Ctrl+F11 to start recording")
        print("       • Press Ctrl+F11 again to stop")
        print("       • Shows: 'What you said' + 'AI output'")
        print("       • Transcribes → AI improves → Pastes enhanced text")
        print("       • Context-aware: Casual in chat, formal in email!")
        print()
        print("   3️⃣  Text → AI Rewrite (Direct Paste)")
        print("       Hotkey: Ctrl + Space")
        print("       • Select text in any app")
        print("       • Press Ctrl+Space")
        print("       • AI response pastes directly")
        print("       • Context-aware: Adapts tone based on app!")
        print()
        print("   4️⃣  Voice Input → Popup (Manual Paste)")
        print("       Hotkey: Ctrl + Shift + V")
        print("       • Press once to start recording")
        print("       • Press again to stop & transcribe")
        print("       • Tab to paste transcribed text")
        print()
        print("   5️⃣  Suggestion History Navigation")
        print("       Hotkeys: Ctrl + Shift + ↑/↓")
        print("       • Ctrl+Shift+Up: Previous suggestion")
        print("       • Ctrl+Shift+Down: Next suggestion")
        print("       • Stores last 10 AI suggestions")
        print("       • Press Tab to reuse any suggestion")
        print()
        print("⚙️  AI MODE:", "🧪 MOCK (for testing)" if MOCK_MODE else "🤖 REAL AI")
        
        # Show context detection status
        if CONTEXT_FEATURES_AVAILABLE:
            print("🎯 CONTEXT: ✅ Smart Detection Enabled")
            print("   🔍 Auto-detects: Email, Code, Chat, Document, Browser, Notes")
        else:
            print("🎯 CONTEXT: ⚠️  Not available (install: pip install pywin32 psutil)")
        
        # Check actual voice_handler status
        if VOICE_AVAILABLE and voice_handler:
            voice_status = "🧪 MOCK (missing dependencies)" if voice_handler.mock_mode else "✅ REAL WHISPER"
            print("🎤 VOICE MODE:", voice_status)
            if not voice_handler.mock_mode:
                print("   💡 Whisper model:", voice_handler.model_size)
        else:
            print("🎤 VOICE MODE: ❌ NOT AVAILABLE")
            
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
