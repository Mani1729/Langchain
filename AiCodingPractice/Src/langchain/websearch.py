import os
from typing import Dict, Any
from anthropic import BaseModel
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
)

tavilyclient = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool(description="Performs a web search using Tavily.")
def web_search(query: str) -> Dict[str, Any]:

    return tavilyclient.search(query, max_results=3)

web_search.invoke({"query": "LangChain framework"})

agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt="You are a helpful assistant that can perform web searches to find information."      
)

question = HumanMessage(content="What are the latest advancements in AI?")

response = agent.invoke(
    {"messages": [question]})

print(response["messages"][-1].content)