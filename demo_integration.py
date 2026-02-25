"""
Integration Example - Connecting UI Module with Real AI Engine
Demonstrates how keyboard layer would integrate both modules
"""
import sys
import time
from PyQt5.QtCore import QTimer
from ui_module import interface


class KeyboardLayerSimulator:
    """
    Simulates how the keyboard layer (Role 1) would integrate
    the UI module (Role 3) with the AI engine (Role 2)
    """
    
    def __init__(self, use_real_ai: bool = False):
        # Initialize UI module
        self.ui = interface.initialize(mock_mode=not use_real_ai)
        
        # Connect signals
        self.ui.suggestion_accepted.connect(self.on_suggestion_accepted)
        self.ui.suggestion_rejected.connect(self.on_suggestion_rejected)
        self.ui.voice_captured.connect(self.on_voice_captured)
        
        # State
        self.current_app = "email"
        self.typing_context = ""
        
        print(f"\n✅ Keyboard Layer Simulator initialized")
        print(f"   AI Mode: {'REAL' if use_real_ai else 'MOCK'}")
        if use_real_ai:
            print(f"   Ensure AI engine is running: uvicorn ai_engine.api_service:app --reload")
    
    def simulate_user_typing(self, text: str, action: str = "autocomplete"):
        """
        Simulate user typing text.
        In real implementation, this would be triggered by keyboard hooks.
        """
        print(f"\n👤 User types: '{text}'")
        self.typing_context = text
        
        # Request AI suggestion
        print(f"   🤖 Requesting {action} from AI engine...")
        
        response = interface.request_ai_suggestion(
            text=text,
            action=action,
            app=self.current_app,
            context={"user_style": "professional"}
        )
        
        print(f"   👻 Ghost text displayed: '{response['result_text']}'")
        print(f"   📊 Confidence: {response['confidence']:.0%}")
        print(f"   💡 User can press [Tab] to accept or [Esc] to reject")
    
    def simulate_tab_press(self):
        """User presses Tab to accept suggestion"""
        print("\n⌨️  User presses [Tab]")
        accepted = interface.accept_suggestion()
        
        if accepted:
            # In real implementation, insert this into the active window
            self.typing_context += accepted
            print(f"   ✅ Text inserted: '{accepted}'")
            print(f"   📝 Full text now: '{self.typing_context}'")
    
    def simulate_esc_press(self):
        """User presses Esc to reject suggestion"""
        print("\n⌨️  User presses [Esc]")
        interface.reject_suggestion()
        print(f"   ❌ Suggestion rejected")
    
    def simulate_voice_input(self, current_text: str):
        """User presses Ctrl+Shift+V for voice input"""
        print(f"\n🎤 User presses [Ctrl+Shift+V] (Push-to-talk)")
        print(f"   Current text: '{current_text}'")
        print(f"   🎙️  Recording... (speak now)")
        
        def on_complete(refined_text):
            print(f"\n   ✅ Voice refinement complete!")
            print(f"   👻 New suggestion: '{refined_text}'")
        
        interface.capture_voice_and_refine(current_text, on_complete)
    
    def on_suggestion_accepted(self, text: str):
        """Callback when suggestion is accepted"""
        print(f"   [SIGNAL] suggestion_accepted: '{text}'")
    
    def on_suggestion_rejected(self):
        """Callback when suggestion is rejected"""
        print(f"   [SIGNAL] suggestion_rejected")
    
    def on_voice_captured(self, text: str):
        """Callback when voice is captured"""
        print(f"   [SIGNAL] voice_captured: '{text}'")
    
    def run_demo_scenario(self):
        """Run a complete demo scenario"""
        print("\n" + "="*70)
        print("INTEGRATION DEMO - KEYBOARD + UI + AI")
        print("="*70)
        print("\nScenario: User composing an email")
        print("-"*70)
        
        # Scenario timeline
        QTimer.singleShot(1000, lambda: self.simulate_user_typing("I would like to", "autocomplete"))
        QTimer.singleShot(4000, lambda: self.simulate_tab_press())
        
        QTimer.singleShot(6000, lambda: self.simulate_user_typing("hey can we meet", "formalize"))
        QTimer.singleShot(9000, lambda: self.simulate_esc_press())
        
        QTimer.singleShot(11000, lambda: self.simulate_user_typing("schedule meeting tomorrow", "formalize"))
        QTimer.singleShot(14000, lambda: self.simulate_tab_press())
        
        QTimer.singleShot(16000, lambda: self.simulate_voice_input("schedule meeting tomorrow"))
        
        QTimer.singleShot(22000, lambda: self.print_summary())
        QTimer.singleShot(24000, lambda: sys.exit(0))
    
    def print_summary(self):
        """Print summary of integration"""
        print("\n" + "="*70)
        print("INTEGRATION SUMMARY")
        print("="*70)
        print("\n✅ Successfully demonstrated:")
        print("   1. Keyboard layer simulating user input")
        print("   2. UI module displaying ghost text")
        print("   3. AI engine providing suggestions")
        print("   4. User accepting/rejecting suggestions")
        print("   5. Voice input refinement")
        print("\n🎯 Integration boundaries respected:")
        print("   - Keyboard layer: Input capture (simulated)")
        print("   - UI module: Display + interaction only")
        print("   - AI engine: Text processing")
        print("\n💡 All modules communicate via clean interfaces!")
        print("="*70)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="UI + AI Integration Demo")
    parser.add_argument("--real-ai", action="store_true", 
                       help="Use real AI engine instead of mock")
    args = parser.parse_args()
    
    # Create simulator
    simulator = KeyboardLayerSimulator(use_real_ai=args.real_ai)
    
    # Show UI
    simulator.ui.show()
    
    # Run demo
    simulator.run_demo_scenario()
    
    # Start event loop
    sys.exit(simulator.ui.run())


if __name__ == "__main__":
    main()
