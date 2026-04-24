import os
from anthropic import BaseModel
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver



load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
)

agent = create_agent(model, checkpointer=InMemorySaver())

config = {"configurable":{"thread_id": "2"}}

question = HumanMessage(content="Hello my name is Seán and my favourite colour is green")

response = agent.invoke({"messages": [question]}, config=config)

print(response["messages"][-1].content)

question = HumanMessage(content="What's my favourite colour?")

response = agent.invoke(
    {"messages": [question]},
    config,  
)

print(response["messages"][-1].content)