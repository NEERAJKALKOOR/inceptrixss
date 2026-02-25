"""
Quick test of Whisper voice transcription
"""
import sys
sys.path.insert(0, '.')

from ui_module.interface import UIController

def test_whisper():
    print("🎤 Testing Whisper Voice Module")
    print("=" * 60)
    
    # Initialize UI with mock mode off
    ui = UIController(mock_mode=False)
    
    print("\n✅ UI Module initialized with Whisper")
    print(f"Voice handler mock mode: {ui.voice_handler.mock_mode}")
    
    if not ui.voice_handler.mock_mode:
        print("\n🔄 Whisper is available and will be used for voice transcription")
        print("📝 The 'base' model (~140MB) will download on first voice capture")
    else:
        print("\n⚠️ Running in mock mode - install requirements:")
        print("   pip install openai-whisper pyaudio numpy")
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")

if __name__ == "__main__":
    test_whisper()
