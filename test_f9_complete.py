"""
Complete F9 Test - Real Whisper Integration
Tests the exact workflow: Select → F9 → Record → F9 → Replace
"""

print("=" * 70)
print("🎤 F9 VOICE REPLACEMENT TEST")
print("=" * 70)
print()
print("📋 INSTRUCTIONS:")
print()
print("   1. This will start the AI keyboard")
print("   2. Open Notepad (will auto-launch)")
print("   3. Type: 'original text'")
print("   4. SELECT the text")
print("   5. Press F9 → Recording starts 🔴")
print("   6. SPEAK clearly: 'hello world'")
print("   7. Press F9 → Stops, transcribes, REPLACES!")
print()
print("=" * 70)
print()
print("⚠️  IMPORTANT: Keep this console window visible to see logs!")
print()

import subprocess
import time

# Launch Notepad
print("🚀 Launching Notepad...")
subprocess.Popen(['notepad.exe'])
time.sleep(2)

print("✅ Notepad launched")
print()
print("Starting AI Keyboard in 3 seconds...")
time.sleep(3)

# Start the unified keyboard
from unified_ai_keyboard import AIKeyboardController

if __name__ == "__main__":
    controller = AIKeyboardController()
    try:
        controller.start()
    except KeyboardInterrupt:
        print("\n\n👋 Test complete!")
