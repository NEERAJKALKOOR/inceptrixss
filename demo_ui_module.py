"""
Demo Script - Simulating Keyboard + AI Integration
Shows how keyboard layer and AI engine would call the UI module
"""
import sys
import time
from PyQt5.QtCore import QTimer
from ui_module import interface


def demo_ghost_text_autocomplete():
    """Demo 1: Ghost text autocomplete suggestions"""
    print("\n" + "="*70)
    print("DEMO 1: GHOST TEXT AUTOCOMPLETE")
    print("="*70)
    
    # Simulate user typing
    user_texts = [
        "I would like to",
        "Dear Sir, I am writing to",
        "The meeting is scheduled for"
    ]
    
    for idx, text in enumerate(user_texts, 1):
        print(f"\n[{idx}] User types: '{text}'")
        print("    Requesting AI suggestion...")
        
        # Keyboard layer would call this
        ai_response = interface.request_ai_suggestion(
            text=text,
            action="autocomplete",
            app="email"
        )
        
        print(f"    Ghost text shown: '{ai_response['result_text']}'")
        print(f"    Confidence: {ai_response['confidence']:.0%}")
        print("    [User can press Tab to accept, Esc to reject]")
        
        time.sleep(2)
        
        # Simulate user accepting
        if idx == 1:
            accepted = interface.accept_suggestion()
            if accepted:
                print(f"    ✅ User pressed Tab - Accepted!")
        else:
            interface.reject_suggestion()
            print(f"    ❌ User pressed Esc - Rejected")
        
        time.sleep(1)


def demo_text_refinement():
    """Demo 2: Text refinement with different actions"""
    print("\n" + "="*70)
    print("DEMO 2: TEXT REFINEMENT (Rewrite, Formalize, Expand, Summarize)")
    print("="*70)
    
    test_cases = [
        ("hey can we meet up", "formalize", "email"),
        ("AI helps productivity", "expand", "document"),
        ("This is a long text about artificial intelligence and how it's transforming the world", "summarize", "notes")
    ]
    
    for idx, (text, action, app) in enumerate(test_cases, 1):
        print(f"\n[{idx}] Original: '{text}'")
        print(f"    Action: {action}")
        
        ai_response = interface.request_ai_suggestion(
            text=text,
            action=action,
            app=app
        )
        
        print(f"    AI Result: '{ai_response['result_text']}'")
        print(f"    Confidence: {ai_response['confidence']:.0%}")
        
        time.sleep(2)
        interface.reject_suggestion()


def demo_voice_refinement():
    """Demo 3: Voice + text hybrid refinement"""
    print("\n" + "="*70)
    print("DEMO 3: VOICE + TEXT HYBRID REFINEMENT")
    print("="*70)
    
    current_text = "schedule meeting"
    
    print(f"\nUser typed: '{current_text}'")
    print("User presses Ctrl+Shift+V (push-to-talk)...")
    print("🎤 Recording voice input...")
    
    def on_voice_complete(refined_text):
        print(f"\n✅ Voice refinement complete!")
        print(f"   Refined suggestion: '{refined_text}'")
    
    # This would be triggered by keyboard layer when user presses push-to-talk
    interface.capture_voice_and_refine(current_text, on_voice_complete)
    
    # Wait for voice capture to complete (3 seconds in this demo)
    time.sleep(4)


def demo_manual_ai_response():
    """Demo 4: External AI engine sending response directly"""
    print("\n" + "="*70)
    print("DEMO 4: EXTERNAL AI ENGINE INTEGRATION")
    print("="*70)
    
    print("\nSimulating external AI engine calling UI module...")
    
    # This is what an external AI engine would send
    external_ai_response = {
        "api_version": "v1",
        "result_text": "I hope this message finds you well. I would like to schedule a meeting to discuss the project.",
        "confidence": 0.95,
        "intent": "formalize",
        "status": "success"
    }
    
    print(f"AI Response received:")
    print(f"  - result_text: '{external_ai_response['result_text']}'")
    print(f"  - confidence: {external_ai_response['confidence']}")
    
    # Display it
    interface.display_suggestion(external_ai_response)
    print("\n✅ Ghost text displayed in overlay!")
    
    time.sleep(3)


def demo_confidence_levels():
    """Demo 5: Different confidence levels visualization"""
    print("\n" + "="*70)
    print("DEMO 5: CONFIDENCE LEVEL VISUALIZATION")
    print("="*70)
    
    confidence_tests = [
        ("High confidence test", 0.95),
        ("Medium confidence test", 0.75),
        ("Low confidence test", 0.50)
    ]
    
    for text, confidence in confidence_tests:
        print(f"\nShowing suggestion with {confidence:.0%} confidence...")
        
        ai_response = {
            "api_version": "v1",
            "result_text": f"This is a {confidence:.0%} confidence suggestion",
            "confidence": confidence,
            "intent": "test",
            "status": "success"
        }
        
        interface.display_suggestion(ai_response)
        time.sleep(2)
        interface.reject_suggestion()


def run_all_demos():
    """Run all demos sequentially"""
    print("\n" + "🚀 "*35)
    print("ALWAYS-ON AI KEYBOARD - UI MODULE DEMO")
    print("🚀 "*35)
    print("\nThis demo simulates how the keyboard layer and AI engine")
    print("would interact with the UI module.")
    print("\nRunning in MOCK MODE - no real AI calls needed")
    print("-"*70)
    
    # Schedule demos
    QTimer.singleShot(1000, demo_ghost_text_autocomplete)
    QTimer.singleShot(10000, demo_text_refinement)
    QTimer.singleShot(18000, demo_voice_refinement)
    QTimer.singleShot(25000, demo_manual_ai_response)
    QTimer.singleShot(30000, demo_confidence_levels)
    
    # Exit after all demos
    QTimer.singleShot(38000, lambda: sys.exit(0))


def main():
    """Main entry point"""
    # Initialize UI module in mock mode
    controller = interface.initialize(mock_mode=True)
    
    print("\n✅ UI Module initialized in MOCK MODE")
    print("   Ghost overlay created")
    print("   Voice handler ready")
    print("   AI integration ready\n")
    
    # Show the overlay
    controller.show()
    
    # Run demos
    run_all_demos()
    
    # Start UI event loop
    sys.exit(controller.run())


if __name__ == "__main__":
    main()
