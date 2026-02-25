"""
Fix for Browser & Word Compatibility
Tests text insertion in different apps
"""
import sys
sys.path.insert(0, '.')

import time
import pyautogui
from keyboard_layer.text_manager import text_manager

def test_insertion():
    print("=" * 60)
    print("BROWSER & WORD COMPATIBILITY TEST")
    print("=" * 60)
    
    # Get active app
    window, app = text_manager.get_active_window_info()
    print(f"\n📱 Active app: {app}")
    print(f"🪟 Active window: {window}")
    
    # Check typing mode
    needs_typing = text_manager._needs_typing_mode()
    print(f"🔤 Using typing mode: {needs_typing}")
    
    print("\n" + "=" * 60)
    print("INSTRUCTIONS:")
    print("1. Click in a text field (browser, Word, etc.)")
    print("2. Wait 3 seconds...")
    print("=" * 60)
    
    # Wait for user to click
    for i in range(3, 0, -1):
        print(f"\rInserting in {i}...", end="")
        time.sleep(1)
    
    print("\n\n🔄 Inserting test text...")
    
    test_text = "This is a test from AI Keyboard! It works in browsers and Word."
    text_manager.insert_text(test_text)
    
    print("✅ Text inserted!")
    print("\nIf you see the text in your app, it's working!")
    print("If not, try running as Administrator:")
    print("  Right-click PowerShell → Run as Administrator")
    print("  Then run: python run_ai_keyboard.py")

if __name__ == "__main__":
    test_insertion()
