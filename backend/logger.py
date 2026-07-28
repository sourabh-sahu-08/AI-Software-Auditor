import logging
import os
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a daily log file name
log_file = os.path.join(LOG_DIR, f"auditor_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure standard Python logging
logger = logging.getLogger("AI_Software_Auditor")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Console Handler (optional, for terminal view)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log_api_call(service: str, endpoint: str, status: str):
    logger.info(f"API CALL - Service: {service} | Endpoint: {endpoint} | Status: {status}")

def log_error(context: str, error_msg: str):
    logger.error(f"ERROR - {context} | Details: {error_msg}")

def log_verification(step: str, status: str, execution_time: float):
    logger.info(f"VERIFICATION - Step: {step} | Status: {status} | Time: {execution_time}s")
