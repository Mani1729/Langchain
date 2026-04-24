import requests
import json
import uuid

# API endpoint
BASE_URL = "http://127.0.0.1:2024"

# Create a thread (conversation session)
def create_thread():
    response = requests.post(f"{BASE_URL}/threads")
    thread = response.json()
    print(f"Created thread: {thread['thread_id']}")
    return thread['thread_id']

# Send a message and get response
def send_message(thread_id, message):
    """Send a message to the chatbot and stream the response."""
    
    payload = {
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Stream the response
    url = f"{BASE_URL}/threads/{thread_id}/runs/stream"
    
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        stream=True
    )
    
    print(f"\nAssistant: ", end="", flush=True)
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]  # Remove 'data: ' prefix
                try:
                    event = json.loads(data)
                    # Print messages as they come
                    if event.get('event') == 'messages/partial':
                        for msg in event.get('data', []):
                            if msg.get('type') == 'ai':
                                print(msg.get('content', ''), end="", flush=True)
                except json.JSONDecodeError:
                    pass
    
    print("\n")

def main():
    print("=" * 50)
    print("LangGraph Chatbot Client")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    # Create a new conversation thread
    thread_id = create_thread()
    
    # Chat loop
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            send_message(thread_id, user_input)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
