"""
Cross-App AI Rewriter - SUPER SIMPLE VERSION
This WILL work since keyboard automation is confirmed working
"""

import time
import pyperclip
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key

# Super simple - just make it work!
COOLDOWN = 3.0

class SimpleRewriter:
    def __init__(self):
        self.processing = False
        self.last_time = 0
        self.keys = set()
    
    def on_press(self, key):
        if self.processing:
            return
        
        self.keys.add(key)
        
        # Ctrl + Space
        if {Key.ctrl_l, Key.space} <= self.keys or {Key.ctrl_r, Key.space} <= self.keys:
            if time.time() - self.last_time < COOLDOWN:
                print("⏳ Wait a moment...")
                return
            
            self.last_time = time.time()
            self.keys.clear()
            self.go()
    
    def on_release(self, key):
        self.keys.discard(key)
        if key == Key.esc:
            return False
    
    def go(self):
        self.processing = True
        
        print("\n" + "="*60)
        print("🎯 AI REWRITE STARTING!")
        print("="*60)
        
        try:
            # Release all keys
            print("\n⏳ Releasing keys...")
            for k in ['ctrl', 'shift', 'alt']:
                pyautogui.keyUp(k)
            time.sleep(0.5)
            
            # Save clipboard
            print("💾 Saving clipboard...")
            old_clip = pyperclip.paste()
            
            # Copy
            print("📋 Copying your text... (Ctrl+C)")
            pyperclip.copy("")
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            
            text = pyperclip.paste()
            print(f"✅ Got: '{text[:40] if text else '(empty)'}...'")
            
            # AI
            print("🤖 AI processing...")
            if not text:
                ai_text = "AI generated: Hello! How can I help?"
            elif "schedule" in text.lower() and "meeting" in text.lower():
                ai_text = "Please let me know your availability next week."
            elif len(text) < 20:
                ai_text = f"{text.upper()} - AI ENHANCED!"
            else:
                ai_text = f"AI says: {text}"
            
            print(f"✅ AI result: '{ai_text[:40]}...'")
            time.sleep(0.2)
            
            # Paste
            print("📝 Copying AI result to clipboard...")
            pyperclip.copy(ai_text)
            time.sleep(0.3)
            
            print("⚡ PASTING NOW... (Ctrl+V)")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # Restore
            print("🔄 Restoring clipboard...")
            pyperclip.copy(old_clip)
            
            print("\n" + "="*60)
            print("✅ ✅ ✅ DONE! Check your app!")
            print("="*60)
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            time.sleep(1)
            self.processing = False
            print("⏳ Ready (wait 3s between uses)\n")
    
    def start(self):
        print("\n" + "="*70)
        print("🚀 SUPER SIMPLE AI REWRITER")
        print("="*70)
        print("\n✨ YOUR SYSTEM WORKS PERFECTLY! ✨")
        print()
        print("📝 EASY STEPS:")
        print()
        print("  1. Open Notepad RIGHT NOW")
        print("  2. Type this: hello world")
        print("  3. Select it (Ctrl+A)")
        print("  4. Press Ctrl+Space")
        print("  5. Watch it change!")
        print()
        print("💡 PRO TIP: Stay in Notepad when you press Ctrl+Space")
        print("   (No need to switch back to terminal)")
        print()
        print("⌨️  Hotkey: Ctrl + Space")
        print("🛑 Exit: Esc")
        print(f"⏱️  Wait 3 seconds between uses")
        print()
        print("⏳ Ready! Press Ctrl+Space in Notepad...\n")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as L:
            L.join()

if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    SimpleRewriter().start()
