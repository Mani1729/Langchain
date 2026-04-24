import os
from dotenv import load_dotenv
from typing import Annotated
from langchain_openai import AzureChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent, InjectedState
from langchain_core.messages import HumanMessage

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Define tools with InjectedState to access agent state
@tool
def get_favourite_colour(state: Annotated[dict, InjectedState]) -> str:
    """Get the favourite colour of the user"""
    return state.get("favourite_colour", "Unknown")

@tool
def get_least_favourite_colour(state: Annotated[dict, InjectedState]) -> str:
    """Get the least favourite colour of the user"""
    return state.get("least_favourite_colour", "Unknown")

# Create agent using create_react_agent (supports InjectedState)
agent = create_react_agent(
    model=model,
    tools=[get_favourite_colour, get_least_favourite_colour]
)

# Invoke agent with custom state including colour preferences
response = agent.invoke({
    "messages": [HumanMessage(content="What is my least favourite colour? Use the get_least_favourite_colour tool.")],
    "favourite_colour": "blue",
    "least_favourite_colour": "brown"
})

print("Response:", response["messages"][-1].content)
