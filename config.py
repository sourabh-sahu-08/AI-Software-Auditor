import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Model Configuration
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_FALLBACK_MODEL = "llama-3.1-8b-instant"

# System Limits & Reliability
REQUEST_TIMEOUT = 10  # Seconds
RETRY_COUNT = 1       # Number of times to retry failed AI requests

# UI & Display
THEME = "dark"
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"
