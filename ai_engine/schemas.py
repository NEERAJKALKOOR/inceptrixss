from pydantic import BaseModel, Field
from typing import Optional

class RequestContext(BaseModel):
    previous_text: str = ""
    user_style: str = "default"

class ProcessTextRequest(BaseModel):
    api_version: str = Field(..., example="v1")
    text: str = Field(..., example="schedule a meeting")
    app: str = Field(..., example="email")
    action: str = Field(..., example="rewrite")
    context: RequestContext

class RefineTextRequest(BaseModel):
    """Schema for iterative refinement requests."""
    api_version: str = Field(..., example="v1")
    app: str = Field(..., example="email")
    original_text: str = Field(..., example="schedule a meeting")
    previous_output: str = Field(..., example="Let's schedule a meeting.")
    feedback: str = Field(..., example="Make it more formal and polite")

class ProcessTextResponse(BaseModel):
    api_version: str = Field(..., example="v1")
    result_text: str = Field(..., example="Please let me know your availability next week.")
    confidence: float = Field(..., example=0.92)
    latency_ms: int = Field(..., example=420)
