"""
LangChain Basics and Setup Guide
=================================

THEORY:
-------
LangChain is a framework for developing applications powered by language models.
It provides:
1. Components - Modular abstractions for working with LLMs
2. Chains - Combining components to accomplish specific tasks
3. Agents - Systems that use LLMs to make decisions about actions
4. Memory - Persisting state between chain/agent calls

Key Concepts:
- LLM Wrappers: Unified interface for different LLM providers
- Prompt Templates: Dynamic prompt creation
- Output Parsers: Structure LLM outputs
- Callbacks: Monitor and log LLM operations
"""

# Installation:
# pip install langchain langchain-openai langchain-community python-dotenv

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example 1: Basic LLM Call with Azure OpenAI
print("=" * 60)
print("EXAMPLE 1: Basic LLM Call with Azure OpenAI")
print("=" * 60)

from langchain_openai import AzureChatOpenAI

# Initialize the LLM with Azure OpenAI
llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.7,  # Controls randomness (0=deterministic, 1=creative)
)

# Simple invocation
response = llm.invoke("What is LangChain in one sentence?")
print(f"Response: {response.content}\n")

# Example 2: Using Different Message Types
print("=" * 60)
print("EXAMPLE 2: Message Types")
print("=" * 60)

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

messages = [
    SystemMessage(content="You are a helpful AI assistant that explains concepts clearly."),
    HumanMessage(content="Explain what a vector database is in simple terms.")
]

response = llm.invoke(messages)
print(f"Response: {response.content}\n")

# Example 3: Streaming Responses
print("=" * 60)
print("EXAMPLE 3: Streaming Responses")
print("=" * 60)

print("Streaming response: ", end="")
for chunk in llm.stream("Write a haiku about programming."):
    print(chunk.content, end="", flush=True)
print("\n")

# Example 4: Batch Processing
print("=" * 60)
print("EXAMPLE 4: Batch Processing")
print("=" * 60)

questions = [
    "What is Python?",
    "What is JavaScript?",
    "What is TypeScript?"
]

responses = llm.batch(questions)
for q, r in zip(questions, responses):
    print(f"Q: {q}")
    print(f"A: {r.content}\n")

# Example 5: Using Output Parsers
print("=" * 60)
print("EXAMPLE 5: Output Parsers")
print("=" * 60)

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

# String parser (most common)
parser = StrOutputParser()
chain = llm | parser  # Using LCEL pipe operator
result = chain.invoke("Say hello in 3 different languages")
print(f"String output: {result}\n")

# JSON parser with schema
class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")
    occupation: str = Field(description="Person's occupation")

json_parser = JsonOutputParser(pydantic_object=Person)
prompt_with_format = f"""
Generate information about a fictional software engineer.
{json_parser.get_format_instructions()}
"""

json_result = llm.invoke(prompt_with_format)
parsed = json_parser.parse(json_result.content)
print(f"Parsed JSON: {parsed}\n")

# Example 6: Using Alternative LLM Providers
print("=" * 60)
print("EXAMPLE 6: Alternative LLM Providers")
print("=" * 60)

# Anthropic Claude
try:
    from langchain_anthropic import ChatAnthropic
    
    claude = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    response = claude.invoke("What makes Claude different?")
    print(f"Claude: {response.content}\n")
except Exception as e:
    print(f"Claude not configured: {e}\n")

# Local models with Ollama
try:
    from langchain_community.llms import Ollama
    
    local_llm = Ollama(model="llama2")
    response = local_llm.invoke("Why use local LLMs?")
    print(f"Local LLM: {response}\n")
except Exception as e:
    print(f"Ollama not configured: {e}\n")

# Example 7: Callbacks and Monitoring
print("=" * 60)
print("EXAMPLE 7: Callbacks for Monitoring")
print("=" * 60)

from langchain_core.callbacks import StdOutCallbackHandler

callback = StdOutCallbackHandler()
llm_with_callback = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o",
    model="gpt-4o",
    callbacks=[callback]
)

response = llm_with_callback.invoke("Count from 1 to 5")
print(f"\nResponse: {response.content}\n")

# Example 8: Token Usage and Cost Tracking
print("=" * 60)
print("EXAMPLE 8: Token Usage Tracking")
print("=" * 60)

from langchain_community.callbacks import get_openai_callback

with get_openai_callback() as cb:
    response = llm.invoke("Explain quantum computing in 50 words.")
    print(f"Response: {response.content}\n")
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost:.6f}\n")

# Example 9: Caching to Save Costs
print("=" * 60)
print("EXAMPLE 9: Caching LLM Calls")
print("=" * 60)

from langchain_community.cache import InMemoryCache
from langchain_core.globals import set_llm_cache

# Enable caching
set_llm_cache(InMemoryCache())

import time

# First call (no cache)
start = time.time()
response1 = llm.invoke("What is 2+2?")
time1 = time.time() - start
print(f"First call (no cache): {time1:.2f}s")
print(f"Response: {response1.content}\n")

# Second call (cached)
start = time.time()
response2 = llm.invoke("What is 2+2?")
time2 = time.time() - start
print(f"Second call (cached): {time2:.2f}s")
print(f"Response: {response2.content}\n")

"""
KEY TAKEAWAYS:
--------------
1. LangChain provides unified interfaces for different LLM providers
2. Three main invocation methods: invoke (single), batch (multiple), stream (real-time)
3. Use SystemMessage for instructions, HumanMessage for user input
4. Output parsers structure LLM responses (String, JSON, etc.)
5. Callbacks enable monitoring, logging, and cost tracking
6. Caching reduces costs and latency for repeated queries
7. Temperature controls creativity (0=focused, 1=creative)

NEXT STEPS:
-----------
Now that you understand the basics, move on to:
- 02_prompting_concepts.py - Learn to craft effective prompts
- 03_lcel.py - Master LangChain Expression Language
"""

print("=" * 60)
print("Setup complete! Review the examples above.")
print("=" * 60)
