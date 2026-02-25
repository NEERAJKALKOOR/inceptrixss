"""
Keyboard Service Integration - Connects all three roles
Role 1 (Keyboard) ↔ Role 3 (UI) ↔ Role 2 (AI)
"""
import sys
import time
from typing import Optional
from keyboard_layer.keyboard_hook import keyboard_monitor
from keyboard_layer.text_manager import text_manager
from keyboard_layer.config import SHOW_GHOST_TEXT, DEBUG_MODE

# Import UI Module (Role 3)
sys.path.insert(0, '.')
from ui_module.interface import UIController


class KeyboardService:
    """
    Main integration service that connects:
    - Keyboard Layer (this)
    - UI Module (ghost text, voice)
    - AI Engine (via UI Module)
    """
    
    def __init__(self, ui_mock_mode: bool = False, ai_mock_mode: bool = False):
        """
        Initialize the keyboard service.
        
        Args:
            ui_mock_mode: Run UI in mock mode (for testing)
            ai_mock_mode: Run AI in mock mode (for testing)
        """
        self.keyboard_monitor = keyboard_monitor
        self.text_manager = text_manager
        self.ui_controller = UIController(mock_mode=ui_mock_mode)
        
        self.is_running = False
        self.current_suggestion = None
        self.current_context = ""
        
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
        
        # Initialize UI
        self.ui_controller.initialize()
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
        print("  Ctrl+Space  - Request AI suggestion")
        print("  Ctrl+Shift+V - Voice input (push-to-talk)")
        print("  Tab         - Accept ghost text suggestion")
        print("  Esc         - Reject ghost text suggestion")
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
        Handle Ctrl+Space - Request AI suggestion.
        
        Args:
            context: Current text buffer
        """
        if DEBUG_MODE:
            print(f"\n🎯 Action key pressed! Context: '{context}'")
        
        # Get active window
        window, app = self.text_manager.get_active_window_info()
        
        # Get selected text (if any)
        selected = self.text_manager.get_selected_text()
        
        # Use selected text or buffer
        text_to_process = selected if selected else context
        
        if not text_to_process or len(text_to_process) < 2:
            print("⚠️ No text to process")
            return
        
        print(f"\n🤖 Requesting AI suggestion for: '{text_to_process[:50]}...'")
        
        # Request AI suggestion via UI module
        self.ui_controller.request_ai_suggestion(
            text=text_to_process,
            action="autocomplete"
        )
        
        # Mark suggestion as active
        self.keyboard_monitor.set_suggestion_active(True)
        self.current_context = text_to_process
        
    def _handle_voice_key(self):
        """Handle Ctrl+Shift+V - Voice input"""
        print("\n🎤 Voice key pressed! Recording...")
        
        # Get current context
        context = self.keyboard_monitor.get_buffer()
        
        # Capture voice and refine
        refined_text = self.ui_controller.capture_voice_and_refine(context)
        
        if refined_text and not refined_text.startswith("[Error"):
            print(f"✅ Voice refined: '{refined_text}'")
            
            # Display as ghost text
            self.ui_controller.display_suggestion(
                suggestion=refined_text,
                confidence=95
            )
            
            # Mark suggestion as active
            self.keyboard_monitor.set_suggestion_active(True)
            self.current_suggestion = refined_text
        else:
            print("❌ Voice refinement failed")
    
    def _handle_accept_suggestion(self):
        """Handle Tab - Accept AI suggestion"""
        print("\n✅ Accepting suggestion...")
        
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
    
    def _handle_reject_suggestion(self):
        """Handle Esc - Reject AI suggestion"""
        print("\n❌ Rejecting suggestion...")
        
        self.ui_controller.reject_suggestion()
        
        # Mark suggestion as inactive
        self.keyboard_monitor.set_suggestion_active(False)
        self.current_suggestion = None
    
    def _handle_text_change(self, text: str):
        """
        Handle automatic AI suggestion on text change (debounced).
        
        Args:
            text: Current text buffer
        """
        if DEBUG_MODE:
            print(f"\n📝 Text changed: '{text}'")
        
        # Only auto-suggest if text editor
        if not self.text_manager.is_text_editor():
            return
        
        # Request autocomplete
        self.ui_controller.request_ai_suggestion(
            text=text,
            action="autocomplete"
        )
        
        # Mark suggestion as active
        self.keyboard_monitor.set_suggestion_active(True)
    
    def run_forever(self):
        """Run the service in a blocking loop"""
        self.start()
        
        try:
            while self.is_running:
                time.sleep(0.1)
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
