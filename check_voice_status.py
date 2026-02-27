"""
Quick Status Check - Verify voice_handler is ready
"""

print("=" * 70)
print("🔍 VOICE HANDLER STATUS CHECK")
print("=" * 70)
print()

try:
    from ui_module.voice_input import voice_handler
    
    print("✅ voice_handler imported successfully")
    print()
    print("📊 Current Status:")
    print(f"   • Mock mode: {voice_handler.mock_mode}")
    print(f"   • Model size: {voice_handler.model_size}")
    print(f"   • Model loaded: {voice_handler.model is not None}")
    
    # Show model info
    model_info = {
        'tiny': '39MB - Fastest (lower accuracy)',
        'base': '140MB - Good balance',
        'small': '470MB - Better accuracy ⭐',
        'medium': '1.5GB - High accuracy',
        'large': '3GB - Best accuracy'
    }
    if voice_handler.model_size in model_info:
        print(f"   📦 Model info: {model_info[voice_handler.model_size]}")
    print()
    
    if voice_handler.mock_mode:
        print("⚠️  STATUS: MOCK MODE")
        print("   Voice will NOT record from microphone")
        print("   Will return fake transcription text")
        print()
        print("   To enable real voice:")
        print("   - Install: pip install openai-whisper pyaudio")
        print("   - Install ffmpeg on your system")
    else:
        print("✅ STATUS: REAL WHISPER MODE")
        print("   Voice WILL record from microphone")
        print("   Voice WILL transcribe with Whisper AI")
        print("   Ready for F9 workflow!")
        
    print()
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
