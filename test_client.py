import requests
import json

def test_api():
    url = "http://localhost:8000/process_text"
    payload = {
        "api_version": "v1",
        "text": "what is mass meaning",
        "app": "email",
        "action": "suggestion",
        "context": {
            "previous_text": "",
            "user_style": "formal"
        }
    }

    try:
        print("Sending request to AI Engine...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        print("\nResponse received:")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server.")
        print("Make sure the FastAPI service is running using: uvicorn ai_engine.api_service:app --reload")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    test_api()
