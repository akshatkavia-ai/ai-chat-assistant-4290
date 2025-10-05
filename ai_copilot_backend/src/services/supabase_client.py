"""
Supabase Client Service

This module provides an optional Supabase client for future features like chat logging.
If SUPABASE_URL and SUPABASE_ANON_KEY are not configured in the environment,
the client returns None and the application continues without Supabase integration.
"""

import os
from typing import Optional


def get_supabase_client() -> Optional[object]:
    """
    Get a Supabase client instance.
    
    This function reads SUPABASE_URL and SUPABASE_ANON_KEY from the environment
    and returns a Supabase client if both are present. If either is missing,
    it returns None.
    
    This is an optional integration. The application will work without Supabase.
    In the future, this can be used to:
    - Log chat conversations to a database
    - Store user preferences
    - Implement chat history features
    
    Returns:
        Optional[object]: Supabase client instance if configured, None otherwise.
        
    Example:
        >>> client = get_supabase_client()
        >>> if client:
        ...     # Use Supabase for logging or data persistence
        ...     pass
        ... else:
        ...     # Continue without persistence
        ...     pass
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        # Supabase is optional - return None if not configured
        return None
    
    # Future implementation: Initialize and return Supabase client
    # For now, we just check if the credentials are present
    # When ready to implement:
    # from supabase import create_client
    # return create_client(supabase_url, supabase_key)
    
    return None
