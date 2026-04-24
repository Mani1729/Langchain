"""
Azure OpenAI Configuration Helper
This module provides utility functions to configure Azure OpenAI for LangChain agents.
"""
import os
from langchain_openai import AzureChatOpenAI


def get_azure_openai_model(**kwargs):
    """
    Create an Azure OpenAI model instance configured from environment variables.
    
    Args:
        **kwargs: Additional keyword arguments to pass to AzureChatOpenAI
        
    Returns:
        AzureChatOpenAI: Configured Azure OpenAI model instance
    """
    default_config = {
        "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
        "temperature": kwargs.pop("temperature", 0),
        "max_tokens": kwargs.pop("max_tokens", None),
        "timeout": kwargs.pop("timeout", None),
        "max_retries": kwargs.pop("max_retries", 2),
    }
    
    # Merge with any additional kwargs
    default_config.update(kwargs)
    
    return AzureChatOpenAI(**default_config)


def setup_azure_openai():
    """
    Configure environment variables for Azure OpenAI.
    Call this after load_dotenv().
    """
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
