"""
Voice Input Module - Push-to-talk with offline speech-to-text
Captures microphone input and converts to text for AI refinement
"""
import wave
import threading
import tempfile
import os
from typing import Callable, Optional
from ui_module.config import SAMPLE_RATE, VOICE_ENABLED

# Try to import pyaudio (optional)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("⚠️ pyaudio not installed. Voice input will use mock mode.")

# Try to import whisper for speech recognition (offline capable)
try:
    import whisper
    import numpy as np
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ openai-whisper not installed. Voice input will use mock mode.")


class VoiceInputHandler:
    """
    Handles push-to-talk voice input with offline speech-to-text.
    Non-blocking, does not interfere with typing.
    """
    
    def __init__(self, mock_mode: bool = not VOICE_ENABLED, model_size: str = "base"):
        self.mock_mode = mock_mode or not (WHISPER_AVAILABLE and PYAUDIO_AVAILABLE)
        self.is_recording = False
        self.audio_frames = []
        
        # Load Whisper model (lazy loading on first use)
        self.model = None
        self.model_size = model_size  # tiny, base, small, medium, large (tiny=39MB, base=140MB)
        
        # Audio settings - optimized for speech
        self.chunk = 1024
        self.format = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
        self.channels = 1
        self.rate = SAMPLE_RATE
        
        self.audio = None
        self.stream = None
        self.input_device_index = None  # Let PyAudio choose default
        
    def start_recording(self):
        """Start capturing microphone input (push-to-talk pressed)"""
        if self.mock_mode:
            print("🎤 [MOCK] Voice recording started...")
            self.is_recording = True
            return
        
        if self.is_recording:
            print("⚠️ Already recording, ignoring start request")
            return  # Already recording
        
        if not PYAUDIO_AVAILABLE:
            print("⚠️ PyAudio not available. Using mock mode.")
            self.mock_mode = True
            self.is_recording = True
            return
        
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
            print("⚠️ Falling back to mock mode")
            self.mock_mode = True
            self.is_recording = True
    
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
        
        try:
            # Wait for recording thread to finish
            if hasattr(self, 'recording_thread'):
                self.recording_thread.join(timeout=1.0)
            
            # Stop stream
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
                self.stream = None
            
            if self.audio:
                try:
                    self.audio.terminate()
                except:
                    pass
                self.audio = None
            
            # Check if we have audio data
            if not self.audio_frames or len(self.audio_frames) == 0:
                print("⚠️ No audio data recorded. Please try again.")
                self.audio_frames = []
                return "[No audio recorded]"
            
            # Calculate audio duration
            audio_duration = (len(self.audio_frames) * self.chunk) / self.rate
            print(f"🎤 Audio duration: {audio_duration:.2f} seconds")
            
            # Check minimum duration (0.5 seconds)
            if audio_duration < 0.5:
                print(f"⚠️ Audio too short ({audio_duration:.2f}s). Please speak for at least 0.5 seconds.")
                self.audio_frames = []
                return "[Audio too short]"
            
            # Save audio to temporary file
            temp_wav = tempfile.mktemp(suffix=".wav")
            
            try:
                # Write audio to WAV file
                wf = wave.open(temp_wav, 'wb')
                wf.setnchannels(self.channels)
                # Use fixed sample width (2 bytes = 16-bit) since audio is already terminated
                wf.setsampwidth(2)
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
                print(f"❌ Error processing audio: {e}")
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
                return "[Transcription error]"
        
        except Exception as e:
            print(f"❌ Error in stop_recording_and_transcribe: {e}")
            import traceback
            traceback.print_exc()
            return "[Error]"
        
        finally:
            # Always cleanup resources
            self.audio_frames = []
            self.is_recording = False
    
    def _transcribe_audio(self, audio_file: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper (offline).
        Whisper provides state-of-the-art accuracy with 99+ language support.
        """
        if not WHISPER_AVAILABLE:
            return "[Whisper not available]"
        
        try:
            # Load model on first use (lazy loading)
            if self.model is None:
                print(f"🔄 Loading Whisper {self.model_size} model (one-time setup)...")
                try:
                    self.model = whisper.load_model(self.model_size)
                    print(f"✅ Whisper model loaded successfully")
                except Exception as load_error:
                    print(f"⚠️ Error loading {self.model_size} model: {load_error}")
                    print(f"🔄 Falling back to 'base' model...")
                    self.model_size = 'base'
                    self.model = whisper.load_model('base')
                    print(f"✅ Base model loaded successfully")
            
            # Check audio file size
            file_size = os.path.getsize(audio_file)
            print(f"📊 Audio file size: {file_size} bytes")
            
            if file_size < 1000:  # Less than 1KB is probably empty
                print("⚠️ Audio file too small. Recording may be empty.")
                return "[Recording too short or empty]"
            
            # Transcribe audio (requires ffmpeg)
            # Force English language and use simple parameters
            print(f"🔄 Transcribing with Whisper {self.model_size} model...")
            result = self.model.transcribe(
                audio_file,
                language='en',  # FORCE English instead of auto-detect
                fp16=False,
                verbose=True  # Show detailed processing
            )
            
            # Debug: Show full result
            print(f"📊 Whisper result keys: {result.keys()}")
            print(f"📊 Raw text: '{result.get('text', '')}'")
            print(f"📊 Language detected: {result.get('language', 'unknown')}")
            
            # Check segments for more detail
            if 'segments' in result and result['segments']:
                print(f"📊 Number of segments: {len(result['segments'])}")
                for i, seg in enumerate(result['segments'][:3]):
                    print(f"   Segment {i}: '{seg.get('text', '')}' (no_speech_prob: {seg.get('no_speech_prob', 0):.2f})")
            
            text = result["text"].strip()
            
            if not text:
                print("⚠️ Whisper returned empty text. Possible causes:")
                print("   • Microphone input level too low")
                print("   • Background noise drowning out speech") 
                print("   • Wrong audio device selected")
                print("   • Try speaking louder and closer to the microphone")
                return "[Could not understand audio - try speaking louder]"
            
            return text
                        
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Whisper transcription error: {e}")
            
            # Provide helpful error messages
            if "key.size" in error_msg or "value.size" in error_msg:
                print("💡 This error usually means the audio is too short or corrupted.")
                print("   Try speaking for at least 1-2 seconds before stopping.")
                return "[Audio too short - speak longer]"
            else:
                return f"[Error: {error_msg[:50]}]"
    
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


# Singleton instance with MEDIUM model (better accuracy, 1.5GB)
# Models: tiny (39MB), base (140MB), small (470MB), medium (1.5GB), large (3GB)
voice_handler = VoiceInputHandler(mock_mode=False, model_size="medium")
