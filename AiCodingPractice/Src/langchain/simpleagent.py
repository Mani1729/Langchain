import os
from anthropic import BaseModel
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
)

agent = create_agent(model)

messages = []

messages.append(HumanMessage(content="What's the capital of the Moon?"))
messages.append(AIMessage(content="The capital of the Moon is Luna City."))
messages.append(HumanMessage(content="Interesting, tell me more about Luna City"))

# response = agent.invoke({"messages": messages})

# print(response["messages"][-1].content)

# for token, metadata in  agent.stream({"messages": messages}, stream_mode="messages"):

#     if token.content:
#         print(token.content, end='', flush=True)

class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str

structureagent = create_agent(model, 
                              system_prompt="You are a science fiction writer, create a capital city at the users request.",
                              response_format=CapitalInfo)

response = structureagent.invoke({"messages": [HumanMessage(content="Create a capital city on Mars.")]})

print(response["structured_response"])