"""
Test voice recording and save the audio file to check quality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui_module.voice_input import voice_handler
import time

def test_recording_and_save():
    """Record audio, transcribe, and save the WAV file for inspection"""
    print("🎤 Voice Recording Test with Audio File Save")
    print("="*60)
    print("\n🔴 Recording will start in 2 seconds...")
    print("🗣️  Get ready to speak clearly...")
    time.sleep(2)
    
    print("\n🔴 RECORDING NOW - Say: 'Hello this is a test'")
    voice_handler.start_recording()
    
    # Record for 5 seconds
    time.sleep(5)
    
    print("\n🔴 Stopping and transcribing...")
    
    # Temporarily modify the transcribe function to save the file
    import wave
    import tempfile
    
    # Stop recording manually to get audio frames
    voice_handler.is_recording = False
    
    if hasattr(voice_handler, 'recording_thread'):
        voice_handler.recording_thread.join(timeout=1.0)
    
    # Stop stream
    if voice_handler.stream:
        voice_handler.stream.stop_stream()
        voice_handler.stream.close()
    if voice_handler.audio:
        sample_width = voice_handler.audio.get_sample_size(voice_handler.format)
        voice_handler.audio.terminate()
    else:
        sample_width = 2
    
    # Save to permanent file instead of temp
    audio_file = "test_recording.wav"
    
    print(f"\n📝 Saving audio to {audio_file}...")
    wf = wave.open(audio_file, 'wb')
    wf.setnchannels(voice_handler.channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(voice_handler.rate)
    wf.writeframes(b''.join(voice_handler.audio_frames))
    wf.close()
    
    # Check file info
    file_size = os.path.getsize(audio_file)
    duration = len(voice_handler.audio_frames) * voice_handler.chunk / voice_handler.rate
    
    print(f"📊 Audio file saved!")
    print(f"   File: {audio_file}")
    print(f"   Size: {file_size} bytes")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Sample rate: {voice_handler.rate} Hz")
    print(f"   Channels: {voice_handler.channels}")
    
    # Now transcribe
    print(f"\n🔄 Transcribing with Whisper...")
    transcribed = voice_handler._transcribe_audio(audio_file)
    
    print(f"\n✅ RESULT: '{transcribed}'")
    print(f"\n💡 You can play {audio_file} in media player to check audio quality")

if __name__ == "__main__":
    test_recording_and_save()
