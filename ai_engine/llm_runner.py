import time
import requests
import json
from ai_engine.config import MOCK_MODE, OLLAMA_URL, OLLAMA_MODEL

class LLMRunner:
    """
    Handles local LLM inference (e.g., via Ollama).
    Includes a mock mode for deterministic output and integration testing.
    Optimizes model selection and latency based on task complexity.
    """
    def __init__(self, mock_mode: bool = MOCK_MODE):
        self.mock_mode = mock_mode
        
    def select_model(self, action: str, text_length: int) -> str:
        """
        Optimize model selection based on task complexity.
        For simple tasks, use faster/smaller models.
        """
        # Simple heuristic: use smaller models for autocomplete and short texts
        if action == "autocomplete" and text_length < 50:
            return "llama3.2:latest"  # Fast model for quick suggestions
        elif action in ["summarize", "rewrite"] and text_length < 100:
            return "llama3.2:latest"
        else:
            return OLLAMA_MODEL  # Default model for complex tasks

    def generate(self, prompt: str, original_request: dict) -> tuple[str, float, int]:
        """
        Runs the generation with optimized model selection.
        Returns: (generated_text, confidence, latency_ms)
        """
        start_time = time.time()

        if self.mock_mode:
            return self._run_mock(original_request, start_time)
        return self._run_ollama(prompt, start_time, original_request)

    def _run_mock(self, request: dict, start_time: float) -> tuple[str, float, int]:
        # Deterministic responses for testing based on intent
        time.sleep(0.1) # Simulate some processing time
        action = request.get("action", "rewrite")
        input_text = request.get("text", "")
        
        mock_responses = {
            "rewrite": f"Rewritten: {input_text}",
            "formalize": f"Please find the formalized version: {input_text}",
            "expand": f"{input_text} Furthermore, this is expanded for clarity.",
            "summarize": f"Summary of: {input_text}",
            "autocomplete": f"{input_text} and then some more."
        }
        
        # Hardcoded matching for tests
        if input_text.lower() == "schedule a meeting":
             result_text = "Please let me know your availability next week."
        else:
             result_text = mock_responses.get(action, f"Processed: {input_text}")
             
        latency_ms = int((time.time() - start_time) * 1000)
        confidence = 0.92
        
        return result_text, confidence, latency_ms

    def _run_ollama(self, prompt: str, start_time: float, request_data: dict = None) -> tuple[str, float, int]:
        # Dynamic model selection for latency optimization
        action = request_data.get("action", "rewrite") if request_data else "rewrite"
        text_length = len(request_data.get("text", "")) if request_data else 0
        selected_model = self.select_model(action, text_length)
        
        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3 if action == "autocomplete" else 0.7,  # Low temp for focused completions
                "top_p": 0.9,
                "num_predict": 30 if action == "autocomplete" else 500  # Very short for VS Code style
            }
        }
        try:
            # Reduced timeout for better responsiveness
            response = requests.post(OLLAMA_URL, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            result_text = result.get("response", "").strip()
            
            # Clean up AI output - remove echoed prompt parts
            result_text = self._clean_ai_output(result_text)
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Confidence based on response quality indicators
            confidence = 0.88
            if latency_ms < 1000:  # Fast response
                confidence = 0.92
            elif latency_ms > 5000:  # Slow response might indicate complexity
                confidence = 0.80
            
            return result_text, confidence, latency_ms
        except Exception as e:
            # Fallback in case Ollama is not running but mock mode is off
            latency_ms = int((time.time() - start_time) * 1000)
            return f"Error connecting to LLM: {str(e)}", 0.0, latency_ms
    
    def _clean_ai_output(self, text: str) -> str:
        """Remove echoed prompt parts and extract only the final output"""
        # If AI echoed the prompt with "Output:" or similar markers
        markers = ["Output:", "Result:", "Improved text:", "Final text:", "Response:"]
        for marker in markers:
            if marker in text:
                # Take everything after the last occurrence of the marker
                text = text.split(marker)[-1].strip()
        
        # Remove any remaining prompt artifacts
        lines = text.split('\n')
        cleaned_lines = []
        skip_mode = False
        
        for line in lines:
            line_lower = line.lower().strip()
            # Skip lines that look like prompt instructions
            if any(phrase in line_lower for phrase in [
                "you are helping", "context:", "tone:", "task:", "input text:", 
                "provide only", "output only", "return only", "formality:"
            ]):
                skip_mode = True
                continue
            # Reset skip mode when we see actual content
            if line.strip() and not skip_mode:
                cleaned_lines.append(line)
            elif skip_mode and line.strip() and line_lower[0].isalnum():
                # Looks like actual content starting
                skip_mode = False
                cleaned_lines.append(line)
        
        # Join and clean
        result = '\n'.join(cleaned_lines).strip()
        
        # Remove surrounding quotes if present
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        if result.startswith("'") and result.endswith("'"):
            result = result[1:-1]
        
        return result.strip()

llm_runner = LLMRunner()
