"""
Quick test of keyboard layer without full integration
"""
import sys
sys.path.insert(0, '.')

from keyboard_layer.keyboard_hook import keyboard_monitor
from keyboard_layer.text_manager import text_manager
import time


def test_keyboard():
    print("=" * 60)
    print("KEYBOARD LAYER TEST")
    print("=" * 60)
    
    # Test window detection
    window, app = text_manager.get_active_window_info()
    print(f"\n📱 Active app: {app}")
    print(f"🪟 Active window: {window}")
    print(f"📝 Is text editor: {text_manager.is_text_editor()}")
    
    # Set up callbacks
    def on_action(text):
        print(f"\n🎯 ACTION KEY! Context: '{text}'")
    
    def on_voice():
        print(f"\n🎤 VOICE KEY!")
    
    def on_accept():
        print(f"\n✅ ACCEPT KEY!")
    
    def on_reject():
        print(f"\n❌ REJECT KEY!")
    
    def on_text(text):
        print(f"\n📝 TEXT CHANGE: '{text}'")
    
    keyboard_monitor.on_action_key = on_action
    keyboard_monitor.on_voice_key = on_voice
    keyboard_monitor.on_accept_key = on_accept
    keyboard_monitor.on_reject_key = on_reject
    keyboard_monitor.on_text_change = on_text
    
    # Start monitoring
    keyboard_monitor.start()
    
    print("\n" + "=" * 60)
    print("HOTKEYS TO TEST:")
    print("  Ctrl+Space  - Action key")
    print("  Ctrl+Shift+V - Voice key")
    print("  Tab - Accept")
    print("  Esc - Reject")
    print("\nType some text and wait 0.5s for auto-trigger")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
        keyboard_monitor.stop()
        print("✅ Test complete!")


if __name__ == "__main__":
    test_keyboard()
