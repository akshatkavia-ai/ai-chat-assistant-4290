# AI Copilot Backend

FastAPI backend service for the AI Copilot application. Handles chat requests from the frontend and communicates with the Gemini API to generate AI responses.

## Overview

This backend service provides REST API endpoints for:
- Health checks
- AI chat interactions powered by Gemini API
- CORS support for frontend integration

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Gemini API key (get one from https://makersuite.google.com/app/apikey)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the `.env.example` file to create your `.env` file:

```bash
cp .env.example .env
```

Edit the `.env` file and configure the following variables:

#### Required Environment Variables

- **`GEMINI_API_KEY`**: Your Google Gemini API key (required for AI responses)
  - Get your API key from: https://makersuite.google.com/app/apikey
  - This is **required** for the application to work

#### Optional Environment Variables

- **`FRONTEND_ORIGIN`**: URL of your frontend application for CORS configuration
  - Default: `http://localhost:3000`
  - Change this to match your frontend URL in production
  - Example: `FRONTEND_ORIGIN=http://localhost:3000`

#### Future Features (Not Currently Used)

The following Supabase variables are **optional** and not currently used by the application. They are placeholders for future features like chat history logging and user data persistence:

- **`SUPABASE_URL`**: Your Supabase project URL (optional)
- **`SUPABASE_ANON_KEY`**: Your Supabase anonymous key (optional)

**Note:** The application will work perfectly without Supabase configuration. No persistence or logging features are currently implemented.

#### Example .env File

```
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Frontend CORS configuration
FRONTEND_ORIGIN=http://localhost:3000

# Optional - Future Supabase integration
SUPABASE_URL=
SUPABASE_ANON_KEY=
```

### 3. Run the Server

Start the FastAPI server:

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

**Important:** The backend runs on port **3001** by default to match the frontend configuration.

The API will be available at `http://localhost:3001`

## How the Chat Flow Works

### 1. Frontend to Backend Communication

The frontend (React app) sends chat messages to the backend via HTTP POST requests to `/api/chat`:

```
Frontend (http://localhost:3000)
    ↓
POST /api/chat
    ↓
Backend (http://localhost:3001)
```

### 2. Request Format

The frontend sends a JSON payload containing:
- **message**: The user's current message
- **history** (optional): Previous conversation messages for context

Example request:
```json
{
  "message": "What is machine learning?",
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help you today?"}
  ]
}
```

### 3. Backend Processing

1. Backend validates the `GEMINI_API_KEY` is configured
2. Converts the request into Gemini API format
3. Sends the message and history to Google's Gemini API
4. Receives the AI-generated response
5. Returns the response to the frontend

```
Backend
    ↓
Gemini API (https://generativelanguage.googleapis.com)
    ↓
AI Response
    ↓
Backend
    ↓
Frontend
```

### 4. Response Format

The backend returns a JSON response:
```json
{
  "reply": "Machine learning is a subset of artificial intelligence..."
}
```

### 5. CORS Configuration

The backend is configured to accept requests from the frontend origin specified in `FRONTEND_ORIGIN`:
- Default: `http://localhost:3000`
- Allows POST, GET, and OPTIONS methods
- Enables credentials for secure communication

## API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: `http://localhost:3001/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:3001/redoc`
- **OpenAPI specification**: `http://localhost:3001/openapi.json`

## API Endpoints

### GET /

Health check endpoint to verify the service is running.

**Response:**
```json
{
  "message": "Healthy"
}
```

### POST /api/chat

Chat endpoint for AI interactions.

**Request Body:**
```json
{
  "message": "string (required)",
  "history": [
    {
      "role": "user|assistant",
      "content": "string"
    }
  ]
}
```

**Response:**
```json
{
  "reply": "string"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request format
- `500`: Server error or API configuration issue
- `503`: AI service unavailable

## Project Structure

```
ai_copilot_backend/
├── src/
│   ├── __init__.py
│   ├── models.py              # Pydantic models for request/response
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application and routes
│   │   └── generate_openapi.py  # OpenAPI schema generator
│   └── services/
│       ├── __init__.py
│       ├── gemini.py          # Gemini API integration
│       └── supabase_client.py # Optional Supabase client (future use)
├── interfaces/
│   └── openapi.json           # Generated API specification
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # This file
```

## Development

### Code Quality

The project uses flake8 for linting. Configuration is in `.flake8`:

```bash
flake8 src/
```

### Testing

Run tests with pytest:

```bash
pytest
```

### Generate OpenAPI Specification

The OpenAPI spec is automatically generated. To manually regenerate:

```bash
python -m src.api.generate_openapi
```

This creates/updates `interfaces/openapi.json`.

## Connecting Frontend and Backend

To ensure proper communication between frontend and backend:

1. **Backend Configuration** (this service):
   - Set `FRONTEND_ORIGIN=http://localhost:3000` in `.env`
   - Run backend on port `3001`: `uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001`

2. **Frontend Configuration** (React app):
   - Set `REACT_APP_BACKEND_URL=http://localhost:3001` in frontend's `.env`
   - Run frontend on port `3000`: `npm start`

3. **Verify CORS**:
   - Backend logs will show: `CORS configured for origin: http://localhost:3000`
   - Check browser console for any CORS errors

## Future Enhancements

### Supabase Integration (Not Yet Implemented)

The `src/services/supabase_client.py` module provides a placeholder for optional Supabase integration. When implemented, this could enable:

- **Chat History**: Store conversation history in Supabase database
- **User Profiles**: Manage user preferences and settings
- **Analytics**: Track usage patterns and popular queries

To enable Supabase in the future:
1. Install the Supabase Python client: `pip install supabase`
2. Set `SUPABASE_URL` and `SUPABASE_ANON_KEY` in your `.env` file
3. Update `supabase_client.py` to initialize the Supabase client
4. Implement data persistence logic in your API routes (see comments in `src/services/gemini.py`)

Currently, `get_supabase_client()` returns `None` if credentials are not configured, allowing the app to run without any database backend.

## Troubleshooting

### "AI service is not configured" error

- Verify `GEMINI_API_KEY` is set in your `.env` file
- Ensure the `.env` file is in the `ai_copilot_backend/` directory
- Restart the server after updating `.env`

### CORS errors in browser console

- Check that `FRONTEND_ORIGIN` matches your frontend URL exactly
- Ensure there are no trailing slashes in the URL
- Restart the backend after changing CORS configuration

### "Failed to connect to AI service" error

- Verify your internet connection
- Check that the Gemini API key is valid
- Visit https://makersuite.google.com/app/apikey to verify your key

### Import errors when running the server

- Ensure you're in the correct directory (the directory containing `src/`)
- Run `pip install -r requirements.txt` to ensure all dependencies are installed
- Use Python 3.8 or higher

## Security Notes

- **Never commit your `.env` file to version control**
- Keep your `GEMINI_API_KEY` secure and rotate it regularly
- Use environment-specific `.env` files for development, staging, and production
- In production, use proper secret management (e.g., AWS Secrets Manager, Azure Key Vault)

## Support

For issues or questions, please refer to the main project documentation or check the API documentation at `/docs` when the server is running.
