"""Schema classes for application structures."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Role(Enum):
    """Enum for message roles."""
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    """Represents a message in the conversation."""
    role: Literal[Role.USER, Role.ASSISTANT] = Field(
        ..., description="The role of the message sender (user or assistant).")
    content: str = Field(..., description="The content of the message.")
