import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
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
async def main():
    client = MultiServerMCPClient(
    {
        "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com"
            }
    }
)

    tools = await client.get_tools()

    agent = create_agent(
        model=model,   
        tools=tools,
        system_prompt="You are a travel agent. No follow up questions.",
        checkpointer=InMemorySaver()
    )
    
    # for tool in tools:
    #     print(f"Tool: {tool.name}")
    #     print(f"Description: {tool.description}")
    #     if hasattr(tool, 'args_schema'):
    #         print(f"Parameters: {json.dumps(tool.args_schema, indent=2)}")
    #     print("-" * 50)

    config = {"configurable": {"thread_id": "1"}}

    try:
        response = await agent.ainvoke(
            {"messages": [HumanMessage(content="Get me a direct flight from San Francisco to Tokyo on Jan 31st 2026")]},
            config
        )
    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()
    print(response["messages"][1].tool_calls)
    print("----- Final Response -----")
    print(response["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())