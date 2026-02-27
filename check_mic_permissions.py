"""
Check Windows microphone permissions and test access
"""
import pyaudio
import sys

def check_mic_permissions():
    """Check if we can access microphone"""
    print("🔐 Checking Microphone Permissions...")
    print("="*60)
    
    try:
        audio = pyaudio.PyAudio()
        
        # Get default input device
        try:
            default_info = audio.get_default_input_device_info()
            print(f"\n✅ Default input device found:")
            print(f"   Name: {default_info['name']}")
            print(f"   Index: {default_info['index']}")
            print(f"   Channels: {default_info['maxInputChannels']}")
            print(f"   Sample Rate: {default_info['defaultSampleRate']}")
        except Exception as e:
            print(f"\n❌ Could not get default input device: {e}")
            print(f"\n💡 FIX: Windows may have blocked microphone access")
            print(f"   1. Press Win + I to open Settings")
            print(f"   2. Go to Privacy & Security > Microphone")
            print(f"   3. Enable 'Let apps access your microphone'")
            print(f"   4. Enable 'Let desktop apps access your microphone'")
            audio.terminate()
            return False
        
        # Try to open microphone stream
        print(f"\n🎤 Testing microphone access...")
        try:
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            
            # Read one frame to test
            data = stream.read(1024, exception_on_overflow=False)
            
            stream.stop_stream()
            stream.close()
            
            print(f"✅ Microphone access successful!")
            print(f"   Captured {len(data)} bytes of audio data")
            
        except Exception as e:
            print(f"\n❌ Could not access microphone: {e}")
            print(f"\n💡 POSSIBLE FIXES:")
            print(f"   1. Check if another app is using the microphone")
            print(f"   2. In Windows Settings > System > Sound:")
            print(f"      • Select correct input device")
            print(f"      • Set volume to 80-100%")
            print(f"      • Test microphone and speak - blue bar should move")
            print(f"   3. Try running Python as Administrator")
            audio.terminate()
            return False
        
        audio.terminate()
        
        print(f"\n" + "="*60)
        print(f"✅ ALL CHECKS PASSED - Microphone is accessible")
        print(f"="*60)
        
        print(f"\n💡 If Whisper still can't transcribe:")
        print(f"   • You may need to speak MUCH LOUDER")
        print(f"   • Try increasing Windows microphone volume to 100%")
        print(f"   • Test by playing back test_recording.wav file")
        
        return True
        
    except Exception as e:
        print(f"\n❌ PyAudio error: {e}")
        return False

if __name__ == "__main__":
    success = check_mic_permissions()
    sys.exit(0 if success else 1)
