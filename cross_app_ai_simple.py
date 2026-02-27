"""
Simplified Cross-Application AI Text Rewriter
Ultra-conservative version with maximum loop prevention

This version has:
- Longer cooldown (3 seconds)
- More aggressive key release
- Extra delays between operations
- Visual countdown feedback
"""

import time
import pyperclip
import pyautogui
import threading
from pynput import keyboard
from pynput.keyboard import Key

# Configuration
MOCK_MODE = True
COOLDOWN_SECONDS = 3.0  # Longer cooldown for safety
COPY_DELAY = 0.25
PASTE_DELAY = 0.15


class SimpleAIRewriter:
    def __init__(self):
        self.is_processing = False
        self.last_trigger = 0
        self.ctrl_pressed = False
        self.space_pressed = False
        
    def on_press(self, key):
        """Simplified key tracking - only monitor Ctrl and Space separately"""
        if self.is_processing:
            return  # Ignore ALL keys during processing
        
        if key == Key.ctrl_l or key == Key.ctrl_r:
            self.ctrl_pressed = True
        elif key == Key.space and self.ctrl_pressed:
            # Cooldown check
            elapsed = time.time() - self.last_trigger
            if elapsed < COOLDOWN_SECONDS:
                remaining = COOLDOWN_SECONDS - elapsed
                print(f"⏳ Please wait {remaining:.1f}s...")
                return
            
            print("\n" + "="*50)
            print("🔑 HOTKEY DETECTED - Starting AI rewrite...")
            print("="*50)
            
            # Update timestamp FIRST
            self.last_trigger = time.time()
            
            # Start processing in thread to avoid blocking listener
            threading.Thread(target=self.process, daemon=True).start()
    
    def on_release(self, key):
        """Track key releases"""
        if key == Key.ctrl_l or key == Key.ctrl_r:
            self.ctrl_pressed = False
        elif key == Key.space:
            self.space_pressed = False
        
        # Exit on Esc
        if key == Key.esc and self.ctrl_pressed:
            print("\n👋 Exiting...")
            return False
    
    def process(self):
        """Process text with maximum safety"""
        if self.is_processing:
            print("⚠️  Already processing, ignoring trigger")
            return
        
        self.is_processing = True
        print("🔒 Processing locked")
        
        try:
            # STEP 1: Release ALL modifier keys
            print("\n1️⃣  Releasing modifier keys...")
            for key in ['ctrl', 'shift', 'alt', 'win', 'cmd']:
                try:
                    pyautogui.keyUp(key)
                except:
                    pass
            time.sleep(0.3)
            
            # STEP 2: Save clipboard
            print("2️⃣  Saving clipboard...")
            original_clip = pyperclip.paste()
            
            # STEP 3: Copy selected text
            print("3️⃣  Copying selected text (Ctrl+C)...")
            pyperclip.copy("")
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(COPY_DELAY)
            
            copied = pyperclip.paste()
            if not copied:
                copied = ""
                print("   ⚠️  No text selected")
            else:
                print(f"   ✅ Got: '{copied[:40]}...'")
            
            # STEP 4: Call AI
            print("4️⃣  Processing with AI...")
            ai_result = self.mock_ai(copied)
            print(f"   ✅ Result: '{ai_result[:40]}...'")
            
            # STEP 5: Copy AI result
            print("5️⃣  Preparing to paste...")
            pyperclip.copy(ai_result)
            time.sleep(0.2)  # Longer delay for clipboard
            
            # Verify clipboard
            verify = pyperclip.paste()
            if verify == ai_result:
                print("   ✅ Clipboard ready")
            else:
                print("   ⚠️  Retrying clipboard copy...")
                pyperclip.copy(ai_result)
                time.sleep(0.15)
            
            # STEP 6: Paste using press/release
            print("6️⃣  Pasting (Ctrl+V)...")
            time.sleep(0.2)  # Extra safety delay
            
            # More reliable paste method
            pyautogui.keyDown('ctrl')
            time.sleep(0.05)
            pyautogui.press('v')
            time.sleep(0.05)
            pyautogui.keyUp('ctrl')
            
            print("   ✅ Paste executed")
            time.sleep(0.3)  # Wait after paste
            
            # STEP 7: Restore clipboard
            print("7️⃣  Restoring clipboard...")
            time.sleep(0.15)
            pyperclip.copy(original_clip)
            
            print("\n✅ COMPLETE!")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
        finally:
            # Extra delay before unlocking
            time.sleep(0.5)
            self.is_processing = False
            print("🔓 Ready for next trigger\n")
    
    def mock_ai(self, text):
        """Mock AI response"""
        time.sleep(0.2)
        if not text:
            return "Please let me know how I can assist you."
        if "schedule a meeting" in text.lower():
            return "Please let me know your availability next week."
        if len(text) < 20:
            return f"{text.capitalize()} - enhanced by AI"
        return f"Regarding: {text}"
    
    def start(self):
        """Start listener"""
        print("\n" + "="*60)
        print("🚀 SIMPLE Cross-App AI Rewriter")
        print("   (Extra loop protection)")
        print("="*60)
        print("\n📖 How to use:")
        print("   1. Select text anywhere")
        print("   2. Press Ctrl+Space")
        print("   3. Wait for completion")
        print(f"\n⚠️  {COOLDOWN_SECONDS}s cooldown between triggers")
        print("🛑 Exit: Ctrl+Esc")
        print("\n⏳ Ready...\n")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    rewriter = SimpleAIRewriter()
    try:
        rewriter.start()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
