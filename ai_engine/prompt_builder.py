from ai_engine.schemas import ProcessTextRequest
from ai_engine.context_manager import context_manager

class PromptBuilder:
    """
    Constructs optimized prompts for the LLM based on intent, application type, and context.
    Includes iterative refinement support using conversation history.
    """
    
    # Advanced prompt templates with specific strategies
    PROMPT_TEMPLATES = {
        "rewrite": {
            "instruction": "Rewrite the following text to improve clarity, flow, and readability while preserving the original meaning.",
            "strategy": "Focus on: sentence structure, word choice, and natural flow. Remove redundancy."
        },
        "formalize": {
            "instruction": "Transform the following text into a highly formal and professional version.",
            "strategy": "Use formal vocabulary, complete sentences, professional tone. Avoid contractions and casual language."
        },
        "expand": {
            "instruction": "Expand the following text by adding relevant details, context, and explanations.",
            "strategy": "Add supporting details, examples, or elaboration while maintaining coherence. Don't change the core message."
        },
        "summarize": {
            "instruction": "Create a concise summary of the following text, capturing the key points.",
            "strategy": "Extract main ideas, remove redundancy, maintain essential information. Be brief but complete."
        },
        "autocomplete": {
            "instruction": "Complete the text with a SHORT, direct continuation (5-15 words max). NO quotes, NO explanations.",
            "strategy": "Like VS Code Copilot: natural inline completion that flows from the typed text. Simple, concise, unquoted."
        }
    }
    
    @staticmethod
    def build_prompt(request: ProcessTextRequest, use_history: bool = True) -> str:
        intent = request.action.lower()
        app_type = request.app
        original_text = request.text
        style = request.context.user_style
        previous_text = request.context.previous_text
        
        # Special ultra-minimal prompt for autocomplete (VS Code style)
        if intent == "autocomplete":
            return f"""Complete this text naturally and concisely (5-10 words max). Write as if you're continuing the sentence.

Examples:
- "what is" → "the meaning of life"
- "how to" → "bake a chocolate cake"
- "define human" → "being or member of homo sapiens"

Text: {original_text}
Completion:"""
        
        # Get template for other intents
        template = PromptBuilder.PROMPT_TEMPLATES.get(intent, PromptBuilder.PROMPT_TEMPLATES["rewrite"])
        
        # Build context-aware prompt
        prompt = f"""You are an expert AI writing assistant for {app_type} applications.

Task: {template['instruction']}
Style: {style}
Strategy: {template['strategy']}
"""
        
        # Add conversation history for iterative refinement
        if use_history:
            history = context_manager.get_history(request.app)
            if history:
                prompt += "\nPrevious Interactions (for context):\n"
                for i, interaction in enumerate(history[-3:], 1):  # Last 3 interactions
                    prompt += f"{i}. Input: \"{interaction['input']}\" → Output: \"{interaction['output']}\"\n"
        
        # Add immediate context
        if previous_text:
            prompt += f"\nPrevious Text: \"{previous_text}\"\n"
        
        # Add the current input
        prompt += f"\nCurrent Input: \"{original_text}\"\n"
        prompt += "\nOutput (only the processed text, no explanations):"
        
        return prompt
