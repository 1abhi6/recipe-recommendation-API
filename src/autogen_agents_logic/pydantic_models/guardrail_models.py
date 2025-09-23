from pydantic import BaseModel, Field
from typing import Optional

class GuardrailPydanticModel(BaseModel):
    status: bool = Field(..., description="Whether the guardrail failed or passed")
    message: Optional[str] = Field(description="Message according to status")
    