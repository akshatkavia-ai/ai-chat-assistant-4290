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
- Gemini API key

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

Edit the `.env` file and add your configuration:

#### Required Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required for AI responses)

#### Optional Environment Variables

The following Supabase variables are **optional** and not currently used by the application. They are placeholders for future features like chat history logging and user data persistence:

- `SUPABASE_URL`: Your Supabase project URL (optional)
- `SUPABASE_ANON_KEY`: Your Supabase anonymous key (optional)

**Note:** The application will work perfectly without Supabase configuration. No persistence or logging features are currently implemented.

### 3. Run the Server

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`
- OpenAPI specification: `http://localhost:8000/openapi.json`

## Project Structure

```
ai_copilot_backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application and routes
│   │   └── generate_openapi.py  # OpenAPI schema generator
│   └── services/
│       └── supabase_client.py   # Optional Supabase client (future use)
├── interfaces/
│   └── openapi.json             # Generated API specification
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── README.md                    # This file
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
4. Implement data persistence logic in your API routes

Currently, `get_supabase_client()` returns `None` if credentials are not configured, allowing the app to run without any database backend.

## Security Notes

- Never commit your `.env` file to version control
- Keep your `GEMINI_API_KEY` secure and rotate it regularly
- Use environment-specific `.env` files for development, staging, and production

## Support

For issues or questions, please refer to the main project documentation.
