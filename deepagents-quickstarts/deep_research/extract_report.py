"""Extract the final report from the agent's state."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the agent
from agent import agent

def extract_files():
    """Extract files from the agent's last run."""
    config = {"configurable": {"thread_id": "1"}}
    
    try:
        # Get the current state
        state = agent.get_state(config)
        
        # Check if files exist in the state
        if hasattr(state, 'values') and 'files' in state.values:
            files = state.values['files']
            
            if '/final_report.md' in files:
                print("📄 Extracting final_report.md...")
                with open("final_report.md", "w", encoding="utf-8") as f:
                    f.write(files['/final_report.md'])
                print("✅ Saved to: final_report.md")
            
            if '/research_request.md' in files:
                print("📄 Extracting research_request.md...")
                with open("research_request.md", "w", encoding="utf-8") as f:
                    f.write(files['/research_request.md'])
                print("✅ Saved to: research_request.md")
            
            if not files:
                print("❌ No files found in agent state.")
        else:
            print("❌ No 'files' key found in agent state.")
            print(f"State keys: {list(state.values.keys()) if hasattr(state, 'values') else 'No values'}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_files()
