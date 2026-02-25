"""
AI Integration Layer
Communicates with the AI engine via HTTP or mock responses
"""
import requests
import json
from typing import Dict, Any
from ui_module.config import AI_ENGINE_URL, MOCK_MODE


class AIIntegration:
    """
    Handles communication with the AI engine.
    Supports both real API calls and mock mode for testing.
    """
    
    def __init__(self, mock_mode: bool = MOCK_MODE):
        self.mock_mode = mock_mode
        self.ai_url = AI_ENGINE_URL
        
    def process_text(self, text: str, action: str = "autocomplete", 
                    app: str = "general", context: Dict = None) -> Dict[str, Any]:
        """
        Send text to AI engine for processing.
        
        Args:
            text: Input text to process
            action: AI action (rewrite, formalize, expand, summarize, autocomplete)
            app: Application context
            context: Additional context (previous_text, user_style, etc.)
            
        Returns:
            AI response dict with result_text, confidence, etc.
        """
        if self.mock_mode:
            return self._mock_ai_response(text, action)
        
        return self._call_ai_engine(text, action, app, context)
    
    def _call_ai_engine(self, text: str, action: str, app: str, context: Dict) -> Dict[str, Any]:
        """Call the real AI engine API"""
        if context is None:
            context = {"previous_text": "", "user_style": "default"}
        
        payload = {
            "api_version": "v1",
            "text": text,
            "app": app,
            "action": action,
            "context": context
        }
        
        try:
            response = requests.post(self.ai_url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            # Normalize response format
            return {
                "api_version": result.get("api_version", "v1"),
                "result_text": result.get("result_text", ""),
                "confidence": result.get("confidence", 0.5),
                "intent": action,
                "status": "success"
            }
            
        except requests.exceptions.ConnectionError:
            return {
                "api_version": "v1",
                "result_text": "[AI Engine not available]",
                "confidence": 0.0,
                "intent": action,
                "status": "error"
            }
        except Exception as e:
            return {
                "api_version": "v1",
                "result_text": f"[Error: {str(e)}]",
                "confidence": 0.0,
                "intent": action,
                "status": "error"
            }
    
    def _mock_ai_response(self, text: str, action: str) -> Dict[str, Any]:
        """Generate mock AI responses for testing"""
        
        mock_responses = {
            "autocomplete": f"{text} and continue with relevant details.",
            "rewrite": f"Here is a better version: {text}",
            "formalize": f"Formal version: {text.capitalize()}.",
            "expand": f"{text} Furthermore, this can be expanded with more context and details to provide a comprehensive understanding.",
            "summarize": f"Summary: {text[:30]}..." if len(text) > 30 else f"Summary: {text}"
        }
        
        result_text = mock_responses.get(action, f"Processed: {text}")
        
        # Simulate varying confidence
        confidence = 0.92 if len(text) > 10 else 0.75
        
        return {
            "api_version": "v1",
            "result_text": result_text,
            "confidence": confidence,
            "intent": action,
            "status": "success"
        }
    
    def refine_with_voice(self, original_text: str, voice_input: str, 
                         previous_output: str = None) -> Dict[str, Any]:
        """
        Hybrid voice + text refinement.
        Voice commands refine existing typed content.
        
        Args:
            original_text: User's original typed text
            voice_input: Transcribed voice command
            previous_output: Previous AI output (if any)
            
        Returns:
            Refined AI response
        """
        if self.mock_mode:
            return {
                "api_version": "v1",
                "result_text": f"{original_text} [refined with voice: {voice_input}]",
                "confidence": 0.88,
                "intent": "voice_refine",
                "status": "success"
            }
        
        # Build refinement request
        feedback = f"Apply this voice command: {voice_input}"
        
        refine_payload = {
            "api_version": "v1",
            "app": "voice_refine",
            "original_text": original_text,
            "previous_output": previous_output or original_text,
            "feedback": feedback
        }
        
        try:
            # Call /refine_text endpoint
            refine_url = self.ai_url.replace("/process_text", "/refine_text")
            response = requests.post(refine_url, json=refine_payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "api_version": "v1",
                "result_text": result.get("result_text", original_text),
                "confidence": result.get("confidence", 0.8),
                "intent": "voice_refine",
                "status": "success"
            }
            
        except Exception as e:
            return {
                "api_version": "v1",
                "result_text": f"[Voice refinement error: {str(e)}]",
                "confidence": 0.0,
                "intent": "voice_refine",
                "status": "error"
            }


# Singleton instance
ai_integration = AIIntegration()
