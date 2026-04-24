import os
from dotenv import load_dotenv
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver

import requests
    
load_dotenv()

@dataclass
class Context:
    user_id: str    

@dataclass
class ResponseFormat:
    summary: str
    temparature_celsisus: float | None = None
    temparature_fahrenheit: float | None = None
    humidity: float | None = None


model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o-mini",
    temperature=0
)

checkpointer =  InMemorySaver()


@tool('locate_user', description="Look up user city based on user context. Returns city name if found, or indicates location is unknown.")
def locate_user(runtime: ToolRuntime[Context]):
    """Locate user based on user context."""
    user_id = runtime.context.user_id
    # Dummy implementation for example purposes
    user_locations = {
        "user_1": "Vienna",
        "user_2": "London",
        "user_3": "San Francisco",
        "user_4": "Tokyo" 
    }
    city = user_locations.get(user_id)
    if city:
        return city
    else:
        return "USER_LOCATION_NOT_FOUND"

@tool('get_weather', description="Retrieve the weather information of a given city. Do not call this if city is USER_LOCATION_NOT_FOUND." , return_direct=False)
def get_weather(city: str):
    """Get the current weather for a given location."""
    if city == "USER_LOCATION_NOT_FOUND":
        return {"error": "Cannot get weather without a valid city name. Please ask the user for their city."}
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    return response.json()


agent = create_agent(
    model=model,
    tools=[get_weather, locate_user],
    system_prompt="You are a helpful assistant who always crack jokes and humorous while remaining helpfull. When asked about weather, ALWAYS call locate_user tool first to find the user's location, then use that location to call get_weather. If location is not found, ask the user for their city.",
    context_schema= Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {'configurable': {'thread_id': 3}} 



response = agent.invoke({'messages': [
    {"role": "user", "content": "What's the weather like?"}]},
    config= config,
    context= Context(user_id="user_1")
)

# print(response);
print(response['structured_response']);
print(response['structured_response'].summary);
print(response['structured_response'].temparature_celsisus);

response = agent.invoke({'messages': [
    {"role": "user", "content": "and is this usual?"}]},
    config= config,
    context= Context(user_id="user_1")
)

# print(response);
# print(response['structured_response']);
print(response['structured_response'].summary);
# print(response['structured_response'].temparature_celsisus);

conversation = [
    SystemMessage(content="You are a helpful assistant that answers questions about programming languages."),
    HumanMessage(content="What is Python?"),
    AIMessage(content="Python is a high-level, interpreted programming language known for its readability and versatility."),   
    HumanMessage(content="When it is released?")
]  

# response1 = model.invoke(conversation);
# print(response1.content)

# for chunk in model.stream("what is python?"):
#     print(chunk.text, end="", flush=True)
