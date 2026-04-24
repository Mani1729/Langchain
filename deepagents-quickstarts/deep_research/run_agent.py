"""Run the deep research agent with a sample query."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the agent
from agent import agent

def main():
    """Run the research agent with a sample query."""
    
    # Verify environment variables are loaded
    print("🔑 Environment Configuration:")
    print(f"  - Azure OpenAI Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    print(f"  - Azure OpenAI Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT')}")
    print(f"  - Tavily API Key: {'✓' if os.getenv('TAVILY_API_KEY') else '✗'}")
    print()
    
    # Sample research query
    query = input("🔍 Enter your research query (or press Enter for default): ")
    if not query:
        query = "What are the latest developments in AI agents and LangGraph?"
    
    print(f"\n🚀 Starting research on: {query}\n")
    print("=" * 80)
    
    # Run the agent
    try:
        config = {"configurable": {"thread_id": "1"}}
        
        final_state = None
        # Stream the agent's response
        for event in agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            config=config,
            stream_mode="values"
        ):
            if "messages" in event:
                last_message = event["messages"][-1]
                if hasattr(last_message, "content") and last_message.content:
                    print(f"\n{last_message.content}")
            final_state = event
        
        # Extract and save files from the agent's virtual file system
        if final_state and "files" in final_state:
            files = final_state["files"]
            if "/final_report.md" in files:
                report_content = files["/final_report.md"]
                with open("final_report.md", "w", encoding="utf-8") as f:
                    f.write(report_content)
                print("\n📄 Final report saved to: final_report.md")
            if "/research_request.md" in files:
                request_content = files["/research_request.md"]
                with open("research_request.md", "w", encoding="utf-8") as f:
                    f.write(request_content)
                print("📄 Research request saved to: research_request.md")
        
        print("\n" + "=" * 80)
        print("✅ Research completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
