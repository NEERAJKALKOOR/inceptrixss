import requests
import json

def test_iterative_refinement():
    """
    Demonstrates the iterative refinement loop - a key requirement.
    User can refine AI outputs based on feedback.
    """
    url_process = "http://localhost:8000/process_text"
    url_refine = "http://localhost:8000/refine_text"
    
    print("=" * 70)
    print("TESTING ITERATIVE REFINEMENT LOOP")
    print("=" * 70)
    
    # Step 1: Initial AI suggestion
    print("\n[Step 1] Initial AI Processing")
    print("-" * 70)
    
    initial_payload = {
        "api_version": "v1",
        "text": "need to talk about project",
        "app": "email",
        "action": "formalize",
        "context": {
            "previous_text": "",
            "user_style": "formal"
        }
    }
    
    try:
        print(f"User input: '{initial_payload['text']}'")
        response = requests.post(url_process, json=initial_payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        first_output = result['result_text']
        
        print(f"AI Suggestion: '{first_output}'")
        print(f"Latency: {result['latency_ms']}ms | Confidence: {result['confidence']}")
        
        # Step 2: User provides feedback and refines
        print("\n[Step 2] User Refinement with Feedback")
        print("-" * 70)
        
        feedback = "Make it more polite and add a greeting"
        print(f"User feedback: '{feedback}'")
        
        refine_payload = {
            "api_version": "v1",
            "app": "email",
            "original_text": initial_payload['text'],
            "previous_output": first_output,
            "feedback": feedback
        }
        
        response = requests.post(url_refine, json=refine_payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        refined_output = result['result_text']
        
        print(f"Refined AI Output: '{refined_output}'")
        print(f"Latency: {result['latency_ms']}ms | Confidence: {result['confidence']}")
        
        # Step 3: Another refinement
        print("\n[Step 3] Second Refinement Iteration")
        print("-" * 70)
        
        feedback2 = "Make it shorter and more direct"
        print(f"User feedback: '{feedback2}'")
        
        refine_payload2 = {
            "api_version": "v1",
            "app": "email",
            "original_text": initial_payload['text'],
            "previous_output": refined_output,
            "feedback": feedback2
        }
        
        response = requests.post(url_refine, json=refine_payload2, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        final_output = result['result_text']
        
        print(f"Final AI Output: '{final_output}'")
        print(f"Latency: {result['latency_ms']}ms | Confidence: {result['confidence']}")
        
        print("\n" + "=" * 70)
        print("REFINEMENT SUMMARY")
        print("=" * 70)
        print(f"Original: '{initial_payload['text']}'")
        print(f"1st Pass: '{first_output}'")
        print(f"2nd Pass: '{refined_output}'")
        print(f"Final:    '{final_output}'")
        print("\nThe iterative refinement loop allows users to continuously")
        print("improve AI outputs until they're satisfied!")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Server not running!")
        print("Start server: uvicorn ai_engine.api_service:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_iterative_refinement()
