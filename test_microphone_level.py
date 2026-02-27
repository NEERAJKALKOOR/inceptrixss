"""
Test microphone input levels to diagnose recording issues
"""
import pyaudio
import numpy as np
import time

def test_microphone():
    """Test microphone and show input levels"""
    audio = pyaudio.PyAudio()
    
    # List all audio devices
    print("\n🎤 Available Audio Devices:")
    print("="*60)
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:  # Input device
            print(f"{i}: {info['name']}")
            print(f"   Max Input Channels: {info['maxInputChannels']}")
            print(f"   Default Sample Rate: {info['defaultSampleRate']}")
            print()
    
    print("="*60)
    print("\n🔴 Recording for 3 seconds to test microphone levels...")
    print("🗣️  SPEAK NOW - Say something clearly into your microphone")
    print()
    
    # Record audio
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    frames = []
    max_amplitude = 0
    
    for i in range(0, int(16000 / 1024 * 3)):  # 3 seconds
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
        
        # Calculate amplitude
        audio_data = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_data).mean()
        max_amplitude = max(max_amplitude, amplitude)
        
        # Show live levels
        bars = int(amplitude / 100)
        if i % 5 == 0:  # Update every ~0.3 seconds
            print(f"📊 Level: {'█' * min(bars, 50)} {amplitude:.0f}")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    print(f"\n📊 Recording Statistics:")
    print(f"   Total frames: {len(frames)}")
    print(f"   Max amplitude: {max_amplitude:.0f}")
    print(f"   Audio data size: {sum(len(f) for f in frames)} bytes")
    
    # Analyze results
    if max_amplitude < 50:
        print("\n⚠️ WARNING: Very low input level!")
        print("   Your microphone might be:")
        print("   • Muted or volume too low")
        print("   • Wrong device selected")
        print("   • Too far away")
        print("\n💡 Fix:")
        print("   1. Right-click speaker icon in taskbar")
        print("   2. Click 'Sound settings'")
        print("   3. Go to 'Input' section")
        print("   4. Test your microphone and adjust volume")
    elif max_amplitude < 200:
        print("\n⚠️ Input level is low. Try speaking louder or closer to mic.")
    else:
        print("\n✅ Microphone input looks good!")
        print("   If Whisper still fails, try the 'base' model instead of 'medium'")

if __name__ == "__main__":
    test_microphone()
