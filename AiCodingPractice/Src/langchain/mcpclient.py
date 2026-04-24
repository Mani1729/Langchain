import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage


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
            "local_server": {
                "transport": "stdio", 
                "command": "python",
                "args": ["mcpserver.py"]} 
        
    })

    tools = await client.get_tools()

    resources = await client.get_resources("local_server")

    prompt_response = await client.get_prompt("local_server", "prompt")
    # Extract the actual prompt text from the response
    prompt = prompt_response[0].content if prompt_response else "You are a helpful assistant."
    
    agent = create_agent(
        model=model,   
        tools=tools,
        system_prompt=prompt,
        checkpointer=InMemorySaver()
    )

    config = {"configurable": {"thread_id": "1"}}

    question = "Can you provide me with some information about LangChain?"
    

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content=question)]},
        config=config
    )

    print(response["messages"][-1].content)
    print(response)
    print(response["messages"][1].tool_calls)


if __name__ == "__main__":
    asyncio.run(main())