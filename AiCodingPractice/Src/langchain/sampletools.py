from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage


load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
)

@tool
def square_root(x: float) -> float:
    """Returns the square root of a number."""
    return x ** 0.5

@tool("Square_root_tool", description="Calculates the square root of a given number.")
def tool1(x : float) -> float:
    """Returns the square of a number."""
    return x ** 0.5

res = tool1.invoke({"x": 16})
print(f"Square root of 16 is: {res}")

agent = create_agent(
    model=model,
    tools=[tool1],
    system_prompt="You are an arithmetic wizard. Use your tools to calculate the square root and square of any number."
)

question = HumanMessage(content="What is the square root of 467?")

# response = agent.invoke(
#     {"messages": [question]}
# )

# print(response["messages"])
# print(response["messages"][-1].content)
# print(response["messages"][1].tool_calls)