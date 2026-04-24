"""
Helper module for Azure OpenAI configuration with LangChain
"""
import os
from langchain_openai import AzureChatOpenAI

def get_azure_chat_model(
    deployment_name=None,
    api_version=None,
    temperature=0,
    **kwargs
):
    """
    Create an AzureChatOpenAI instance using environment variables.
    
    Args:
        deployment_name: Azure OpenAI deployment name (defaults to env var)
        api_version: API version (defaults to env var)
        temperature: Model temperature (default: 0)
        **kwargs: Additional arguments to pass to AzureChatOpenAI
    
    Returns:
        AzureChatOpenAI: Configured Azure OpenAI chat model
    """
    deployment = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    version = api_version or os.getenv("AZURE_OPENAI_API_VERSION")
    
    return AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=version,
        temperature=temperature,
        **kwargs
    )

def get_model_string():
    """
    Get the model string for use with create_agent.
    For Azure OpenAI, we need to use the full configuration.
    
    Returns:
        AzureChatOpenAI: Configured model instance
    """
    return get_azure_chat_model()
