"""
Cross-App AI Rewriter - PYNPUT VERSION
Uses pynput for ALL keyboard operations (more reliable than pyautogui)
"""

import time
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Configuration
MOCK_MODE = True
COOLDOWN_SECONDS = 2.0
SWITCH_WINDOW_DELAY = 2.0  # Extra time to switch


class PynputAIRewriter:
    def __init__(self):
        self.kb = Controller()  # Keyboard controller for sending keys
        self.is_processing = False
        self.last_trigger = 0
        self.current_keys = set()
    
    def on_press(self, key):
        """Handle key press"""
        if self.is_processing:
            return
        
        self.current_keys.add(key)
        
        # Check for Ctrl+Space
        hotkey = {Key.ctrl_l, Key.space}
        if self.current_keys >= hotkey:
            elapsed = time.time() - self.last_trigger
            if elapsed < COOLDOWN_SECONDS:
                print(f"⏳ Wait {elapsed:.1f}s...")
                return
            
            print("\n" + "="*70)
            print("🔑 CTRL+SPACE DETECTED!")
            print("="*70)
            print("\n⚠️  SWITCH TO YOUR TARGET APP NOW!")
            print("    (Notepad, Word, browser, etc.)\n")
            
            self.last_trigger = time.time()
            self.current_keys.clear()
            
            # Countdown
            for i in range(int(SWITCH_WINDOW_DELAY), 0, -1):
                print(f"   ⏰ Starting in {i}s... (click into target app!)", end='\r')
                time.sleep(1)
            
            print("\n\n✅ Processing...\n")
            self.process()
    
    def on_release(self, key):
        """Handle key release"""
        self.current_keys.discard(key)
        
        if key == Key.esc and (Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys):
            print("\n👋 Exiting...")
            return False
    
    def send_ctrl_c(self):
        """Send Ctrl+C using pynput"""
        print("   📤 Sending Ctrl+C...")
        with self.kb.pressed(Key.ctrl):
            self.kb.press('c')
            time.sleep(0.05)
            self.kb.release('c')
        time.sleep(0.05)
    
    def send_ctrl_v(self):
        """Send Ctrl+V using pynput"""
        print("   📥 Sending Ctrl+V...")
        with self.kb.pressed(Key.ctrl):
            self.kb.press('v')
            time.sleep(0.05)
            self.kb.release('v')
        time.sleep(0.05)
    
    def process(self):
        """Main processing with pynput keyboard control"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        try:
            # Wait a bit more to ensure window has focus
            time.sleep(0.3)
            
            # Step 1: Save clipboard
            print("1️⃣  Saving original clipboard...")
            original_clip = pyperclip.paste()
            print(f"    ✅ Saved: '{original_clip[:40]}...'")
            
            # Step 2: Clear clipboard and copy
            print("\n2️⃣  Copying selected text...")
            pyperclip.copy("")
            time.sleep(0.1)
            
            self.send_ctrl_c()
            time.sleep(0.25)  # Wait for copy to complete
            
            copied = pyperclip.paste()
            if not copied:
                print("    ⚠️  No text selected - generating new text")
                copied = ""
            else:
                print(f"    ✅ Copied: '{copied[:40]}...'")
            
            # Step 3: AI processing
            print("\n3️⃣  Processing with AI...")
            ai_result = self.mock_ai(copied)
            print(f"    ✅ AI: '{ai_result[:40]}...'")
            
            # Step 4: Copy AI result to clipboard
            print("\n4️⃣  Copying AI result to clipboard...")
            pyperclip.copy(ai_result)
            time.sleep(0.2)
            
            # Verify
            verify = pyperclip.paste()
            if verify == ai_result:
                print("    ✅ Clipboard ready")
            else:
                print("    ⚠️  Retrying...")
                pyperclip.copy(ai_result)
                time.sleep(0.2)
            
            # Step 5: Paste using pynput
            print("\n5️⃣  Pasting AI result...")
            time.sleep(0.25)  # Extra delay before paste
            
            self.send_ctrl_v()
            
            print("    ✅ Paste command sent!")
            time.sleep(0.3)
            
            # Step 6: Restore clipboard
            print("\n6️⃣  Restoring original clipboard...")
            time.sleep(0.2)
            pyperclip.copy(original_clip)
            print("    ✅ Restored")
            
            print("\n" + "="*70)
            print("✅ ✅ ✅  COMPLETE! CHECK YOUR TARGET APP!")
            print("="*70)
            print()
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(0.5)
            self.is_processing = False
            print("⏳ Ready for next trigger\n")
    
    def mock_ai(self, text):
        """Mock AI"""
        time.sleep(0.15)
        if not text:
            return "AI generated text - ready to help!"
        if "schedule a meeting" in text.lower():
            return "Please let me know your availability next week."
        if "hello" in text.lower():
            return "Hello! How can I assist you today?"
        if len(text) < 20:
            return f"{text.capitalize()} - enhanced by AI"
        return f"Regarding your request: {text}"
    
    def start(self):
        """Start listener"""
        print("\n" + "="*70)
        print("🚀 Cross-App AI Rewriter - PYNPUT VERSION")
        print("="*70)
        print("\n📌 This version uses PYNPUT for keyboard control")
        print("   (More reliable than PyAutoGUI on some systems)")
        print()
        print("📖 HOW TO USE:")
        print("   1. Keep this window open")
        print("   2. Open Notepad (or Word, VS Code, etc.)")
        print("   3. In Notepad: type and select text")
        print("   4. Press Ctrl+Space (from anywhere)")
        print(f"   5. You get {SWITCH_WINDOW_DELAY:.0f} seconds to click into Notepad")
        print("   6. Watch your text transform!")
        print()
        print("⚡ QUICK TIP: Press Ctrl+Space WHILE IN NOTEPAD")
        print("   (Then you don't need to switch windows!)")
        print()
        print("⌨️  Hotkey: Ctrl + Space")
        print("🛑 Exit: Ctrl + Esc")
        print(f"⏱️  Cooldown: {COOLDOWN_SECONDS}s")
        print()
        print("🧪 Test in Notepad first - it's most reliable!")
        print("\n⏳ Listening for Ctrl+Space...\n")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    rewriter = PynputAIRewriter()
    try:
        rewriter.start()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
