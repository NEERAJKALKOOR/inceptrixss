"""
Debug F9 Voice - Find why it's using mock
"""
import sys

print("=" * 70)
print("🔍 DEBUGGING F9 VOICE")
print("=" * 70)
print()

# Step 1: Check voice_handler directly
print("1️⃣ Checking voice_handler singleton...")
try:
    from ui_module.voice_input import voice_handler
    print(f"   ✅ Imported successfully")
    print(f"   • Mock mode: {voice_handler.mock_mode}")
    print(f"   • Model: {voice_handler.model_size}")
    print(f"   • Is recording: {voice_handler.is_recording}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()

# Step 2: Test a quick recording
print("2️⃣ Testing quick recording (5 seconds)...")
print()
print("   Press Enter to start recording...")
input()
print("   🎙️ RECORDING... Speak now!")

voice_handler.start_recording()
print(f"   Recording state: {voice_handler.is_recording}")

import time
time.sleep(5)

print("   🔄 Stopping and transcribing...")
result = voice_handler.stop_recording_and_transcribe()

print()
print("=" * 70)
print(f"📝 RESULT: {result}")
print("=" * 70)
print()

if result and not result.startswith("[") and "mock" not in result.lower():
    print("✅ Real transcription working!")
    print()
    print("Now checking unified_ai_keyboard.py logic...")
    print()
    
    # Step 3: Check the condition in unified_ai_keyboard
    VOICE_AVAILABLE = True
    condition_result = VOICE_AVAILABLE and voice_handler and not voice_handler.mock_mode
    
    print(f"3️⃣ Condition check: VOICE_AVAILABLE and voice_handler and not voice_handler.mock_mode")
    print(f"   • VOICE_AVAILABLE: {VOICE_AVAILABLE}")
    print(f"   • voice_handler exists: {voice_handler is not None}")
    print(f"   • voice_handler.mock_mode: {voice_handler.mock_mode}")
    print(f"   • Final result: {condition_result}")
    print()
    
    if condition_result:
        print("✅ Condition would trigger REAL transcription")
    else:
        print("❌ Condition fails - would use MOCK")
        print("   This is the bug!")
else:
    print("❌ Voice not working properly")
    print(f"   Got: {result}")

print()
print("=" * 70)
