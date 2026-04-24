import os
import asyncio
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
import json

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
)
    

@dataclass
class ColourContext:
    favourite_colour: str = "blue"
    least_favourite_colour: str = "brown"

agent = create_agent(
    model=model,
    context_schema= ColourContext,
    )

response = agent.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()
)

print("Response:", response["messages"][-1].content)

@tool
def get_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the favourite colour of the user"""
    return runtime.context.favourite_colour

@tool
def get_least_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the least favourite colour of the user"""
    return runtime.context.least_favourite_colour

agent1 = create_agent(
    model=model,
    tools=[get_favourite_colour, get_least_favourite_colour],
    context_schema=ColourContext
)

response1 = agent1.invoke(
    {"messages": [HumanMessage(content="What is my least favourite colour?")]},
    context=ColourContext()
)
print("Response1:", response1["messages"][-1].content)