"""
Test F9 Voice Selection Replacement
Quick test to verify the new F9 → Voice → Replace workflow
"""

print("="*70)
print("🎤 Testing F9 Voice Selection Replacement")
print("="*70)
print()
print("📝 INSTRUCTIONS:")
print("   1. Open Notepad or any text editor")
print("   2. Type some text: 'Replace this text'")
print("   3. Select the text with your mouse or keyboard")
print("   4. Press F9 - You'll hear/see 'Recording started'")
print("   5. Press F9 again - It will transcribe (mock mode)")
print("   6. The transcribed text will REPLACE your selection!")
print()
print("="*70)
print()
print("Starting unified AI keyboard in 3 seconds...")
print("Keep this console open to see the logs.")
print()

import time
time.sleep(3)

# Import and run the unified keyboard
from unified_ai_keyboard import AIKeyboardController

if __name__ == "__main__":
    controller = AIKeyboardController()
    try:
        print("\n🚀 System starting...\n")
        controller.start()
    except KeyboardInterrupt:
        print("\n\n👋 Test complete! Goodbye!")
