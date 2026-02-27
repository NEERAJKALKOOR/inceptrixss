"""
Test Context Detection and Suggestion History Features
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from window_detector import window_detector, get_active_context, get_active_app_info
from context_personas import get_persona_for_context, format_ai_prompt, CONTEXT_PERSONAS
from suggestion_history import suggestion_history
import time


def test_window_detection():
    """Test 1: Window detection"""
    print("\n" + "="*70)
    print("🔍 TEST 1: Window Detection")
    print("="*70)
    
    print("\n📝 Instructions:")
    print("   Switch between different apps in the next 15 seconds:")
    print("   • Open VS Code (should detect 'code' context)")
    print("   • Open Word (should detect 'document' context)")
    print("   • Open Chrome/Gmail (should detect 'email' or 'browser' context)")
    print("   • Open Slack/Discord (should detect 'chat' context)")
    print("\n⏳ Starting in 3 seconds...")
    time.sleep(3)
    
    print("\n🔄 Detecting active windows...")
    for i in range(5):
        info = get_active_app_info()
        print(f"\n   {i+1}. Active Window:")
        print(f"      Title: {info['title'][:50]}")
        print(f"      Process: {info['process']}")
        print(f"      📧 Context: {info['context'].upper()}")
        
        persona = get_persona_for_context(info['context'])
        print(f"      🎭 Persona: {persona['name']}")
        print(f"      💬 Tone: {persona['tone']} (formality: {persona['formality']})")
        
        print(f"\n   ⏳ Switch to a different app... (waiting 3 seconds)")
        time.sleep(3)
    
    print("\n✅ Window detection test complete!")


def test_context_personas():
    """Test 2: Context-aware AI prompts"""
    print("\n" + "="*70)
    print("🎭 TEST 2: Context Personas")
    print("="*70)
    
    test_input = "hey can we talk tmrw"
    
    print(f"\n📝 Test input: '{test_input}'")
    print(f"\n🔄 Testing AI prompts for each context:\n")
    
    for context_name in ["email", "code", "chat", "document", "general"]:
        persona = get_persona_for_context(context_name)
        
        print(f"📧 {context_name.upper()}:")
        print(f"   Persona: {persona['name']}")
        print(f"   Tone: {persona['tone']} (formality: {persona['formality']})")
        
        # Show how prompt would be formatted
        prompt = format_ai_prompt(test_input, "rewrite", context_name)
        print(f"   AI Instructions: {persona['ai_instructions'][:80]}...")
        
        # Show example transformation
        if test_input in persona.get('example_transformations', {}):
            example = persona['example_transformations'][test_input]
            print(f"   ✨ Example output: '{example[:60]}...'")
        
        print()
    
    print("✅ Context personas test complete!")


def test_suggestion_history():
    """Test 3: Suggestion history navigation"""
    print("\n" + "="*70)
    print("📜 TEST 3: Suggestion History")
    print("="*70)
    
    # Clear history
    suggestion_history.clear()
    
    # Add test suggestions
    test_suggestions = [
        {"text": "Hello world", "context": "chat", "action": "casualize", "result": "hey there! 👋"},
        {"text": "meeting tomorrow", "context": "email", "action": "formalize", "result": "Dear [Name],\n\nWould it be possible to schedule a meeting tomorrow?"},
        {"text": "sort list", "context": "code", "action": "complete", "result": "def sort_list(items):\n    return sorted(items)"},
        {"text": "AI explanation", "context": "document", "action": "expand", "result": "Artificial Intelligence represents a significant technological advancement..."},
        {"text": "thanks", "context": "chat", "action": "expand", "result": "thanks so much! 🙏"},
    ]
    
    print(f"\n📝 Adding {len(test_suggestions)} suggestions to history...")
    for item in test_suggestions:
        suggestion_history.add(
            suggestion=item["result"],
            context=item["context"],
            action=item["action"],
            original_text=item["text"]
        )
        print(f"   ✅ Added: '{item['text']}' → '{item['result'][:40]}...' [{item['context']}]")
    
    # Mark some as accepted
    suggestion_history.mark_accepted(True)
    
    # Show stats
    print(f"\n📊 History Statistics:")
    stats = suggestion_history.get_stats()
    print(f"   Total: {stats['total']}")
    print(f"   Accepted: {stats['accepted']}")
    print(f"   Rejected: {stats['rejected']}")
    print(f"   Acceptance rate: {stats['acceptance_rate']:.0%}")
    
    # Test navigation
    print(f"\n⬅️  Testing BACKWARD navigation (Ctrl+Shift+Up):")
    for i in range(6):
        prev = suggestion_history.get_previous()
        if prev:
            print(f"   {i+1}. '{prev['original_text']}' → '{prev['suggestion'][:40]}...' [{prev['context']}]")
        else:
            print(f"   {i+1}. (No more - at oldest)")
            break
    
    print(f"\n➡️  Testing FORWARD navigation (Ctrl+Shift+Down):")
    for i in range(6):
        next_item = suggestion_history.get_next()
        if next_item:
            print(f"   {i+1}. '{next_item['original_text']}' → '{next_item['suggestion'][:40]}...' [{next_item['context']}]")
        else:
            print(f"   {i+1}. (No more - at newest)")
            break
    
    print("\n✅ History navigation test complete!")


def test_combined_workflow():
    """Test 4: Combined workflow simulation"""
    print("\n" + "="*70)
    print("🔄 TEST 4: Combined Workflow")
    print("="*70)
    
    print("\n📝 Simulating user workflow:\n")
    
    # Scenario 1: Email
    print("1️⃣  User in Outlook, types: 'hey can we meet'")
    print("   Press Ctrl+Space...")
    context = "email"
    persona = get_persona_for_context(context)
    print(f"   🎯 Detected context: {context}")
    print(f"   🎭 Using persona: {persona['name']}")
    ai_result = "Dear [Name],\n\nI hope this message finds you well. Would it be possible to schedule a meeting at your earliest convenience?\n\nBest regards"
    print(f"   ✨ AI suggests: '{ai_result[:60]}...'")
    suggestion_history.add(ai_result, context, "formalize", "hey can we meet")
    print(f"   💾 Stored in history")
    
    # Scenario 2: Code editor
    print(f"\n2️⃣  User in VS Code, types: 'function to calculate sum'")
    print("   Press Ctrl+Space...")
    context = "code"
    persona = get_persona_for_context(context)
    print(f"   🎯 Detected context: {context}")
    print(f"   🎭 Using persona: {persona['name']}")
    ai_result = "def calculate_sum(a, b):\n    return a + b"
    print(f"   ✨ AI suggests: '{ai_result}'")
    suggestion_history.add(ai_result, context, "complete", "function to calculate sum")
    print(f"   💾 Stored in history")
    
    # Scenario 3: Navigate history
    print(f"\n3️⃣  User presses Ctrl+Shift+Up to see previous suggestion...")
    prev = suggestion_history.get_previous()
    print(f"   ⬅️  Showing: '{prev['suggestion'][:50]}...' [{prev['context']}]")
    
    print(f"\n4️⃣  User presses Ctrl+Shift+Up again...")
    prev = suggestion_history.get_previous()
    print(f"   ⬅️  Showing: '{prev['suggestion'][:50]}...' [{prev['context']}]")
    
    print(f"\n5️⃣  User presses Tab to accept the suggestion")
    print(f"   ✅ Pasting suggestion from history")
    suggestion_history.mark_accepted(True)
    
    # Show final stats
    print(f"\n📊 Final Statistics:")
    stats = suggestion_history.get_stats()
    print(f"   Total suggestions: {stats['total']}")
    print(f"   Accepted: {stats['accepted']}")
    print(f"   Acceptance rate: {stats['acceptance_rate']:.0%}")
    
    print("\n✅ Combined workflow test complete!")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 CONTEXT DETECTION & HISTORY FEATURES TEST SUITE")
    print("="*70)
    
    # Test 1: Window detection
    print("\nTest 1 will require you to switch apps...")
    input("Press Enter to start window detection test (or Ctrl+C to skip)...")
    test_window_detection()
    
    # Test 2: Context personas
    input("\nPress Enter to test context personas...")
    test_context_personas()
    
    # Test 3: Suggestion history
    input("\nPress Enter to test suggestion history...")
    test_suggestion_history()
    
    # Test 4: Combined workflow
    input("\nPress Enter to test combined workflow...")
    test_combined_workflow()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETE!")
    print("="*70)
    print("\n💡 Now run: python unified_ai_keyboard.py")
    print("   Try Ctrl+Space in different apps to see context adaptation!")
    print("   Try Ctrl+Shift+Up/Down to navigate suggestion history!")


if __name__ == "__main__":
    main()
