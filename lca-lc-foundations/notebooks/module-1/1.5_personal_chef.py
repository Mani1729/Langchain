import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import azure_openai_config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

load_dotenv()

from azure_openai_config import setup_azure_openai, get_azure_openai_model
setup_azure_openai()

from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)

system_prompt = """

You are a personal chef. The user will give you a list of ingredients they have left over in their house.

Using the web search tool, search the web for recipes that can be made with the ingredients they have.

Return recipe suggestions and eventually the recipe instructions to the user, if requested.

"""

from langchain.agents import create_agent

agent = create_agent(
    model=get_azure_openai_model(),
    tools=[web_search],
    system_prompt=system_prompt
)