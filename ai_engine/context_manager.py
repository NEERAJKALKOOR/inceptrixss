import threading
from typing import Dict, Any

class ContextManager:
    """
    Manages in-memory context for the AI Engine.
    No disk persistence as per requirements.
    """
    def __init__(self):
        self._context_store: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def update_context(self, session_id: str, data: dict):
        with self._lock:
            if session_id not in self._context_store:
                self._context_store[session_id] = {"history": []}
            self._context_store[session_id].update(data)

    def add_interaction(self, session_id: str, user_text: str, ai_response: str):
        """Stores the interaction for the iterative refinement loop."""
        with self._lock:
            if session_id not in self._context_store:
                self._context_store[session_id] = {"history": []}
            history = self._context_store[session_id].setdefault("history", [])
            history.append({"input": user_text, "output": ai_response})
            # Keep only last 5 iterations to prevent context bloat and optimize latency
            if len(history) > 5:
                self._context_store[session_id]["history"] = history[-5:]

    def get_history(self, session_id: str) -> list:
        with self._lock:
            return self._context_store.get(session_id, {}).get("history", [])

    def get_context(self, session_id: str) -> dict:
        with self._lock:
            return self._context_store.get(session_id, {})

    def clear_context(self, session_id: str):
        with self._lock:
            if session_id in self._context_store:
                del self._context_store[session_id]

# Singleton instance for the service
context_manager = ContextManager()
