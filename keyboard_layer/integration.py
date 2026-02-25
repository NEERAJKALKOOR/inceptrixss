"""
Keyboard Service Integration - Connects all three roles
Role 1 (Keyboard) ↔ Role 3 (UI) ↔ Role 2 (AI)
"""
import sys
import time
from typing import Optional
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from keyboard_layer.keyboard_hook import keyboard_monitor
from keyboard_layer.text_manager import text_manager
from keyboard_layer.config import SHOW_GHOST_TEXT, DEBUG_MODE

# Import UI Module (Role 3)
sys.path.insert(0, '.')
from ui_module.interface import UIController


class KeyboardService(QObject):
    """
    Main integration service that connects:
    - Keyboard Layer (this)
    - UI Module (ghost text, voice)
    - AI Engine (via UI Module)
    
    Uses Qt signals to ensure thread-safe UI updates.
    """
    
    # Signals for thread-safe communication
    ai_request_signal = pyqtSignal(str, str, str)  # text, action, app (F12 replace)
    ghost_text_signal = pyqtSignal(str, str, str)  # text, action, app (auto ghost text)
    suggestion_accept_signal = pyqtSignal()
    suggestion_reject_signal = pyqtSignal()
    voice_request_signal = pyqtSignal(str)  # context
    
    def __init__(self, ui_mock_mode: bool = False, ai_mock_mode: bool = False):
        """
        Initialize the keyboard service.
        
        Args:
            ui_mock_mode: Run UI in mock mode (for testing)
            ai_mock_mode: Run AI in mock mode (for testing)
        """
        super().__init__()
        
        self.keyboard_monitor = keyboard_monitor
        self.text_manager = text_manager
        self.ui_controller = UIController(mock_mode=ui_mock_mode)
        
        # Override AI mock mode if specified
        if not ai_mock_mode:
            self.ui_controller.ai_integration.mock_mode = False
            print("✅ AI Integration: REAL MODE (Ollama)")
        else:
            self.ui_controller.ai_integration.mock_mode = True
            print("🎭 AI Integration: MOCK MODE")
        
        self.is_running = False
        self.current_suggestion = None
        self.current_context = ""
        self.request_in_progress = False
        self.last_request_time = 0
        
        # Connect signals to handlers (Qt thread-safe)
        self.ai_request_signal.connect(self._process_ai_request)
        self.ghost_text_signal.connect(self._process_ghost_text_request)
        self.suggestion_accept_signal.connect(self._process_accept_suggestion)
        self.suggestion_reject_signal.connect(self._process_reject_suggestion)
        self.voice_request_signal.connect(self._process_voice_request)
        
        # Connect keyboard callbacks to handlers
        self._setup_callbacks()
        
    def _setup_callbacks(self):
        """Wire up keyboard events to handlers"""
        self.keyboard_monitor.on_action_key = self._handle_action_key
        self.keyboard_monitor.on_voice_key = self._handle_voice_key
        self.keyboard_monitor.on_accept_key = self._handle_accept_suggestion
        self.keyboard_monitor.on_reject_key = self._handle_reject_suggestion
        self.keyboard_monitor.on_text_change = self._handle_text_change
        
    def start(self):
        """Start the keyboard service"""
        if self.is_running:
            print("⚠️ Service already running")
            return
        
        print("=" * 60)
        print("🚀 AI KEYBOARD SERVICE STARTING")
        print("=" * 60)
        
        # UI is already initialized in __init__, just confirm
        print("✅ UI Module initialized")
        
        # Start keyboard monitoring
        self.keyboard_monitor.start()
        print("✅ Keyboard monitor active")
        
        # Get active window info
        window, app = self.text_manager.get_active_window_info()
        print(f"📱 Active app: {app}")
        print(f"🪟 Active window: {window}")
        
        self.is_running = True
        
        print("\n" + "=" * 60)
        print("HOTKEYS:")
        print("  F12          - Request AI suggestion")
        print("  Ctrl+Shift+V - Voice input (push-to-talk)")
        print("  Tab          - Accept ghost text suggestion")
        print("  Esc          - Reject ghost text suggestion")
        print("=" * 60)
        print("\n✅ Service running! Start typing in any app...")
        print("   Press Ctrl+C to stop\n")
        
    def stop(self):
        """Stop the keyboard service"""
        if not self.is_running:
            return
        
        print("\n🛑 Stopping AI Keyboard Service...")
        
        self.keyboard_monitor.stop()
        self.ui_controller.reject_suggestion()  # Clear any visible ghost text
        
        self.is_running = False
        print("✅ Service stopped")
        
    def _handle_action_key(self, context: str):
        """
        Handle F12 - Request AI suggestion.
        ONLY works with selected text - replaces selection with AI response.
        
        Args:
            context: Current text buffer (ignored - only selected text is used)
        """
        # Debounce: ignore if request already in progress
        current_time = time.time()
        if self.request_in_progress:
            print("⏳ AI request already in progress, please wait...")
            return
        
        # Debounce: ignore if less than 1 second since last request
        if current_time - self.last_request_time < 1.0:
            print("⏱️ Please wait 1 second between requests")
            return
        
        if DEBUG_MODE:
            print(f"\n🎯 Action key pressed!")
        
        # Get active window
        window, app = self.text_manager.get_active_window_info()
        
        # Get selected text - REQUIRED
        selected = self.text_manager.get_selected_text()
        
        # Only process if text is selected
        if not selected or len(selected) < 2:
            print("⚠️ No text selected! Select text first, then press F12.")
            return
        
        print(f"\n🤖 Sending to AI: '{selected[:50]}...'")
        
        # Mark request as in progress
        self.request_in_progress = True
        self.last_request_time = current_time
        
        # Emit signal for thread-safe UI update
        self.ai_request_signal.emit(selected, "autocomplete", app or "general")
        
    def _handle_voice_key(self):
        """Handle Ctrl+Shift+V - Voice input"""
        print("\n🎤 Voice key pressed! Recording...")
        
        # Get current context
        context = self.keyboard_monitor.get_buffer()
        
        # Emit signal for thread-safe voice handling
        self.voice_request_signal.emit(context)
        
        # Mark suggestion as active
        self.keyboard_monitor.set_suggestion_active(True)
    
    def _handle_accept_suggestion(self):
        """Handle Tab - Accept AI suggestion"""
        print("\n✅ Accepting suggestion...")
        
        # Emit signal for thread-safe handling
        self.suggestion_accept_signal.emit()
    
    def _handle_reject_suggestion(self):
        """Handle Esc - Reject AI suggestion"""
        print("\n❌ Rejecting suggestion...")
        
        # Emit signal for thread-safe handling
        self.suggestion_reject_signal.emit()
    
    def _handle_text_change(self, text: str):
        """
        Handle automatic AI suggestion on text change (debounced).
        Shows GHOST TEXT that can be accepted with Tab.
        
        Args:
            text: Current text buffer
        """
        if DEBUG_MODE:
            print(f"\n📝 Text changed: '{text}'")
        
        # Get active app
        _, app = self.text_manager.get_active_window_info()
        
        print(f"👻 Ghost text triggered for app: {app}, text: '{text[:30]}...'")
        
        # Emit signal for thread-safe ghost text display
        self.ghost_text_signal.emit(text, "autocomplete", app or "general")
        
        # Mark suggestion as active
        self.keyboard_monitor.set_suggestion_active(True)
    
    # === Signal Handlers (Qt thread-safe) ===
    
    def _process_ghost_text_request(self, text: str, action: str, app: str):
        """Process ghost text request in Qt thread - displays as overlay"""
        print(f"👻 Ghost text request for: '{text[:50]}...'")
        
        # Request AI suggestion (will show as ghost text overlay)
        self.ui_controller.request_ai_suggestion(text, action, app)
    
    def _process_ai_request(self, text: str, action: str, app: str):
        """Process AI request in Qt thread - FOR F12 REPLACE ACTION ONLY"""
        try:
            print(f"🔧 DEBUG: _process_ai_request called (F12 replace)")
            print(f"   Text: '{text[:50]}'")
            print(f"   Action: {action}, App: {app}")
            
            # Get AI response
            print("   Calling ai_integration.process_text()...")
            ai_response = self.ui_controller.ai_integration.process_text(text, action, app)
            
            print(f"   AI Response received: {ai_response}")
            
            # Check if successful
            if ai_response.get("status") == "success":
                result_text = ai_response.get("result_text", "")
                
                if result_text:
                    print(f"\n✅ AI Response: '{result_text[:100]}...'")
                    print(f"📝 Replacing selected text...")
                    
                    # Small delay to ensure selection is still active
                    time.sleep(0.2)
                    
                    # Replace the selected text with AI response
                    self.text_manager.insert_text(result_text, replace_selection=True)
                    print(f"✅ Text replaced!")
                else:
                    print("⚠️ No result text from AI")
            else:
                print(f"❌ AI request failed: {ai_response.get('status', 'unknown error')}")
        
        finally:
            # Mark request as complete
            self.request_in_progress = False
            print("🏁 Request complete")
    
    def _process_accept_suggestion(self):
        """Process suggestion acceptance in Qt thread"""
        # Get the suggestion from UI
        suggestion = self.ui_controller.accept_suggestion()
        
        if suggestion:
            # Insert the text
            self.text_manager.insert_text(suggestion, replace_selection=False)
            print(f"✅ Inserted: '{suggestion[:50]}...'")
            
            # Clear buffer
            self.keyboard_monitor.clear_buffer()
        
        # Mark suggestion as inactive
        self.keyboard_monitor.set_suggestion_active(False)
        self.current_suggestion = None
    
    def _process_reject_suggestion(self):
        """Process suggestion rejection in Qt thread"""
        self.ui_controller.reject_suggestion()
        
        # Mark suggestion as inactive
        self.keyboard_monitor.set_suggestion_active(False)
        self.current_suggestion = None
    
    def _process_voice_request(self, context: str):
        """Process voice request in Qt thread"""
        # Capture voice and refine (this handles display internally)
        self.ui_controller.capture_voice_and_refine(context)
    
    def run_forever(self):
        """Run the service in a blocking loop with Qt event processing"""
        self.start()
        
        try:
            # Use Qt event loop instead of time.sleep to allow signal processing
            from PyQt5.QtCore import QTimer
            
            # Create a timer to keep checking if service is running
            check_timer = QTimer()
            check_timer.timeout.connect(lambda: None)  # Do nothing, just process events
            check_timer.start(100)  # Check every 100ms
            
            # Run Qt event loop (this processes signals)
            print("🔄 Starting Qt event loop...")
            self.ui_controller.app.exec_()
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Keyboard interrupt detected")
        finally:
            self.stop()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Keyboard Service")
    parser.add_argument("--ui-mock", action="store_true", help="Run UI in mock mode")
    parser.add_argument("--ai-mock", action="store_true", help="Run AI in mock mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Set debug mode
    if args.debug:
        import keyboard_layer.config as config
        config.DEBUG_MODE = True
    
    # Create and run service
    service = KeyboardService(
        ui_mock_mode=args.ui_mock,
        ai_mock_mode=args.ai_mock
    )
    
    service.run_forever()


if __name__ == "__main__":
    main()
