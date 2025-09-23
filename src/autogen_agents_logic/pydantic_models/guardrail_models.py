from pydantic import BaseModel, Field
from typing import Optional

class InputGuardrailPydanticModel(BaseModel):
    status: bool = Field(..., description="Whether the user input is within the scope of the application")
    message: Optional[str] = Field(description="Text to be returned to the user")
    