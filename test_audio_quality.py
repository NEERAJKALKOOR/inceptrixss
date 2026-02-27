"""
Check if recorded audio actually contains speech
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyaudio
import wave
import numpy as np
import time

def analyze_audio_file(filename):
    """Analyze a WAV file to see if it contains speech"""
    print(f"\n🔍 Analyzing {filename}...")
    
    # Read WAV file
    wf = wave.open(filename, 'rb')
    
    print(f"📊 WAV File Properties:")
    print(f"   Channels: {wf.getnchannels()}")
    print(f"   Sample width: {wf.getsampwidth()} bytes")
    print(f"   Sample rate: {wf.getframerate()} Hz")
    print(f"   Frames: {wf.getnframes()}")
    print(f"   Duration: {wf.getnframes() / wf.getframerate():.2f} seconds")
    
    # Read all audio data
    audio_data = wf.readframes(wf.getnframes())
    wf.close()
    
    # Convert to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Analyze amplitude
    mean_amplitude = np.abs(audio_array).mean()
    max_amplitude = np.abs(audio_array).max()
    
    print(f"\n📊 Audio Analysis:")
    print(f"   Mean amplitude: {mean_amplitude:.1f}")
    print(f"   Max amplitude: {max_amplitude}")
    print(f"   Min value: {audio_array.min()}")
    print(f"   Max value: {audio_array.max()}")
    
    # Check for silence
    if mean_amplitude < 10:
        print(f"\n⚠️ WARNING: Audio is mostly SILENT!")
        print(f"   This means your microphone isn't capturing sound properly.")
    elif mean_amplitude < 100:
        print(f"\n⚠️ WARNING: Audio level is VERY LOW")
        print(f"   Your speech might be too quiet to transcribe.")
    elif mean_amplitude < 500:
        print(f"\n✅ Audio level is okay but could be louder")
    else:
        print(f"\n✅ Audio level looks good!")
    
    # Check for variation (speech has variation, silence doesn't)
    std_dev = np.std(audio_array.astype(float))
    print(f"   Standard deviation: {std_dev:.1f}")
    
    if std_dev < 50:
        print(f"   ⚠️ Very little variation - likely silence or steady noise")
    else:
        print(f"   ✅ Good variation - likely contains speech")

def record_and_analyze():
    """Record audio and analyze it immediately"""
    print("🎤 Recording Audio Quality Test")
    print("="*60)
    
    audio = pyaudio.PyAudio()
    
    # Get default input device
    default_input = audio.get_default_input_device_info()
    print(f"\n🎤 Using microphone: {default_input['name']}")
    print(f"   Sample rate: {default_input['defaultSampleRate']}")
    
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    print(f"\n🔴 Recording for 5 seconds...")
    print(f"🗣️  SPEAK LOUDLY AND CLEARLY: 'Hello world this is a test'")
    print()
    
    frames = []
    for i in range(0, int(16000 / 1024 * 5)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
        
        # Show live feedback
        if i % 5 == 0:
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_data).mean()
            bars = int(amplitude / 100)
            print(f"📊 {'█' * min(bars, 50)} {amplitude:.0f}")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save to file
    filename = "test_quality.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    # Analyze the file
    analyze_audio_file(filename)
    
    print(f"\n💡 Play {filename} to hear what was recorded")
    print(f"   If you can't hear your voice clearly, that's the problem!")

if __name__ == "__main__":
    record_and_analyze()
