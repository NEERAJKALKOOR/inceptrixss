"""
Cross-App AI Rewriter - DEBUG VERSION
Shows detailed output at every step to diagnose paste issues
"""

import time
import pyperclip
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key

# Configuration
MOCK_MODE = True
COOLDOWN_SECONDS = 2.0
DEBUG = True  # Extra verbose output

class DebugAIRewriter:
    def __init__(self):
        self.is_processing = False
        self.last_trigger = 0
        self.current_keys = set()
    
    def log(self, msg, prefix="ℹ️"):
        """Debug logging with timestamp"""
        if DEBUG:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] {prefix} {msg}")
    
    def on_press(self, key):
        """Handle key press"""
        if self.is_processing:
            return
        
        self.current_keys.add(key)
        
        # Check for Ctrl+Space
        hotkey = {Key.ctrl_l, Key.space}
        if self.current_keys >= hotkey:
            # Cooldown check
            elapsed = time.time() - self.last_trigger
            if elapsed < COOLDOWN_SECONDS:
                self.log(f"Cooldown active: {elapsed:.1f}s elapsed", "⏳")
                return
            
            self.log("HOTKEY DETECTED - Ctrl+Space", "🔑")
            self.last_trigger = time.time()
            self.current_keys.clear()
            self.process()
    
    def on_release(self, key):
        """Handle key release"""
        self.current_keys.discard(key)
        
        if key == Key.esc and Key.ctrl in self.current_keys:
            self.log("Exit requested", "👋")
            return False
    
    def process(self):
        """Process text with detailed debugging"""
        if self.is_processing:
            self.log("Already processing, skipping", "⚠️")
            return
        
        self.is_processing = True
        self.log("Processing STARTED", "🚀")
        
        try:
            # Step 1: Release modifier keys
            self.log("Releasing modifier keys...", "🔓")
            for key in ['ctrl', 'shift', 'alt', 'win']:
                try:
                    pyautogui.keyUp(key)
                except Exception as e:
                    self.log(f"KeyUp {key} failed: {e}", "⚠️")
            time.sleep(0.25)
            self.log("Modifier keys released", "✅")
            
            # Step 2: Save clipboard
            self.log("Reading original clipboard...", "📋")
            original_clip = pyperclip.paste()
            self.log(f"Original: '{original_clip[:40]}...'", "📋")
            
            # Step 3: Clear and copy
            self.log("Clearing clipboard...", "🗑️")
            pyperclip.copy("")
            time.sleep(0.1)
            
            self.log("Simulating Ctrl+C...", "📤")
            pyautogui.hotkey('ctrl', 'c')
            self.log("Ctrl+C sent, waiting 0.25s...", "⏱️")
            time.sleep(0.25)
            
            # Step 4: Read copied text
            self.log("Reading clipboard after copy...", "📖")
            copied_text = pyperclip.paste()
            if not copied_text:
                self.log("No text selected (empty clipboard)", "⚠️")
                copied_text = ""
            else:
                self.log(f"Copied: '{copied_text[:40]}...'", "✅")
            
            # Step 5: AI processing
            self.log("Calling AI...", "🧠")
            ai_result = self.mock_ai(copied_text)
            self.log(f"AI result: '{ai_result[:40]}...'", "✅")
            
            # Step 6: Copy AI result
            self.log("Copying AI result to clipboard...", "📝")
            pyperclip.copy(ai_result)
            time.sleep(0.15)
            
            # Verify
            verify = pyperclip.paste()
            if verify == ai_result:
                self.log("Clipboard verification: PASS", "✅")
            else:
                self.log(f"Clipboard verification: FAIL", "❌")
                self.log(f"Expected: '{ai_result[:30]}'", "❌")
                self.log(f"Got: '{verify[:30]}'", "❌")
                self.log("Retrying copy...", "🔄")
                pyperclip.copy(ai_result)
                time.sleep(0.15)
            
            # Step 7: Paste with detailed logging
            self.log("Preparing to paste...", "📥")
            time.sleep(0.2)
            
            self.log("METHOD 1: Using hotkey('ctrl', 'v')", "🎮")
            pyautogui.hotkey('ctrl', 'v')
            self.log("Hotkey command sent", "✅")
            time.sleep(0.3)
            
            # Step 8: Restore clipboard
            self.log("Restoring original clipboard...", "🔄")
            time.sleep(0.15)
            pyperclip.copy(original_clip)
            time.sleep(0.1)
            
            final_clip = pyperclip.paste()
            if final_clip == original_clip:
                self.log("Clipboard restore: PASS", "✅")
            else:
                self.log("Clipboard restore: PARTIAL", "⚠️")
            
            self.log("Processing COMPLETE", "🎉")
            print()
            
        except Exception as e:
            self.log(f"ERROR: {e}", "❌")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(0.3)
            self.is_processing = False
            self.log("Ready for next trigger", "✅")
            print()
    
    def mock_ai(self, text):
        """Mock AI"""
        time.sleep(0.1)
        if not text:
            return "Please let me know how I can assist you."
        if "schedule a meeting" in text.lower():
            return "Please let me know your availability next week."
        if len(text) < 20:
            return f"{text.capitalize()} - enhanced by AI"
        return f"Regarding: {text}"
    
    def start(self):
        """Start listener"""
        print("\n" + "=" * 70)
        print("🐛 Cross-App AI Rewriter - DEBUG MODE")
        print("=" * 70)
        print("\n📝 This version shows DETAILED output for every step")
        print("\n⌨️  Hotkey: Ctrl+Space")
        print("🛑 Exit: Ctrl+Esc")
        print(f"⏱️  Cooldown: {COOLDOWN_SECONDS}s between triggers")
        print("\n⏳ Listening...\n")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    rewriter = DebugAIRewriter()
    try:
        rewriter.start()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
