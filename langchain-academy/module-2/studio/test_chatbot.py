import requests
import json

BASE_URL = "http://127.0.0.1:2024"

# Create a thread
print("Creating conversation thread...")
try:
    response = requests.post(f"{BASE_URL}/threads", timeout=10)
    thread_id = response.json()['thread_id']
    print(f"Thread ID: {thread_id}\n")
except requests.exceptions.Timeout:
    print("Error: Server is not responding. Please wait for server to fully start.")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Send a message
message = input("Enter your message: ")

print("\nSending message...")
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

headers = {
    "Content-Type": "application/json"
}

response = requests.post(
    f"{BASE_URL}/threads/{thread_id}/runs/stream",
    json=payload,
    headers=headers,
    stream=True
)

print("\nAssistant: ", end="", flush=True)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = line[6:]
            try:
                event = json.loads(data)
                if event.get('event') == 'messages/partial':
                    for msg in event.get('data', []):
                        if msg.get('type') == 'ai':
                            print(msg.get('content', ''), end="", flush=True)
            except json.JSONDecodeError:
                pass

print("\n")
