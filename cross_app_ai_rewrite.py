"""
Cross-Application AI Text Rewriting System

Works by simulating standard copy-paste shortcuts across any application.
NO caret tracking, NO DOM manipulation, NO app-specific APIs.

Hotkey: Ctrl + Space
Flow: Copy → AI Process → Paste → Restore Clipboard
"""

import time
import pyperclip
import pyautogui
import requests
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller
import sys
import os

# Configuration
AI_API_URL = "http://localhost:8000/process_text"
MOCK_MODE = True  # Set to False if using real Ollama service
HOTKEY = {Key.ctrl_l, Key.space}  # Ctrl + Space
COPY_DELAY = 0.2  # Delay after Ctrl+C to read clipboard (increased for reliability)
PASTE_DELAY = 0.1  # Delay before Ctrl+V (increased for reliability)
COOLDOWN_SECONDS = 2.0  # Minimum time between triggers to prevent loops
SWITCH_WINDOW_DELAY = 1.5  # Time for user to switch to target app after hotkey


class CrossAppAIRewriter:
    """
    Global AI text rewriting system using clipboard simulation.
    """
    
    def __init__(self):
        self.keyboard_controller = Controller()
        self.current_keys = set()
        self.is_processing = False
        self.listener = None
        self.last_trigger_time = 0
        self.cooldown_period = COOLDOWN_SECONDS  # Use constant from config
        
    def on_press(self, key):
        """Handle key press events"""
        # Ignore keys while processing
        if self.is_processing:
            return
            
        self.current_keys.add(key)
        
        # Check if hotkey combination is pressed
        if self.current_keys >= HOTKEY:
            # Check cooldown
            current_time = time.time()
            if current_time - self.last_trigger_time < self.cooldown_period:
                print("⏳ Cooldown active, please wait...")
                return
            
            print("\n" + "="*60)
            print("🔑 Ctrl+Space DETECTED!")
            print("="*60)
            print("\n⚠️  QUICKLY! Switch to your target app (Notepad, Word, etc.)")
            print(f"    You have {SWITCH_WINDOW_DELAY:.1f} seconds...\n")
            
            self.last_trigger_time = current_time
            
            # Clear keys immediately to prevent re-trigger
            self.current_keys.clear()
            
            # Countdown to give user time to switch windows
            for i in range(int(SWITCH_WINDOW_DELAY), 0, -1):
                print(f"   Starting in {i}s...", end='\r')
                time.sleep(1)
            
            print("\n✅ Processing now...\n")
            self.trigger_ai_rewrite()
            
    def on_release(self, key):
        """Handle key release events"""
        try:
            self.current_keys.discard(key)
        except KeyError:
            pass
            
        # Exit on Ctrl+Shift+Q
        if key == Key.esc and Key.ctrl in self.current_keys:
            print("\n👋 Exiting Cross-App AI Rewriter...")
            return False
    
    def trigger_ai_rewrite(self):
        """
        Main AI rewrite flow:
        1. Save clipboard
        2. Simulate Ctrl+C
        3. Read copied text
        4. Send to AI
        5. Copy AI response
        6. Simulate Ctrl+V
        7. Restore clipboard
        """
        self.is_processing = True
        
        # CRITICAL: Release all modifier keys first
        for key in ['ctrl', 'shift', 'alt', 'win']:
            try:
                pyautogui.keyUp(key)
            except:
                pass
        
        time.sleep(0.2)  # Wait for key release
        
        try:
            # Step 1: Save existing clipboard
            original_clipboard = self._safe_get_clipboard()
            print(f"📋 Original clipboard saved: '{original_clipboard[:50]}...'")
            
            # Step 2: Simulate Ctrl+C to copy selected text
            print("📤 Simulating Ctrl+C...")
            pyperclip.copy("")  # Clear clipboard first
            time.sleep(0.05)
            
            # Use keyDown/press/keyUp for more reliable Ctrl+C
            pyautogui.keyDown('ctrl')
            time.sleep(0.05)
            pyautogui.press('c')
            time.sleep(0.05)
            pyautogui.keyUp('ctrl')
            
            # Step 3: Wait and read clipboard
            time.sleep(COPY_DELAY)
            copied_text = pyperclip.paste()
            
            # Handle edge case: no selection
            if not copied_text or copied_text == "":
                print("⚠️  No text selected. AI will generate fresh text...")
                copied_text = ""
            else:
                print(f"✅ Copied text: '{copied_text[:50]}...'")
            
            # Step 4: Send to AI for processing
            ai_result = self._call_ai(copied_text)
            print(f"🧠 AI response: '{ai_result[:50]}...'")
            
            # Step 5: Copy AI result to clipboard
            print("📝 Copying AI result to clipboard...")
            pyperclip.copy(ai_result)
            time.sleep(0.15)  # Wait for clipboard to update
            
            # Verify clipboard has AI result
            verify_clip = pyperclip.paste()
            if verify_clip != ai_result:
                print("⚠️  Clipboard verification failed, retrying...")
                pyperclip.copy(ai_result)
                time.sleep(0.1)
            
            # Step 6: Simulate Ctrl+V to paste
            print("📥 Pasting with Ctrl+V...")
            time.sleep(0.15)  # Extra delay before paste
            
            # Use press/release for more reliable paste
            pyautogui.keyDown('ctrl')
            time.sleep(0.05)
            pyautogui.press('v')
            time.sleep(0.05)
            pyautogui.keyUp('ctrl')
            
            print("✅ Paste command sent!")
            
            # CRITICAL: Wait after paste to prevent re-trigger
            time.sleep(0.3)
            
            # Step 7: Restore original clipboard
            time.sleep(0.1)
            pyperclip.copy(original_clipboard)
            print("✅ Original clipboard restored")
            print("✨ AI rewrite complete!\n")
            
        except Exception as e:
            print(f"❌ Error during AI rewrite: {e}")
            import traceback
            traceback.print_exc()  # Show full error for debugging
            # Try to restore clipboard even on error
            try:
                if 'original_clipboard' in locals():
                    pyperclip.copy(original_clipboard)
            except:
                pass
        
        finally:
            # Add extra delay before accepting new triggers
            time.sleep(0.3)
            self.is_processing = False
            print("⏳ Ready for next trigger (cooldown: 2s)\n")
    
    def _safe_get_clipboard(self) -> str:
        """Safely get clipboard content"""
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"⚠️  Could not read clipboard: {e}")
            return ""
    
    def _call_ai(self, text: str) -> str:
        """
        Call AI service to process text.
        Falls back to mock response if service unavailable.
        """
        if MOCK_MODE:
            return self._mock_ai_response(text)
        
        try:
            # Call the existing AI engine service
            payload = {
                "api_version": "v1",
                "text": text,
                "app": "cross-app",
                "action": "rewrite",
                "context": {
                    "previous_text": "",
                    "user_style": "default"
                }
            }
            
            response = requests.post(AI_API_URL, json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("result_text", text)
            else:
                print(f"⚠️  AI service returned {response.status_code}, using mock")
                return self._mock_ai_response(text)
                
        except requests.exceptions.ConnectionError:
            print("⚠️  AI service not running. Using mock mode.")
            return self._mock_ai_response(text)
        except Exception as e:
            print(f"⚠️  AI call failed: {e}, using mock")
            return self._mock_ai_response(text)
    
    def _mock_ai_response(self, text: str) -> str:
        """
        Mock AI response for testing without backend.
        Simulates realistic AI improvements.
        """
        time.sleep(0.2)  # Simulate processing time
        
        # Handle empty text (no selection case)
        if not text or text.strip() == "":
            return "Please let me know how I can assist you."
        
        # Specific test cases
        if "schedule a meeting" in text.lower():
            return "Please let me know your availability next week."
        
        if "test" in text.lower():
            return "This is an AI-improved version of your text."
        
        # Generic improvements based on text characteristics
        if len(text) < 20:
            return f"{text.capitalize()} - enhanced by AI"
        
        # For longer text, add professional framing
        return f"Regarding your request: {text}\n\nI would like to proceed accordingly."
    
    def start(self):
        """Start the global hotkey listener"""
        print("=" * 60)
        print("🚀 Cross-Application AI Text Rewriter")
        print("=" * 60)
        print("\n📖 Instructions:")
        print("  1. Keep this terminal window OPEN")
        print("  2. Open your target app (Notepad, Word, VS Code, etc.)")
        print("  3. Select text (or place cursor for new text)")
        print("  4. Press Ctrl + Space")
        print(f"  5. You get {SWITCH_WINDOW_DELAY:.1f}s to click into your target app")
        print("  6. System will copy, AI-process, and paste automatically")
        print(f"\n⚠️  Note: {COOLDOWN_SECONDS}s cooldown between triggers (prevents loops)")
        print(f"⚠️  Important: After Ctrl+Space, SWITCH to target app within {SWITCH_WINDOW_DELAY:.1f}s!")
        print("\n⌨️  Hotkey: Ctrl + Space")
        print("🛑 Exit: Ctrl + Esc")
        print(f"🧠 Mode: {'MOCK (no backend needed)' if MOCK_MODE else 'LIVE AI Service'}")
        print("\n💡 Tip: Test in Notepad first - it's most reliable!")
        print("\n⏳ Listening for Ctrl+Space...\n")
        
        # Start keyboard listener
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as self.listener:
            self.listener.join()


def main():
    """Main entry point"""
    # Disable pyautogui failsafe for better UX
    pyautogui.FAILSAFE = False
    
    # Create and start rewriter
    rewriter = CrossAppAIRewriter()
    
    try:
        rewriter.start()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
