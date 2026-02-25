"""
Voice Input Module - Push-to-talk with offline speech-to-text
Captures microphone input and converts to text for AI refinement
"""
import pyaudio
import wave
import threading
import tempfile
import os
from typing import Callable, Optional
from ui_module.config import SAMPLE_RATE, VOICE_ENABLED

# Try to import speech recognition (offline capable)
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ speech_recognition not installed. Voice input will use mock mode.")


class VoiceInputHandler:
    """
    Handles push-to-talk voice input with offline speech-to-text.
    Non-blocking, does not interfere with typing.
    """
    
    def __init__(self, mock_mode: bool = not VOICE_ENABLED):
        self.mock_mode = mock_mode or not SPEECH_RECOGNITION_AVAILABLE
        self.is_recording = False
        self.audio_frames = []
        self.recognizer = sr.Recognizer() if SPEECH_RECOGNITION_AVAILABLE else None
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = SAMPLE_RATE
        
        self.audio = None
        self.stream = None
        
    def start_recording(self):
        """Start capturing microphone input (push-to-talk pressed)"""
        if self.mock_mode:
            print("🎤 [MOCK] Voice recording started...")
            self.is_recording = True
            return
        
        if self.is_recording:
            return  # Already recording
        
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.is_recording = True
            self.audio_frames = []
            
            # Start recording in background thread
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print("🎤 Voice recording started...")
            
        except Exception as e:
            print(f"❌ Error starting voice recording: {e}")
            self.is_recording = False
    
    def _record_audio(self):
        """Background thread to record audio"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.audio_frames.append(data)
            except Exception as e:
                print(f"❌ Error recording audio: {e}")
                break
    
    def stop_recording_and_transcribe(self, callback: Optional[Callable[[str], None]] = None) -> str:
        """
        Stop recording and convert speech to text.
        
        Args:
            callback: Optional callback function to receive transcribed text
            
        Returns:
            Transcribed text
        """
        if self.mock_mode:
            self.is_recording = False
            mock_text = "This is a mock voice transcription for testing"
            print(f"🎤 [MOCK] Voice transcribed: '{mock_text}'")
            if callback:
                callback(mock_text)
            return mock_text
        
        if not self.is_recording:
            return ""
        
        self.is_recording = False
        
        # Wait for recording thread to finish
        if hasattr(self, 'recording_thread'):
            self.recording_thread.join(timeout=1.0)
        
        # Stop stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        
        # Save audio to temporary file
        temp_wav = tempfile.mktemp(suffix=".wav")
        
        try:
            # Write audio to WAV file
            wf = wave.open(temp_wav, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format) if self.audio else 2)
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.audio_frames))
            wf.close()
            
            # Transcribe using speech recognition (offline)
            transcribed_text = self._transcribe_audio(temp_wav)
            
            print(f"🎤 Voice transcribed: '{transcribed_text}'")
            
            # Cleanup
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            
            if callback:
                callback(transcribed_text)
            
            return transcribed_text
            
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            return ""
    
    def _transcribe_audio(self, audio_file: str) -> str:
        """
        Transcribe audio file to text using offline speech recognition.
        Falls back to Sphinx (offline) if available.
        """
        if not self.recognizer:
            return "[Speech recognition not available]"
        
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
                
                # Try offline recognition first (Sphinx)
                try:
                    text = self.recognizer.recognize_sphinx(audio_data)
                    return text
                except sr.UnknownValueError:
                    return "[Could not understand audio]"
                except sr.RequestError:
                    # Sphinx not installed, try Google (requires internet)
                    try:
                        text = self.recognizer.recognize_google(audio_data)
                        return text
                    except:
                        return "[Speech recognition failed - install pocketsphinx for offline mode]"
                        
        except Exception as e:
            return f"[Error: {str(e)}]"
    
    def cancel_recording(self):
        """Cancel current recording without transcription"""
        if self.is_recording:
            self.is_recording = False
            
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
            
            self.audio_frames = []
            print("🎤 Voice recording cancelled")


# Singleton instance
voice_handler = VoiceInputHandler()
