import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage
from pprint import pprint
from typing import Any
from langchain.agents import AgentState
from langchain.messages import RemoveMessage
from langgraph.runtime import Runtime
from langchain.agents.middleware import before_agent
from langchain.messages import ToolMessage
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command


load_dotenv()


model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the given address."""
    # take email from state
    return runtime.state["email"]

@tool
def send_email(body: str) -> str:
    """Send an email to the given address with the given subject and body."""
    # fake email sending
    return f"Email sent"




class EmailState(AgentState):
    email: str

agent = create_agent(
    model=model,
    tools=[read_email, send_email],
    state_schema=EmailState,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,
                "send_email": True,
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
)

config = {"configurable": {"thread_id": "2"}}

response = agent.invoke(
    {
        "messages": [HumanMessage(content="Please read my email and send a response.")],
        "email": "Hi Seán, I'm going to be late for our meeting tomorrow. Can we reschedule? Best, John."
    },
    config=config
)


print(response['__interrupt__'][0].value['action_requests'][0]['args']['body'])

response = agent.invoke(
    Command( 
        resume={"decisions": [{"type": "approve"}]}
    ), 
    config=config # Same thread ID to resume the paused conversation
)

pprint(response)