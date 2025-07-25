#!/usr/bin/env python3
"""
ResumePro - AI-Powered Resume Analysis Tool
Hugging Face Spaces Deployment Entry Point
"""

import os
import sys
import logging
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import the main Flask app from backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from app import app as flask_app

# Use the imported app
app = flask_app

# Configure logging for Hugging Face Spaces
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Hugging Face Spaces configuration
if __name__ == "__main__":
    # Get port from environment (Hugging Face Spaces uses port 7860)
    port = int(os.environ.get("PORT", 7860))
    
    logger.info(f"Starting ResumePro on port {port}")
    logger.info(f"Environment: {os.environ.get('SPACE_ID', 'local')}")
    
    # Run the app
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False  # Always False in production
    )
