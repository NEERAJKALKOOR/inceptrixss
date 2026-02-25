"""
Interactive Voice Test with Whisper
Press Enter to record, speak, then press Enter again to transcribe
"""
import sys
sys.path.insert(0, '.')

from ui_module.voice_input import voice_handler
import time

def test_voice_recording():
    print("=" * 60)
    print("🎤 WHISPER VOICE TEST")
    print("=" * 60)
    
    if voice_handler.mock_mode:
        print("\n⚠️ Running in MOCK mode")
        print("Missing dependencies. Install with:")
        print("   pip install openai-whisper pyaudio numpy")
        print("\nNote: Also requires ffmpeg on your system")
        return
    
    print("\n✅ Whisper is ready!")
    print(f"📊 Using model: {voice_handler.model_size}")
    print("\n" + "=" * 60)
    
    while True:
        print("\n📝 Press [Enter] to start recording...")
        input()
        
        print("🎙️  RECORDING... Speak now!")
        voice_handler.start_recording()
        
        print("Press [Enter] when done speaking...")
        input()
        
        print("🔄 Processing... (first time will download model)")
        result = voice_handler.stop_recording_and_transcribe()
        
        print("\n" + "=" * 60)
        print(f"📝 Transcribed: {result}")
        print("=" * 60)
        
        print("\nTest again? [Enter] = Yes, [q] = Quit")
        choice = input().strip().lower()
        if choice == 'q':
            break
    
    print("\n✅ Voice test complete!")

if __name__ == "__main__":
    try:
        test_voice_recording()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled")
