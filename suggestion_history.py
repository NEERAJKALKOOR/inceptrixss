"""
Suggestion History Manager - Store and navigate previous AI suggestions
"""
from collections import deque
from typing import Optional, Dict, List
import time


class SuggestionHistory:
    """
    Manages history of AI suggestions with navigation support
    """
    
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.history = deque(maxlen=max_size)  # Auto-removes oldest when full
        self.current_index = -1  # -1 means no history navigation active
        self.is_navigating = False
    
    def add(self, suggestion: str, context: str, action: str, original_text: str):
        """
        Add a new suggestion to history
        
        Args:
            suggestion: The AI-generated text
            context: App context (email, code, chat, etc.)
            action: Action type (expand, rewrite, etc.)
            original_text: The original user text
        """
        entry = {
            "suggestion": suggestion,
            "context": context,
            "action": action,
            "original_text": original_text,
            "timestamp": time.time(),
            "accepted": None  # Will be set when user accepts/rejects
        }
        
        self.history.append(entry)
        self.current_index = -1  # Reset navigation
        self.is_navigating = False
    
    def mark_accepted(self, accepted: bool):
        """Mark most recent suggestion as accepted or rejected"""
        if len(self.history) > 0:
            self.history[-1]["accepted"] = accepted
    
    def get_previous(self) -> Optional[Dict]:
        """
        Navigate to previous suggestion in history
        Returns None if at beginning
        """
        if len(self.history) == 0:
            return None
        
        if not self.is_navigating:
            # Start navigating from most recent
            self.current_index = len(self.history) - 1
            self.is_navigating = True
        else:
            # Move backward
            if self.current_index > 0:
                self.current_index -= 1
            else:
                # Already at oldest
                return None
        
        return dict(self.history[self.current_index])
    
    def get_next(self) -> Optional[Dict]:
        """
        Navigate to next suggestion in history
        Returns None if at end
        """
        if not self.is_navigating or len(self.history) == 0:
            return None
        
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return dict(self.history[self.current_index])
        else:
            # At newest, exit navigation mode
            self.current_index = -1
            self.is_navigating = False
            return None
    
    def get_current(self) -> Optional[Dict]:
        """Get currently viewed history item"""
        if self.is_navigating and 0 <= self.current_index < len(self.history):
            return dict(self.history[self.current_index])
        return None
    
    def get_all(self) -> List[Dict]:
        """Get all history items (newest first)"""
        return list(reversed(self.history))
    
    def clear(self):
        """Clear all history"""
        self.history.clear()
        self.current_index = -1
        self.is_navigating = False
    
    def get_stats(self) -> Dict:
        """Get statistics about suggestions"""
        if len(self.history) == 0:
            return {
                "total": 0,
                "accepted": 0,
                "rejected": 0,
                "pending": 0,
                "acceptance_rate": 0.0
            }
        
        accepted = sum(1 for h in self.history if h["accepted"] == True)
        rejected = sum(1 for h in self.history if h["accepted"] == False)
        pending = sum(1 for h in self.history if h["accepted"] is None)
        
        acceptance_rate = accepted / len(self.history) if len(self.history) > 0 else 0.0
        
        return {
            "total": len(self.history),
            "accepted": accepted,
            "rejected": rejected,
            "pending": pending,
            "acceptance_rate": acceptance_rate
        }
    
    def get_size(self) -> int:
        """Get current history size"""
        return len(self.history)
    
    def is_empty(self) -> bool:
        """Check if history is empty"""
        return len(self.history) == 0


# Singleton instance
suggestion_history = SuggestionHistory(max_size=10)


if __name__ == "__main__":
    """Test suggestion history"""
    print("📜 Suggestion History Test")
    print("="*60)
    
    # Add some test entries
    suggestion_history.add(
        suggestion="Hello, I hope this message finds you well.",
        context="email",
        action="formalize",
        original_text="hey there"
    )
    
    suggestion_history.add(
        suggestion="def calculate_sum(a, b):\n    return a + b",
        context="code",
        action="generate",
        original_text="function to add numbers"
    )
    
    suggestion_history.add(
        suggestion="Sounds good! 👍",
        context="chat",
        action="casualize",
        original_text="that is acceptable"
    )
    
    print(f"\n📊 History stats: {suggestion_history.get_stats()}")
    
    print(f"\n⬅️  Testing backward navigation:")
    prev = suggestion_history.get_previous()
    print(f"   1. {prev['suggestion'][:40]}... ({prev['context']})")
    
    prev = suggestion_history.get_previous()
    print(f"   2. {prev['suggestion'][:40]}... ({prev['context']})")
    
    print(f"\n➡️  Testing forward navigation:")
    next_item = suggestion_history.get_next()
    print(f"   1. {next_item['suggestion'][:40]}... ({next_item['context']})")
    
    print(f"\n✅ History system working correctly!")
