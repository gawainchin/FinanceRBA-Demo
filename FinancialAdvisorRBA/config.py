#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Load and return configuration settings."""
    # Load environment variables from .env file
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print("Error: .env file not found in the FinancialAdvisorRBA directory.")
        print("Please create a .env file with your OPENAI_API_KEY.")
        return None
    
    load_dotenv(env_path)
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please add your OpenAI API key to the .env file.")
        return None
    
    return {
        "api_key": api_key,
        "llm_config": {
            "config_list": [{
                "model": "gpt-4o-mini",
                "api_key": api_key
            }]
        },
        "pdf_dir": Path(__file__).parent / "sample_pdf"
    } 