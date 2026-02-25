"""
Comprehensive Test Suite for UI Module
Tests all functionality in isolation and integration
"""
import sys
import time
from ui_module import interface


class UIModuleTestSuite:
    """Test suite for UI module"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.controller = None
    
    def test_initialization(self):
        """Test 1: Module initialization"""
        print("\n[TEST 1] Module Initialization")
        try:
            self.controller = interface.initialize(mock_mode=True)
            assert self.controller is not None
            print("✅ PASS: Module initialized successfully")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_display_suggestion(self):
        """Test 2: Display AI suggestion"""
        print("\n[TEST 2] Display Suggestion")
        try:
            ai_response = {
                "api_version": "v1",
                "result_text": "Test suggestion text",
                "confidence": 0.92,
                "intent": "test",
                "status": "success"
            }
            interface.display_suggestion(ai_response)
            print("✅ PASS: Suggestion displayed")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_accept_suggestion(self):
        """Test 3: Accept suggestion"""
        print("\n[TEST 3] Accept Suggestion")
        try:
            # First display a suggestion
            ai_response = {
                "api_version": "v1",
                "result_text": "Accepted text",
                "confidence": 0.90,
                "intent": "test",
                "status": "success"
            }
            interface.display_suggestion(ai_response)
            
            # Accept it
            accepted = interface.accept_suggestion()
            assert accepted == "Accepted text"
            print(f"✅ PASS: Suggestion accepted: '{accepted}'")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_reject_suggestion(self):
        """Test 4: Reject suggestion"""
        print("\n[TEST 4] Reject Suggestion")
        try:
            # Display a suggestion
            ai_response = {
                "api_version": "v1",
                "result_text": "Rejected text",
                "confidence": 0.85,
                "intent": "test",
                "status": "success"
            }
            interface.display_suggestion(ai_response)
            
            # Reject it
            interface.reject_suggestion()
            print("✅ PASS: Suggestion rejected")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_request_ai_suggestion(self):
        """Test 5: Request AI suggestion (mock)"""
        print("\n[TEST 5] Request AI Suggestion")
        try:
            response = interface.request_ai_suggestion(
                text="Test input",
                action="autocomplete",
                app="test"
            )
            
            assert "result_text" in response
            assert "confidence" in response
            assert response["status"] == "success"
            
            print(f"✅ PASS: AI response received: '{response['result_text']}'")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_confidence_levels(self):
        """Test 6: Different confidence levels"""
        print("\n[TEST 6] Confidence Level Visualization")
        try:
            levels = [
                (0.95, "High"),
                (0.75, "Medium"),
                (0.50, "Low")
            ]
            
            for confidence, level in levels:
                ai_response = {
                    "api_version": "v1",
                    "result_text": f"{level} confidence test",
                    "confidence": confidence,
                    "intent": "test",
                    "status": "success"
                }
                interface.display_suggestion(ai_response)
                time.sleep(0.5)
                interface.reject_suggestion()
            
            print("✅ PASS: All confidence levels displayed correctly")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_all_actions(self):
        """Test 7: All AI actions"""
        print("\n[TEST 7] All AI Actions")
        try:
            actions = ["rewrite", "formalize", "expand", "summarize", "autocomplete"]
            
            for action in actions:
                response = interface.request_ai_suggestion(
                    text=f"Test {action}",
                    action=action
                )
                assert response["status"] == "success"
                interface.reject_suggestion()
            
            print(f"✅ PASS: All {len(actions)} actions tested")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_voice_input_mock(self):
        """Test 8: Voice input (mock mode)"""
        print("\n[TEST 8] Voice Input (Mock)")
        try:
            voice_completed = [False]
            
            def on_complete(result):
                voice_completed[0] = True
                print(f"   Voice result: '{result}'")
            
            interface.capture_voice_and_refine(
                current_text="Test voice",
                on_complete=on_complete
            )
            
            # Wait for mock voice to complete
            time.sleep(4)
            
            assert voice_completed[0], "Voice callback not triggered"
            print("✅ PASS: Voice input completed")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_error_handling(self):
        """Test 9: Error handling"""
        print("\n[TEST 9] Error Handling")
        try:
            # Invalid response
            invalid_response = {
                "status": "error",
                "result_text": "[Error message]",
                "confidence": 0.0
            }
            
            # Should not crash
            interface.display_suggestion(invalid_response)
            print("✅ PASS: Error handled gracefully")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def test_signals(self):
        """Test 10: Signal connections"""
        print("\n[TEST 10] Signal Connections")
        try:
            signals_triggered = []
            
            # Connect to signals
            self.controller.suggestion_accepted.connect(
                lambda text: signals_triggered.append(f"accepted:{text}")
            )
            self.controller.suggestion_rejected.connect(
                lambda: signals_triggered.append("rejected")
            )
            
            # Trigger signals
            ai_response = {
                "api_version": "v1",
                "result_text": "Signal test",
                "confidence": 0.90,
                "intent": "test",
                "status": "success"
            }
            interface.display_suggestion(ai_response)
            interface.accept_suggestion()
            
            assert len(signals_triggered) > 0
            print(f"✅ PASS: Signals triggered: {signals_triggered}")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.failed += 1
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("UI MODULE - COMPREHENSIVE TEST SUITE")
        print("="*70)
        
        tests = [
            self.test_initialization,
            self.test_display_suggestion,
            self.test_accept_suggestion,
            self.test_reject_suggestion,
            self.test_request_ai_suggestion,
            self.test_confidence_levels,
            self.test_all_actions,
            self.test_voice_input_mock,
            self.test_error_handling,
            self.test_signals
        ]
        
        for test in tests:
            test()
            time.sleep(0.5)
        
        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Success Rate: {self.passed}/{self.passed + self.failed} ({self.passed/(self.passed + self.failed)*100:.1f}%)")
        print("="*70)
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! UI Module is ready for deployment.")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Review errors above.")
        
        return self.failed == 0


def main():
    """Main entry point"""
    suite = UIModuleTestSuite()
    
    # Show UI
    if suite.test_initialization():
        suite.controller.show()
    
    # Run tests
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(1000, lambda: suite.run_all_tests())
    QTimer.singleShot(15000, lambda: sys.exit(0 if suite.failed == 0 else 1))
    
    # Run event loop
    sys.exit(suite.controller.run())


if __name__ == "__main__":
    main()
