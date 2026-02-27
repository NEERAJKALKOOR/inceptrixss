"""
Test Script for Cross-App AI Rewriter
Demonstrates the AI processing logic without requiring manual keyboard input
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mock_ai_responses():
    """Test the mock AI response logic"""
    from cross_app_ai_rewrite import CrossAppAIRewriter
    
    rewriter = CrossAppAIRewriter()
    
    print("=" * 60)
    print("Testing Mock AI Responses")
    print("=" * 60)
    print()
    
    # Test case 1: Meeting scheduling
    test_cases = [
        {
            "input": "schedule a meeting",
            "expected": "Please let me know your availability next week."
        },
        {
            "input": "test this feature",
            "expected": "This is an AI-improved version of your text."
        },
        {
            "input": "",
            "expected": "Please let me know how I can assist you."
        },
        {
            "input": "hi",
            "expected": "Hi - enhanced by AI"
        },
        {
            "input": "This is a longer piece of text that needs improvement",
            "expected_contains": "Regarding your request:"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        input_text = test["input"]
        expected = test.get("expected")
        expected_contains = test.get("expected_contains")
        
        result = rewriter._mock_ai_response(input_text)
        
        if expected and result == expected:
            print(f"✅ Test {i} PASSED")
            print(f"   Input: '{input_text}'")
            print(f"   Output: '{result}'")
            passed += 1
        elif expected_contains and expected_contains in result:
            print(f"✅ Test {i} PASSED (contains check)")
            print(f"   Input: '{input_text}'")
            print(f"   Output: '{result}'")
            passed += 1
        else:
            print(f"❌ Test {i} FAILED")
            print(f"   Input: '{input_text}'")
            print(f"   Expected: '{expected or f'contains {expected_contains}'}'")
            print(f"   Got: '{result}'")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


def test_clipboard_operations():
    """Test clipboard save/restore logic"""
    import pyperclip
    import time
    
    print("\n" + "=" * 60)
    print("Testing Clipboard Operations")
    print("=" * 60)
    print()
    
    # Save original clipboard
    original = pyperclip.paste()
    print(f"📋 Original clipboard: '{original}'")
    
    # Test 1: Set and restore
    test_text = "Test clipboard content"
    pyperclip.copy(test_text)
    time.sleep(0.05)
    
    retrieved = pyperclip.paste()
    if retrieved == test_text:
        print("✅ Clipboard write/read works")
    else:
        print(f"❌ Clipboard failed: expected '{test_text}', got '{retrieved}'")
    
    # Test 2: Restore original
    pyperclip.copy(original)
    time.sleep(0.05)
    
    restored = pyperclip.paste()
    if restored == original:
        print("✅ Clipboard restore works")
    else:
        print(f"❌ Restore failed: expected '{original}', got '{restored}'")
    
    print()


def test_hotkey_configuration():
    """Test hotkey configuration"""
    from pynput.keyboard import Key
    
    print("=" * 60)
    print("Testing Hotkey Configuration")
    print("=" * 60)
    print()
    
    from cross_app_ai_rewrite import HOTKEY
    
    print(f"✅ Configured hotkey: {HOTKEY}")
    print(f"   Expected: {{{Key.ctrl_l}, {Key.space}}}")
    
    if HOTKEY == {Key.ctrl_l, Key.space}:
        print("✅ Hotkey configuration correct")
    else:
        print("❌ Hotkey configuration incorrect")
    
    print()


def main():
    """Run all tests"""
    print("\n")
    print("🧪" * 30)
    print("  Cross-App AI Rewriter - Test Suite")
    print("🧪" * 30)
    print()
    
    try:
        # Run tests
        test_hotkey_configuration()
        test_clipboard_operations()
        ai_tests_passed = test_mock_ai_responses()
        
        print("\n" + "=" * 60)
        if ai_tests_passed:
            print("✅ All tests PASSED!")
        else:
            print("⚠️  Some tests FAILED")
        print("=" * 60)
        print()
        
        print("💡 To test the full system:")
        print("   1. Run: python cross_app_ai_rewrite.py")
        print("   2. Open any text app (Notepad, browser, etc.)")
        print("   3. Select text and press Ctrl+Space")
        print()
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
