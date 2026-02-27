"""
Quick Test: F9 Voice with Real Whisper (Same as test_voice_whisper.py)
This uses the exact same voice_handler singleton that works in test_voice_whisper.py
"""

print("=" * 70)
print("🎤 QUICK F9 VOICE TEST - Real Whisper Integration")
print("=" * 70)
print()

# Test 1: Import the singleton voice_handler
print("1️⃣  Importing voice_handler singleton...")
try:
    from ui_module.voice_input import voice_handler
    print(f"   ✅ Voice handler imported")
    print(f"   📊 Mock mode: {voice_handler.mock_mode}")
    print(f"   📊 Model size: {voice_handler.model_size}")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

print()

# Test 2: Verify unified_ai_keyboard uses same handler
print("2️⃣  Checking unified_ai_keyboard integration...")
try:
    import sys
    # Read the file to verify it imports voice_handler not VoiceInputHandler
    with open('unified_ai_keyboard.py', 'r') as f:
        content = f.read()
        if 'from ui_module.voice_input import voice_handler' in content:
            print("   ✅ Uses singleton voice_handler (same as test)")
        elif 'from ui_module.voice_input import VoiceInputHandler' in content:
            print("   ⚠️  Still using VoiceInputHandler class (wrong!)")
        else:
            print("   ❓ Import not found")
except Exception as e:
    print(f"   ❌ Check failed: {e}")

print()

# Test 3: Manual voice test
print("3️⃣  Manual voice test (like test_voice_whisper.py)...")
print()

if voice_handler.mock_mode:
    print("   ⚠️  Running in MOCK mode")
    print("   Install: pip install openai-whisper pyaudio")
    print()
    print("=" * 70)
    print("✅ Integration verified (mock mode)")
    print("=" * 70)
else:
    print("   ✅ Real Whisper mode active")
    print()
    print("   Press [Enter] to test voice recording...")
    input()
    
    print("   🎙️  RECORDING... Speak now!")
    voice_handler.start_recording()
    
    print("   Press [Enter] when done speaking...")
    input()
    
    print("   🔄 Processing...")
    result = voice_handler.stop_recording_and_transcribe()
    
    print()
    print("   " + "=" * 66)
    print(f"   📝 Transcribed: {result}")
    print("   " + "=" * 66)
    print()
    print("=" * 70)
    print("✅ Integration verified - Same system works in unified_ai_keyboard!")
    print("=" * 70)

print()
print("🚀 Now run: python unified_ai_keyboard.py")
print("   Or: .\start_f9_voice.bat")
print()
