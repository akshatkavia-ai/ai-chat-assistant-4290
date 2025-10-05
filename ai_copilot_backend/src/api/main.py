"""
AI Copilot Backend API

FastAPI application providing REST endpoints for AI chat functionality.
Integrates with Google's Gemini API for generating AI responses.
"""

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.models import ChatRequest, ChatResponse
from src.services.gemini import generate_reply

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata for OpenAPI documentation
app = FastAPI(
    title="AI Copilot Backend API",
    description="Backend service for AI chat powered by Gemini API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoints"
        },
        {
            "name": "chat",
            "description": "AI chat endpoints powered by Gemini"
        }
    ]
)

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

# Validate required environment variables
if not GEMINI_API_KEY:
    logger.warning(
        "GEMINI_API_KEY not found in environment. "
        "Chat functionality will not work until this is configured."
    )

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS", "GET"],
    allow_headers=["*"],
)

logger.info(f"CORS configured for origin: {FRONTEND_ORIGIN}")


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["health"],
    summary="Health Check",
    description="Returns the health status of the API service",
    response_description="Health status message"
)
def health_check():
    """
    Health check endpoint.
    
    Returns a simple message indicating the service is running.
    Useful for monitoring and load balancer health checks.
    
    Returns:
        dict: A dictionary with a health status message
    """
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["chat"],
    summary="Chat with AI",
    description="Send a message to the AI and receive a response. "
                "Optionally include conversation history for context.",
    responses={
        200: {
            "description": "Successful response with AI-generated reply",
            "content": {
                "application/json": {
                    "example": {"reply": "Hello! How can I help you today?"}
                }
            }
        },
        400: {
            "description": "Invalid request format"
        },
        500: {
            "description": "Server error or API configuration issue"
        },
        503: {
            "description": "AI service unavailable"
        }
    }
)
async def chat(request: ChatRequest):
    """
    Chat endpoint for AI interactions.
    
    This endpoint accepts a user message and optional conversation history,
    sends it to the Gemini API, and returns the AI-generated response.
    
    Args:
        request: ChatRequest containing the message and optional history
        
    Returns:
        ChatResponse: Contains the AI-generated reply
        
    Raises:
        HTTPException: If GEMINI_API_KEY is not configured or API call fails
        
    Example request:
        POST /api/chat
        {
            "message": "What is machine learning?",
            "history": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi! How can I help?"}
            ]
        }
    
    Example response:
        {
            "reply": "Machine learning is a subset of artificial intelligence..."
        }
    
    Note:
        Future enhancement: This is where we can add Supabase logging to persist
        chat conversations for analytics or history features. The generate_reply
        function already has a placeholder comment for this integration.
    """
    # Validate API key is configured
    if not GEMINI_API_KEY:
        logger.error("Chat endpoint called but GEMINI_API_KEY not configured")
        raise HTTPException(
            status_code=500,
            detail="AI service is not configured. Please contact administrator."
        )
    
    try:
        # Convert history to dict format if provided
        history_dict = None
        if request.history:
            history_dict = [
                {"role": msg.role, "content": msg.content}
                for msg in request.history
            ]
        
        # Generate AI response
        logger.info(f"Processing chat request with message length: {len(request.message)}")
        reply_text = await generate_reply(
            message=request.message,
            api_key=GEMINI_API_KEY,
            history=history_dict
        )
        
        logger.info("Successfully generated AI response")
        
        # Return the response
        return ChatResponse(reply=reply_text)
        
    except HTTPException:
        # Re-raise HTTP exceptions from generate_reply
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
