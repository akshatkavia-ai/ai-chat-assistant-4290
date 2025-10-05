"""
Chat Models

Pydantic models for chat request and response validation.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """
    Represents a single chat message in the conversation history.
    
    Attributes:
        role: The role of the message sender ('user' or 'assistant')
        content: The text content of the message
    """
    role: Literal['user', 'assistant'] = Field(
        ...,
        description="Role of the message sender"
    )
    content: str = Field(
        ...,
        description="Text content of the message"
    )


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Attributes:
        message: The user's current message
        history: Optional list of previous chat messages for context
    """
    message: str = Field(
        ...,
        description="The user's current message to send to the AI"
    )
    history: Optional[List[ChatMessage]] = Field(
        None,
        description="Optional conversation history for context"
    )


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Attributes:
        reply: The AI-generated response text
    """
    reply: str = Field(
        ...,
        description="The AI-generated response to the user's message"
    )
