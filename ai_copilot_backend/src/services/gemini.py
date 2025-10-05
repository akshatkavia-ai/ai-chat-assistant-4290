"""
Gemini AI Service

This module handles communication with Google's Gemini API for generating
AI responses to user messages. It uses the REST API endpoint with httpx.

The service supports conversation history to maintain context across multiple
messages in a chat session.
"""

import logging
from typing import Dict, List, Optional

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_MODEL = "gemini-1.5-flash"


# PUBLIC_INTERFACE
async def generate_reply(
    message: str,
    api_key: str,
    history: Optional[List[Dict]] = None
) -> str:
    """
    Generate an AI reply using the Gemini API.
    
    This function sends a user message (with optional conversation history)
    to the Gemini API and returns the AI-generated response.
    
    Args:
        message: The current user message to send to the AI
        api_key: The Gemini API key for authentication
        history: Optional list of previous messages for context.
                Each item should be a dict with 'role' and 'content' keys.
    
    Returns:
        str: The AI-generated response text
        
    Raises:
        HTTPException: If the API call fails or returns an error
        
    Example:
        >>> reply = await generate_reply(
        ...     message="Hello, how are you?",
        ...     api_key="your-api-key",
        ...     history=[{"role": "user", "content": "Hi"}]
        ... )
    
    Note:
        Future enhancement: Add a call to Supabase here to log the conversation
        for analytics or chat history features.
    """
    if not api_key:
        logger.error("Gemini API key is missing")
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured"
        )
    
    # Build the API endpoint URL
    endpoint = f"{GEMINI_API_BASE}/{GEMINI_MODEL}:generateContent"
    
    # Build the request payload
    contents = []
    
    # Add conversation history if provided
    if history:
        for msg in history:
            contents.append({
                "role": msg.get("role"),
                "parts": [{"text": msg.get("content")}]
            })
    
    # Add the current user message
    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })
    
    payload = {
        "contents": contents
    }
    
    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                endpoint,
                params={"key": api_key},
                json=payload
            )
            
            # Check for HTTP errors
            if response.status_code != 200:
                logger.error(
                    f"Gemini API error: {response.status_code} - {response.text}"
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Gemini API error: {response.text}"
                )
            
            # Parse the response
            response_data = response.json()
            
            # Extract the reply text
            try:
                reply_text = (
                    response_data
                    .get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                )
                
                if not reply_text:
                    logger.warning("Empty reply from Gemini API")
                    raise HTTPException(
                        status_code=500,
                        detail="Received empty response from AI"
                    )
                
                # TODO: Add Supabase logging here
                # Example:
                # supabase_client = get_supabase_client()
                # if supabase_client:
                #     await log_conversation(supabase_client, message, reply_text)
                
                return reply_text
                
            except (KeyError, IndexError, TypeError) as e:
                logger.error(f"Error parsing Gemini response: {e}")
                logger.debug(f"Response data: {response_data}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to parse AI response"
                )
                
    except httpx.RequestError as e:
        logger.error(f"Network error calling Gemini API: {e}")
        raise HTTPException(
            status_code=503,
            detail="Failed to connect to AI service"
        )
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_reply: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
