"""
Cross-Application AI Text Rewriter - WORKING VERSION
Gives user time to switch to target application after hotkey press
"""

import time
import pyperclip
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key
import winsound  # For beep notification

# Configuration
MOCK_MODE = True
COOLDOWN_SECONDS = 2.0
COPY_DELAY = 0.25
PASTE_DELAY = 0.15
SWITCH_WINDOW_DELAY = 1.0  # Time to switch to target app

class WorkingAIRewriter:
    def __init__(self):
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
            # Cooldown check
            elapsed = time.time() - self.last_trigger
            if elapsed < COOLDOWN_SECONDS:
                remaining = COOLDOWN_SECONDS - elapsed
                print(f"⏳ Cooldown active: {remaining:.1f}s remaining")
                return
            
            print("\n" + "="*60)
            print("🔑 Ctrl+Space DETECTED!")
            print("="*60)
            
            # Beep to confirm detection
            try:
                winsound.Beep(1000, 100)  # 1000Hz for 100ms
            except:
                pass
            
            self.last_trigger = time.time()
            self.current_keys.clear()
            
            # Important: Tell user to switch windows
            print("\n⚠️  SWITCH TO YOUR TARGET APP NOW!")
            print("    (Notepad, Word, Browser, etc.)")
            print()
            
            # Countdown
            for i in range(int(SWITCH_WINDOW_DELAY), 0, -1):
                print(f"   Starting in {i}s...", end='\r')
                time.sleep(1)
            
            print("\n✅ Processing now...\n")
            self.process()
    
    def on_release(self, key):
        """Handle key release"""
        self.current_keys.discard(key)
        
        if key == Key.esc and Key.ctrl in self.current_keys:
            print("\n👋 Exiting...")
            return False
    
    def process(self):
        """Process text with proper window focus"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        try:
            # Step 1: Release modifier keys
            print("1️⃣  Releasing modifier keys...")
            for key in ['ctrl', 'shift', 'alt', 'win']:
                try:
                    pyautogui.keyUp(key)
                except:
                    pass
            time.sleep(0.3)
            
            # Step 2: Save clipboard
            print("2️⃣  Saving clipboard...")
            original_clip = pyperclip.paste()
            
            # Step 3: Copy selected text
            print("3️⃣  Copying selected text (Ctrl+C)...")
            pyperclip.copy("")
            time.sleep(0.1)
            
            # Use press/release for better reliability
            pyautogui.keyDown('ctrl')
            time.sleep(0.05)
            pyautogui.press('c')
            time.sleep(0.05)
            pyautogui.keyUp('ctrl')
            
            time.sleep(COPY_DELAY)
            
            copied = pyperclip.paste()
            if not copied:
                print("   ⚠️  No text selected - AI will generate fresh text")
                copied = ""
            else:
                print(f"   ✅ Copied: '{copied[:40]}...'")
            
            # Step 4: Call AI
            print("4️⃣  Processing with AI...")
            ai_result = self.mock_ai(copied)
            print(f"   ✅ Result: '{ai_result[:40]}...'")
            
            # Step 5: Copy AI result
            print("5️⃣  Copying AI result to clipboard...")
            pyperclip.copy(ai_result)
            time.sleep(0.2)
            
            # Verify clipboard
            verify = pyperclip.paste()
            if verify != ai_result:
                print("   ⚠️  Retrying clipboard copy...")
                pyperclip.copy(ai_result)
                time.sleep(0.15)
            else:
                print("   ✅ Clipboard ready")
            
            # Step 6: Paste using press/release (more reliable)
            print("6️⃣  Pasting (Ctrl+V)...")
            time.sleep(0.2)
            
            pyautogui.keyDown('ctrl')
            time.sleep(0.05)
            pyautogui.press('v')
            time.sleep(0.05)
            pyautogui.keyUp('ctrl')
            
            print("   ✅ Paste executed!")
            time.sleep(0.3)
            
            # Step 7: Restore clipboard
            print("7️⃣  Restoring original clipboard...")
            time.sleep(0.2)
            pyperclip.copy(original_clip)
            
            print("\n✅ COMPLETE! Check your target app.")
            print("="*60 + "\n")
            
            # Success beep
            try:
                winsound.Beep(1500, 100)
            except:
                pass
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            time.sleep(0.5)
            self.is_processing = False
    
    def mock_ai(self, text):
        """Mock AI response"""
        time.sleep(0.15)
        if not text:
            return "Please let me know how I can assist you."
        if "schedule a meeting" in text.lower():
            return "Please let me know your availability next week."
        if len(text) < 20:
            return f"{text.capitalize()} - enhanced by AI"
        return f"Regarding your request: {text}"
    
    def start(self):
        """Start listener"""
        print("\n" + "="*70)
        print("🚀 Cross-App AI Rewriter - WORKING VERSION")
        print("="*70)
        print("\n📖 How to use:")
        print("   1. Keep this terminal window open")
        print("   2. Open your target app (Notepad, Word, etc.)")
        print("   3. Select text (or place cursor)")
        print("   4. Press Ctrl+Space")
        print("   5. You have 1 second to switch to target app")
        print("   6. System will copy, process, and paste automatically")
        print()
        print(f"⚠️  Important: After pressing Ctrl+Space, you get {SWITCH_WINDOW_DELAY:.0f}s")
        print("    to click into your target application!")
        print()
        print("⌨️  Hotkey: Ctrl+Space")
        print("🛑 Exit: Ctrl+Esc")
        print(f"⏱️  Cooldown: {COOLDOWN_SECONDS}s between triggers")
        print("\n🔊 Listen for beeps:")
        print("   - Short beep = Hotkey detected")
        print("   - Higher beep = Operation complete")
        print("\n⏳ Ready and listening...\n")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    rewriter = WorkingAIRewriter()
    try:
        rewriter.start()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
