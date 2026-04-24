"""
Memory in LangChain
===================

THEORY:
-------
Memory allows LLMs to remember previous interactions in a conversation.
Without memory, each LLM call is stateless and independent.

Key Concepts:
1. Chat History - Store and retrieve conversation messages
2. Memory Types - Different strategies for storing conversation context
3. Memory Windows - Limit how much history to keep
4. Memory Summarization - Compress old conversations
5. Entity Memory - Remember specific entities across conversation

Common Memory Types:
1. ConversationBufferMemory - Store all messages
2. ConversationBufferWindowMemory - Keep last N messages
3. ConversationSummaryMemory - Summarize conversation history
4. ConversationSummaryBufferMemory - Hybrid approach
5. ConversationEntityMemory - Track specific entities
6. ConversationKGMemory - Knowledge graph of conversation
7. VectorStoreMemory - Semantic search over past conversations

Memory Components:
- Memory Variable: Key to access history in prompts
- Input/Output Keys: What to store from chain I/O
- Return Messages: Format of memory (string or message objects)
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.7
)

# =============================================================================
# EXAMPLE 1: Manual Message History (No Memory Object)
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Manual Message History")
print("=" * 60)

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Manual conversation tracking
messages = [
    SystemMessage(content="You are a helpful assistant."),
]

# First turn
messages.append(HumanMessage(content="My name is Alice."))
response = llm.invoke(messages)
messages.append(AIMessage(content=response.content))
print(f"AI: {response.content}\n")

# Second turn - LLM remembers name
messages.append(HumanMessage(content="What's my name?"))
response = llm.invoke(messages)
messages.append(AIMessage(content=response.content))
print(f"AI: {response.content}\n")

# =============================================================================
# EXAMPLE 2: In-Memory Chat History with LCEL
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: In-Memory Chat History with LCEL")
print("=" * 60)

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Create chat history storage
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Create prompt template with history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create chain
chain = prompt | llm | StrOutputParser()

# Wrap with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Have a conversation
print("\n--- Turn 1 ---")
response1 = chain_with_history.invoke(
    {"input": "Hi, I'm learning LangChain."},
    config={"configurable": {"session_id": "session1"}}
)
print(f"AI: {response1}\n")

print("--- Turn 2 ---")
response2 = chain_with_history.invoke(
    {"input": "Can you tell me what I'm learning?"},
    config={"configurable": {"session_id": "session1"}}
)
print(f"AI: {response2}\n")

print("--- Turn 3 ---")
response3 = chain_with_history.invoke(
    {"input": "Why is it useful?"},
    config={"configurable": {"session_id": "session1"}}
)
print(f"AI: {response3}\n")

# View stored history
print("--- Message History ---")
history = store["session1"]
for msg in history.messages:
    print(f"{msg.type}: {msg.content[:100]}...")
print()

# =============================================================================
# EXAMPLE 3: Limiting History Window (Last N Messages)
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: Limiting History Window")
print("=" * 60)

from langchain_core.runnables import RunnableLambda

# Create a new session with window limit
def get_limited_history(session_id: str, limit: int = 4):
    """Get history but only return last N messages"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    history = store[session_id]
    # Return only last N messages
    return InMemoryChatMessageHistory(messages=history.messages[-limit:])

# Create chain with limited history
chain_with_window = RunnableWithMessageHistory(
    prompt | llm | StrOutputParser(),
    lambda session_id: get_limited_history(session_id, limit=4),  # Only last 2 turns (4 messages)
    input_messages_key="input",
    history_messages_key="history"
)

# Have multiple conversations
print("Turn 1:")
r1 = chain_with_window.invoke(
    {"input": "My favorite color is blue."},
    config={"configurable": {"session_id": "session2"}}
)
print(f"AI: {r1}\n")

print("Turn 2:")
r2 = chain_with_window.invoke(
    {"input": "My favorite food is pizza."},
    config={"configurable": {"session_id": "session2"}}
)
print(f"AI: {r2}\n")

print("Turn 3:")
r3 = chain_with_window.invoke(
    {"input": "My favorite animal is a dog."},
    config={"configurable": {"session_id": "session2"}}
)
print(f"AI: {r3}\n")

# Ask about first thing (should be forgotten due to window)
print("Turn 4 (asking about turn 1):")
response = chain_with_window.invoke(
    {"input": "What's my favorite color?"},
    config={"configurable": {"session_id": "session2"}}
)
print(f"AI: {response}")
print("(May not remember blue if it fell outside the window)\n")

# =============================================================================
# EXAMPLE 4: Summarizing Conversation History
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Summarizing Conversation History")
print("=" * 60)

# Create a summary prompt
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following conversation in 2-3 sentences:"),
    ("human", "{conversation}")
])

# Simulate a longer conversation
conversation_text = """
Human: I'm a software engineer working on AI projects.
AI: That's great! AI projects are fascinating.
Human: I specialize in Python and machine learning.
AI: Python is excellent for machine learning.
Human: I've been doing this for 5 years.
AI: You must have significant experience then!
"""

# Get summary
summary_chain = summary_prompt | llm | StrOutputParser()
summary = summary_chain.invoke({"conversation": conversation_text})

print(f"Original conversation length: {len(conversation_text)} chars")
print(f"\nSummary:\n{summary}")
print(f"\nSummary length: {len(summary)} chars")
print("(This is useful for long conversations to reduce token usage)\n")

# =============================================================================
# EXAMPLE 5: Multiple Conversation Sessions
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Multiple Conversation Sessions")
print("=" * 60)

# Have conversations with different users
print("--- User Alice's Session ---")
r1 = chain_with_history.invoke(
    {"input": "My name is Alice and I like cats."},
    config={"configurable": {"session_id": "alice"}}
)
print(f"AI: {r1}\n")

print("--- User Bob's Session ---")
r2 = chain_with_history.invoke(
    {"input": "My name is Bob and I like dogs."},
    config={"configurable": {"session_id": "bob"}}
)
print(f"AI: {r2}\n")

# Continue Alice's conversation
print("--- Back to Alice ---")
r3 = chain_with_history.invoke(
    {"input": "What pet do I like?"},
    config={"configurable": {"session_id": "alice"}}
)
print(f"AI: {r3}\n")

# Continue Bob's conversation
print("--- Back to Bob ---")
r4 = chain_with_history.invoke(
    {"input": "What pet do I like?"},
    config={"configurable": {"session_id": "bob"}}
)
print(f"AI: {r4}\n")

print("(Each session maintains its own independent history)\n")

# =============================================================================
# EXAMPLE 6: Persistent File-Based History
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: Persistent File-Based History")
print("=" * 60)

from langchain_community.chat_message_histories import FileChatMessageHistory

# Create file-based history
file_history = FileChatMessageHistory("chat_history.json")

# Create chain with file-based history
chain_with_file_history = RunnableWithMessageHistory(
    prompt | llm | StrOutputParser(),
    lambda session_id: FileChatMessageHistory(f"chat_{session_id}.json"),
    input_messages_key="input",
    history_messages_key="history"
)

print("Conversation saved to file:")
r1 = chain_with_file_history.invoke(
    {"input": "Remember: my password hint is 'blue ocean'."},
    config={"configurable": {"session_id": "persistent"}}
)
print(f"AI: {r1}\n")

r2 = chain_with_file_history.invoke(
    {"input": "What was my password hint?"},
    config={"configurable": {"session_id": "persistent"}}
)
print(f"AI: {r2}")
print("(This conversation is saved to chat_persistent.json)\n")

# =============================================================================
# EXAMPLE 7: Custom Memory Implementation
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: Custom Memory with Filtering")
print("=" * 60)

from langchain_core.messages import HumanMessage, AIMessage

class FilteredMemory:
    """Custom memory that filters sensitive information"""
    
    def __init__(self):
        self.messages = []
        self.sensitive_words = ['password', 'ssn', 'credit card']
    
    def add_message(self, message):
        # Filter sensitive content
        if isinstance(message, (HumanMessage, AIMessage)):
            content = message.content.lower()
            if any(word in content for word in self.sensitive_words):
                print(f"⚠️ Filtered sensitive content from message")
                return
            self.messages.append(message)

# Test custom memory
filtered_mem = FilteredMemory()

filtered_mem.add_message(HumanMessage(content="My password is abc123"))
filtered_mem.add_message(HumanMessage(content="I like Python programming"))
filtered_mem.add_message(AIMessage(content="Python is great!"))

print("Filtered memory messages:")
for msg in filtered_mem.messages:
    print(f"{msg.__class__.__name__}: {msg.content}")
print("(Sensitive messages were filtered out)\n")

"""
KEY TAKEAWAYS:
--------------
1. Memory enables stateful conversations with LLMs
2. InMemoryChatMessageHistory: Simple in-memory storage
3. RunnableWithMessageHistory: Modern LCEL approach to memory
4. Session IDs: Enable multiple independent conversations
5. Message window: Limit history to last N messages for token efficiency
6. Summarization: Compress old conversations to save tokens
7. File-based history: Persist conversations across sessions
8. Custom memory: Implement filtering, metadata, or special logic
9. Choose memory strategy based on:
   - Conversation length
   - Token budget
   - Persistence needs
   - Context requirements

MEMORY SELECTION GUIDE:
-----------------------

Short conversations (< 10 turns):
✅ Full history (InMemoryChatMessageHistory)

Long conversations (> 10 turns):
✅ Window-based history (limit to last 4-6 messages)
✅ Summarization for very long conversations

Production applications:
✅ File or database-backed history
✅ Session management with IDs
✅ Consider token costs

Multiple users:
✅ Separate session IDs per user
✅ Persistent storage (files/database)

NEXT STEPS:
-----------
- 06_chain_building.py - Build complex chains
- 07_agents.py - Create ReAct agents
"""

print("=" * 60)
print("Memory concepts complete!")
print("=" * 60)

# Cleanup
import os
for file in ["chat_history.json", "chat_persistent.json", "conversation_history.json"]:
    if os.path.exists(file):
        os.remove(file)
