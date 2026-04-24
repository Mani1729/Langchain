"""
Azure OpenAI Configuration Utility
This module provides pre-configured Azure OpenAI chat models for use across all notebooks.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Pre-configured Azure OpenAI chat models
def get_chat_model(temperature=0, deployment="gpt-4o"):
    """
    Get an Azure OpenAI chat model instance.
    
    Args:
        temperature (float): The sampling temperature (0-1)
        deployment (str): The Azure deployment name
        
    Returns:
        AzureChatOpenAI: Configured chat model instance
    """
    return AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=temperature
    )

# Default model instances for convenience
gpt4o_chat = get_chat_model(temperature=0, deployment="gpt-4o")
gpt35_chat = get_chat_model(temperature=0, deployment="gpt-4o")  # Update deployment name if you have a separate GPT-3.5 deployment
