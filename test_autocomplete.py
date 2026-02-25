import requests
import json

def test_autocomplete_suggestions():
    """
    Demonstrates how inline ghost suggestions would work.
    The frontend would call this API as user types and show the result as ghost text.
    """
    url = "http://localhost:8000/process_text"
    
    test_cases = [
        {
            "text": "I am writing to inform you about",
            "app": "email",
            "action": "autocomplete",
            "description": "Email completion"
        },
        {
            "text": "Dear Sir, I would like to",
            "app": "email", 
            "action": "autocomplete",
            "description": "Formal email suggestion"
        },
        {
            "text": "The meeting is scheduled for",
            "app": "calendar",
            "action": "autocomplete",
            "description": "Calendar autocomplete"
        },
        {
            "text": "Thank you for your",
            "app": "email",
            "action": "autocomplete",
            "description": "Polite closing"
        }
    ]
    
    print("=" * 70)
    print("TESTING AUTOCOMPLETE SUGGESTIONS (Ghost Text Simulation)")
    print("=" * 70)
    
    for idx, test in enumerate(test_cases, 1):
        payload = {
            "api_version": "v1",
            "text": test["text"],
            "app": test["app"],
            "action": test["action"],
            "context": {
                "previous_text": "",
                "user_style": "formal"
            }
        }
        
        try:
            print(f"\n[Test {idx}] {test['description']}")
            print(f"You typed: '{test['text']}'")
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            suggestion = result['result_text']
            
            print(f"Ghost suggestion: '{suggestion}'")
            print(f"Confidence: {result['confidence']} | Latency: {result['latency_ms']}ms")
            print("-" * 70)
            
        except requests.exceptions.ConnectionError:
            print("\n❌ Error: Server not running!")
            print("Start server: uvicorn ai_engine.api_service:app --reload")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
            return
    
    print("\n" + "=" * 70)
    print("HOW INLINE GHOST SUGGESTIONS WOULD WORK:")
    print("=" * 70)
    print("1. User types in any app (email, chat, document)")
    print("2. Frontend sends partial text to this API with 'autocomplete' action")
    print("3. API returns suggestion (like above)")
    print("4. Frontend shows suggestion as gray ghost text")
    print("5. User presses Tab/→ to accept, or keeps typing to ignore")
    print("=" * 70)

if __name__ == "__main__":
    test_autocomplete_suggestions()
