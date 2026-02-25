"""
Simple hotkey detection test
Press Ctrl+Alt+K to test if detection works
"""
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

current_keys = set()

def on_press(key):
    current_keys.add(key)
    
    # Check for Ctrl+Alt+K
    has_ctrl = Key.ctrl_l in current_keys or Key.ctrl_r in current_keys
    has_alt = Key.alt_l in current_keys or Key.alt_r in current_keys or Key.alt_gr in current_keys
    has_k = KeyCode.from_char('k') in current_keys or KeyCode.from_char('K') in current_keys
    
    if has_ctrl and has_alt and has_k:
        print("\n🎯 DETECTED: Ctrl+Alt+K pressed!")
        print(f"Current keys: {current_keys}")
    
def on_release(key):
    try:
        current_keys.discard(key)
    except:
        pass
    
    if key == Key.esc:
        return False

print("=" * 60)
print("HOTKEY DETECTION TEST")
print("=" * 60)
print("\nPress Ctrl+Alt+K to test detection")
print("Press Esc to quit")
print("\nCurrent keys pressed will be shown:")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("\nTest complete!")
