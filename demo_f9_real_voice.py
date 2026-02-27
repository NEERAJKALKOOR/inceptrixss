"""
Real Voice Demo - Complete F9 Workflow Test
This demonstrates the full F9 voice selection replacement with real Whisper transcription
"""

import sys
import time

# Check dependencies first
print("=" * 70)
print("🔍 Checking dependencies...")
print("=" * 70)

try:
    import whisper
    import pyaudio
    import PyQt5
    print("✅ All dependencies available!")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nPlease install:")
    print("   pip install -r requirements_ui.txt")
    sys.exit(1)

print()
print("=" * 70)
print("🎤 F9 VOICE SELECTION REPLACEMENT - REAL WHISPER")
print("=" * 70)
print()
print("📋 DEMO WORKFLOW:")
print()
print("   Step 1: Open Notepad (notepad.exe)")
print("   Step 2: Type some text: 'original text here'")
print("   Step 3: Select the text you just typed")
print("   Step 4: Press F9 🔴")
print("   Step 5: SPEAK CLEARLY into your microphone")
print("           Example: 'this is my voice replacing the text'")
print("   Step 6: Press F9 again")
print("   Step 7: Watch the magic! Your voice text replaces the selection")
print()
print("=" * 70)
print()
print("💡 TIPS:")
print("   • Speak clearly and at normal pace")
print("   • Use a quiet environment for best results")
print("   • First time: Whisper will download model (~140MB)")
print("   • After that, it's instant and 100% offline!")
print()
print("=" * 70)
print()

# Launch Notepad for easy testing
print("🚀 Launching Notepad for testing...")
import subprocess
subprocess.Popen(['notepad.exe'])
time.sleep(2)

print()
print("Starting AI Keyboard with real voice in 3 seconds...")
print("Keep this console open to see transcription results!")
print()
time.sleep(3)

# Import and run the unified keyboard
from unified_ai_keyboard import AIKeyboardController

if __name__ == "__main__":
    controller = AIKeyboardController()
    try:
        print("\n🚀 System starting...\n")
        controller.start()
    except KeyboardInterrupt:
        print("\n\n👋 Demo complete! Goodbye!")
