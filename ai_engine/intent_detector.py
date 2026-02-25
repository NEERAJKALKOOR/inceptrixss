class IntentDetector:
    """
    Detects and validates the intent of the request.
    Supported actions: rewrite, formalize, expand, summarize, autocomplete
    """
    SUPPORTED_INTENTS = {"rewrite", "formalize", "expand", "summarize", "autocomplete"}

    @staticmethod
    def detect_intent(action: str) -> str:
        intent = action.lower()
        if intent not in IntentDetector.SUPPORTED_INTENTS:
             # Fallback to rewrite if unknown
             return "rewrite"
        return intent
