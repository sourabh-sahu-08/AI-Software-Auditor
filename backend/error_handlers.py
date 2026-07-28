import streamlit as st
from backend.logger import log_error

def handle_error(context: str, error: Exception):
    """
    Reusable error handler that logs the error and displays a friendly message
    in the Streamlit UI.
    """
    error_str = str(error).lower()
    
    # Log the error
    log_error(context, str(error))
    
    # Render appropriate Streamlit error
    if "api key" in error_str or "token" in error_str:
        st.error(f"**Authentication Error:** Missing or invalid API Key. Please check your `.env` file.\n\n*Context: {context}*")
    elif "404" in error_str or "not found" in error_str:
        st.error(f"**Resource Not Found:** The requested repository or resource could not be found. Ensure it is public or you have access.\n\n*Context: {context}*")
    elif "timeout" in error_str:
        st.error(f"**Network Timeout:** The request took too long. Please check your connection and try again.\n\n*Context: {context}*")
    elif "groq" in error_str and ("connection" in error_str or "unavailable" in error_str):
        st.error(f"**API Unavailable:** The Groq API is currently unreachable. Please try again later.\n\n*Context: {context}*")
    else:
        st.error(f"**Unexpected Error:** {str(error)}\n\n*Context: {context}*")
