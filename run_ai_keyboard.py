"""
Main AI Keyboard Service Entry Point
Runs all three roles integrated:
- Role 1: Keyboard Layer (OS hooks, text insertion)
- Role 3: UI Module (ghost text, voice)
- Role 2: AI Engine (suggestions, refinement)
"""
import sys
sys.path.insert(0, '.')

from keyboard_layer.integration import KeyboardService


def main():
    """
    Launch the full AI Keyboard system.
    
    This starts:
    1. Keyboard monitoring (background)
    2. Ghost text overlay (UI)
    3. AI engine connection
    4. Voice input capability
    
    Hotkeys:
    - Ctrl+Space: Request AI suggestion
    - Ctrl+Shift+V: Voice input
    - Tab: Accept suggestion
    - Esc: Reject suggestion
    """
    print("=" * 70)
    print(" " * 15 + "🚀 AI KEYBOARD - FULL SYSTEM")
    print("=" * 70)
    print()
    print("This service enables AI-powered typing assistance across all apps!")
    print()
    print("Prerequisites:")
    print("  ✅ AI Engine running (uvicorn ai_engine.api_service:app --reload)")
    print("  ✅ Dependencies installed (see requirements*.txt)")
    print()
    print("=" * 70)
    print()
    
    # Ask for mode
    print("Choose mode:")
    print("  1. FULL MODE - Real AI + Real Voice (Ollama + Whisper)")
    print("  2. MOCK MODE - Testing without AI server")
    print()
    
    try:
        choice = input("Enter choice [1/2, default=1]: ").strip()
        
        if choice == "2":
            print("\n🎭 Starting in MOCK mode...")
            service = KeyboardService(ui_mock_mode=True, ai_mock_mode=True)
        else:
            print("\n🤖 Starting in FULL mode (requires AI engine)...")
            service = KeyboardService(ui_mock_mode=False, ai_mock_mode=False)
        
        # Run the service
        service.run_forever()
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. AI engine is running: uvicorn ai_engine.api_service:app --reload")
        print("  2. Dependencies installed: pip install -r requirements_keyboard.txt")


if __name__ == "__main__":
    main()
