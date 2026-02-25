"""
Interactive Demo - Manual Testing
Allows you to manually test the UI features
"""
import sys
from PyQt5.QtCore import QTimer
from ui_module import interface


def print_menu():
    """Print interactive menu"""
    print("\n" + "="*70)
    print("ALWAYS-ON AI KEYBOARD - INTERACTIVE UI DEMO")
    print("="*70)
    print("\nCommands:")
    print("  1 - Show autocomplete suggestion")
    print("  2 - Show formalize suggestion")
    print("  3 - Show expand suggestion")
    print("  4 - Show summarize suggestion")
    print("  5 - Test voice input (mock)")
    print("  6 - Accept current suggestion (Tab)")
    print("  7 - Reject current suggestion (Esc)")
    print("  8 - Custom text + action")
    print("  0 - Exit")
    print("="*70)


def handle_command(controller):
    """Handle user commands"""
    print_menu()
    
    try:
        choice = input("\nEnter command: ").strip()
        
        if choice == "1":
            text = input("Enter text to autocomplete: ")
            response = interface.request_ai_suggestion(text, "autocomplete")
            print(f"✅ Suggestion shown: '{response['result_text']}'")
            
        elif choice == "2":
            text = input("Enter text to formalize: ")
            response = interface.request_ai_suggestion(text, "formalize")
            print(f"✅ Suggestion shown: '{response['result_text']}'")
            
        elif choice == "3":
            text = input("Enter text to expand: ")
            response = interface.request_ai_suggestion(text, "expand")
            print(f"✅ Suggestion shown: '{response['result_text']}'")
            
        elif choice == "4":
            text = input("Enter text to summarize: ")
            response = interface.request_ai_suggestion(text, "summarize")
            print(f"✅ Suggestion shown: '{response['result_text']}'")
            
        elif choice == "5":
            text = input("Enter current text: ")
            print("🎤 Simulating voice input...")
            interface.capture_voice_and_refine(text, lambda result: print(f"✅ Voice refined: '{result}'"))
            
        elif choice == "6":
            accepted = interface.accept_suggestion()
            if accepted:
                print(f"✅ Accepted: '{accepted}'")
            else:
                print("❌ No suggestion to accept")
                
        elif choice == "7":
            interface.reject_suggestion()
            print("❌ Suggestion rejected")
            
        elif choice == "8":
            text = input("Enter text: ")
            action = input("Enter action (rewrite/formalize/expand/summarize/autocomplete): ")
            response = interface.request_ai_suggestion(text, action)
            print(f"✅ Suggestion shown: '{response['result_text']}'")
            
        elif choice == "0":
            print("👋 Exiting...")
            sys.exit(0)
        else:
            print("❌ Invalid command")
        
        # Schedule next command
        QTimer.singleShot(100, lambda: handle_command(controller))
        
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        sys.exit(0)


def main():
    """Main entry point"""
    # Initialize in mock mode
    controller = interface.initialize(mock_mode=True)
    
    print("\n✅ UI Module initialized in MOCK MODE")
    print("   (Set UI_MOCK_MODE=False to use real AI engine)")
    
    # Show overlay
    controller.show()
    
    # Start interactive loop
    QTimer.singleShot(500, lambda: handle_command(controller))
    
    # Run event loop
    sys.exit(controller.run())


if __name__ == "__main__":
    main()
