"""
Public Interface for UI Module
This is the main interface that external modules (keyboard layer, AI engine) will use.
"""
import sys
from typing import Dict, Any, Optional, Callable
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, pyqtSignal, QObject

from ui_module.ghost_overlay import GhostTextOverlay
from ui_module.voice_input import voice_handler
from ui_module.ai_integration import ai_integration
from ui_module.config import MOCK_MODE


class UIController(QObject):
    """
    Main controller for the UI module.
    Provides clean public interface for external integration.
    """
    
    # Signals for external integration
    suggestion_accepted = pyqtSignal(str)  # Emitted when user accepts suggestion
    suggestion_rejected = pyqtSignal()  # Emitted when user rejects suggestion
    voice_captured = pyqtSignal(str)  # Emitted when voice is transcribed
    
    def __init__(self, mock_mode: bool = MOCK_MODE):
        super().__init__()
        
        # Initialize QApplication
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # Initialize components
        self.overlay = GhostTextOverlay()
        self.voice_handler = voice_handler
        self.ai_integration = ai_integration
        self.ai_integration.mock_mode = mock_mode
        
        # Connect signals
        self.overlay.suggestion_accepted.connect(self._on_suggestion_accepted)
        self.overlay.suggestion_rejected.connect(self._on_suggestion_rejected)
        
        # State
        self.current_context = {
            "app": "general",
            "current_text": "",
            "last_action": "autocomplete"
        }
        
    def display_suggestion(self, ai_response: Dict[str, Any]):
        """
        Display AI suggestion as ghost text.
        
        Args:
            ai_response: AI response dict with format:
                {
                    "api_version": "v1",
                    "result_text": "suggested text...",
                    "confidence": 0.92,
                    "intent": "autocomplete",
                    "status": "success"
                }
        """
        result_text = ai_response.get("result_text", "")
        confidence = ai_response.get("confidence", 0.5)
        current_text = self.current_context.get("current_text", "")
        
        if result_text and ai_response.get("status") == "success":
            self.overlay.display_suggestion(current_text, result_text, confidence)
        else:
            print(f"⚠️ Cannot display suggestion: {ai_response.get('status', 'unknown error')}")
    
    def accept_suggestion(self) -> Optional[str]:
        """
        User accepts the current suggestion.
        Commits ghost text into real text.
        
        Returns:
            Accepted text or None
        """
        return self.overlay.accept_suggestion()
    
    def reject_suggestion(self):
        """
        User rejects the current suggestion.
        Clears ghost text.
        """
        self.overlay.reject_suggestion()
    
    def capture_voice_and_refine(self, current_text: str = "", 
                                 on_complete: Optional[Callable[[str], None]] = None):
        """
        Handle push-to-talk voice input and refine text.
        
        Args:
            current_text: Current typed text to refine
            on_complete: Callback when refinement is complete
        """
        self.current_context["current_text"] = current_text
        
        # Start recording
        self.voice_handler.start_recording()
        print("🎤 Push-to-talk activated. Speak now...")
        
        # Stop and transcribe after a delay (in real implementation, 
        # this would be triggered by releasing the push-to-talk key)
        QTimer.singleShot(3000, lambda: self._finish_voice_capture(current_text, on_complete))
    
    def _finish_voice_capture(self, current_text: str, callback: Optional[Callable]):
        """Internal: Finish voice capture and process"""
        transcribed = self.voice_handler.stop_recording_and_transcribe()
        
        if transcribed:
            self.voice_captured.emit(transcribed)
            
            # Refine current text with voice input
            ai_response = self.ai_integration.refine_with_voice(
                original_text=current_text,
                voice_input=transcribed,
                previous_output=self.overlay.ghost_text
            )
            
            # Display refined suggestion
            self.display_suggestion(ai_response)
            
            if callback:
                callback(ai_response.get("result_text", ""))
    
    def request_ai_suggestion(self, text: str, action: str = "autocomplete", 
                             app: str = "general", context: Dict = None):
        """
        Request AI suggestion for given text.
        
        Args:
            text: Input text
            action: AI action (autocomplete, rewrite, formalize, expand, summarize)
            app: Application context
            context: Additional context
        """
        self.current_context["current_text"] = text
        self.current_context["app"] = app
        self.current_context["last_action"] = action
        
        # Get AI response
        ai_response = self.ai_integration.process_text(text, action, app, context)
        
        # Display suggestion
        self.display_suggestion(ai_response)
        
        return ai_response
    
    def show(self):
        """Show the overlay UI"""
        self.overlay.show()
    
    def hide(self):
        """Hide the overlay UI"""
        self.overlay.hide()
    
    def run(self):
        """Run the UI event loop (blocking)"""
        return self.app.exec_()
    
    def _on_suggestion_accepted(self, text: str):
        """Internal: Handle suggestion acceptance"""
        self.suggestion_accepted.emit(text)
        print(f"✅ Suggestion accepted: '{text}'")
    
    def _on_suggestion_rejected(self):
        """Internal: Handle suggestion rejection"""
        self.suggestion_rejected.emit()
        print("❌ Suggestion rejected")


# === Public API Functions ===
# These are the main functions external modules will call

_controller_instance = None

def initialize(mock_mode: bool = MOCK_MODE) -> UIController:
    """
    Initialize the UI module.
    
    Args:
        mock_mode: Use mock AI responses instead of real API
        
    Returns:
        UIController instance
    """
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = UIController(mock_mode=mock_mode)
    return _controller_instance


def display_suggestion(ai_response: Dict[str, Any]):
    """
    Display AI suggestion as ghost text.
    
    Args:
        ai_response: AI response dict with result_text, confidence, etc.
    """
    if _controller_instance is None:
        raise RuntimeError("UI module not initialized. Call initialize() first.")
    _controller_instance.display_suggestion(ai_response)


def accept_suggestion() -> Optional[str]:
    """
    Accept the current suggestion.
    
    Returns:
        Accepted text or None
    """
    if _controller_instance is None:
        raise RuntimeError("UI module not initialized. Call initialize() first.")
    return _controller_instance.accept_suggestion()


def reject_suggestion():
    """Reject the current suggestion."""
    if _controller_instance is None:
        raise RuntimeError("UI module not initialized. Call initialize() first.")
    _controller_instance.reject_suggestion()


def capture_voice_and_refine(current_text: str = "", 
                             on_complete: Optional[Callable[[str], None]] = None):
    """
    Capture voice input and refine text.
    
    Args:
        current_text: Current typed text
        on_complete: Callback when complete
    """
    if _controller_instance is None:
        raise RuntimeError("UI module not initialized. Call initialize() first.")
    _controller_instance.capture_voice_and_refine(current_text, on_complete)


def request_ai_suggestion(text: str, action: str = "autocomplete", 
                         app: str = "general", context: Dict = None) -> Dict[str, Any]:
    """
    Request AI suggestion for text.
    
    Args:
        text: Input text
        action: AI action type
        app: Application context
        context: Additional context
        
    Returns:
        AI response dict
    """
    if _controller_instance is None:
        raise RuntimeError("UI module not initialized. Call initialize() first.")
    return _controller_instance.request_ai_suggestion(text, action, app, context)


def get_controller() -> UIController:
    """Get the controller instance"""
    if _controller_instance is None:
        raise RuntimeError("UI module not initialized. Call initialize() first.")
    return _controller_instance
