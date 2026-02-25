from fastapi import FastAPI, HTTPException
from ai_engine.schemas import ProcessTextRequest, ProcessTextResponse, RefineTextRequest
from ai_engine.context_manager import context_manager
from ai_engine.intent_detector import IntentDetector
from ai_engine.prompt_builder import PromptBuilder
from ai_engine.llm_runner import llm_runner
import time

app = FastAPI(
    title="Always-On AI Keyboard Engine",
    description="Standalone local AI engine service for an Always-On AI Keyboard.",
    version="1.0.0"
)

@app.post("/process_text", response_model=ProcessTextResponse)
def process_text(request: ProcessTextRequest):
    try:
        # 1. Manage Context (RAM-only)
        # Using app type as a session identifier for simplistic scoping
        context_manager.update_context(request.app, request.context.model_dump())
        
        # 2. Intent Detection
        intent = IntentDetector.detect_intent(request.action)
        request.action = intent # Normalize intent
        
        # 3. Prompt Construction with history
        prompt = PromptBuilder.build_prompt(request, use_history=True)
        
        # 4. Offline LLM Inference with optimized model selection
        # Request dict needed for mock mode logic
        result_text, confidence, latency_ms = llm_runner.generate(prompt, request.model_dump())
        
        # 5. Store interaction for iterative refinement
        context_manager.add_interaction(request.app, request.text, result_text)
        
        # 6. Return Structured Output
        output = ProcessTextResponse(
            api_version=request.api_version,
            result_text=result_text,
            confidence=confidence,
            latency_ms=latency_ms
        )
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine_text", response_model=ProcessTextResponse)
def refine_text(request: RefineTextRequest):
    """
    Iterative refinement endpoint: User can refine previous AI output based on feedback.
    This enables the iterative refinement loop.
    """
    try:
        # Build refinement prompt with feedback
        history = context_manager.get_history(request.app)
        
        prompt = f"""You are refining a previous AI output based on user feedback.

Original Input: \"{request.original_text}\"
Previous AI Output: \"{request.previous_output}\"
User Feedback: \"{request.feedback}\"

Task: Improve the output based on the feedback while maintaining the original intent.
Output (only the refined text):"""
        
        # Generate refined version
        result_text, confidence, latency_ms = llm_runner.generate(prompt, request.model_dump())
        
        # Update history with refined version
        context_manager.add_interaction(request.app, request.original_text, result_text)
        
        return ProcessTextResponse(
            api_version=request.api_version,
            result_text=result_text,
            confidence=confidence,
            latency_ms=latency_ms
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear_context/{app_name}")
def clear_context(app_name: str):
    """Clear conversation history for a specific app."""
    context_manager.clear_context(app_name)
    return {"status": "success", "message": f"Context cleared for {app_name}"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "mode": "mock" if llm_runner.mock_mode else "ollama"}
