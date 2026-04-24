"""
LCEL - LangChain Expression Language
=====================================

THEORY:
-------
LCEL is LangChain's declarative way to compose chains using the pipe (|) operator.
It's the modern, recommended way to build LangChain applications.

Key Concepts:
1. Runnables - Base interface for all LCEL components
2. Pipe Operator (|) - Chain components together
3. RunnablePassthrough - Pass inputs through unchanged
4. RunnableParallel - Execute multiple runnables in parallel
5. RunnableLambda - Wrap custom functions
6. RunnableBranch - Conditional routing

Benefits:
- Streaming support out of the box
- Async support automatically
- Parallel execution when possible
- Built-in retry and fallback mechanisms
- Easy composition and reusability

Core Methods:
- invoke() - Single input
- batch() - Multiple inputs
- stream() - Streaming output
- ainvoke() - Async single input
- abatch() - Async multiple inputs
- astream() - Async streaming
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o-mini",
    temperature=0.7
)

# =============================================================================
# EXAMPLE 1: Basic LCEL Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Basic LCEL Chain (Prompt | LLM | Parser)")
print("=" * 60)

# Traditional way (without LCEL)
prompt_template = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
prompt_value = prompt_template.format(topic="cats")
llm_output = llm.invoke(prompt_value)
final_output = llm_output.content
print(f"Traditional way: {final_output}\n")

# LCEL way (clean and composable)
chain = ChatPromptTemplate.from_template("Tell me a joke about {topic}") | llm | StrOutputParser()
result = chain.invoke({"topic": "dogs"})
print(f"LCEL way: {result}\n")

# =============================================================================
# EXAMPLE 2: Multiple Chaining
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Multi-Step Chain")
print("=" * 60)

# Chain: Generate topic -> Write poem -> Translate
topic_chain = (
    ChatPromptTemplate.from_template("Suggest a random topic for a poem") 
    | llm 
    | StrOutputParser()
)

poem_chain = (
    ChatPromptTemplate.from_template("Write a 4-line poem about: {topic}") 
    | llm 
    | StrOutputParser()
)

translate_chain = (
    ChatPromptTemplate.from_template("Translate to Spanish: {poem}") 
    | llm 
    | StrOutputParser()
)

# Execute sequentially
topic = topic_chain.invoke({})
print(f"Topic: {topic}")

poem = poem_chain.invoke({"topic": topic})
print(f"\nPoem:\n{poem}")

translation = translate_chain.invoke({"poem": poem})
print(f"\nTranslation:\n{translation}\n")

# =============================================================================
# EXAMPLE 3: RunnablePassthrough
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: RunnablePassthrough")
print("=" * 60)

from langchain_core.runnables import RunnablePassthrough

# Pass original input alongside processed output
chain = (
    RunnablePassthrough.assign(
        joke=ChatPromptTemplate.from_template("Tell a joke about {topic}") | llm | StrOutputParser()
    )
)

result = chain.invoke({"topic": "programming"})
print(f"Original input preserved:")
print(f"Topic: {result['topic']}")
print(f"Joke: {result['joke']}\n")

# =============================================================================
# EXAMPLE 4: RunnableParallel
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: RunnableParallel - Execute Multiple Chains")
print("=" * 60)

from langchain_core.runnables import RunnableParallel

# Execute multiple chains in parallel
parallel_chain = RunnableParallel(
    joke=ChatPromptTemplate.from_template("Tell a joke about {topic}") | llm | StrOutputParser(),
    poem=ChatPromptTemplate.from_template("Write a haiku about {topic}") | llm | StrOutputParser(),
    fact=ChatPromptTemplate.from_template("Give an interesting fact about {topic}") | llm | StrOutputParser()
)

result = parallel_chain.invoke({"topic": "space"})
print(f"Joke:\n{result['joke']}\n")
print(f"Poem:\n{result['poem']}\n")
print(f"Fact:\n{result['fact']}\n")

# Alternative syntax using dict
parallel_dict = {
    "pros": ChatPromptTemplate.from_template("List 3 pros of {topic}") | llm | StrOutputParser(),
    "cons": ChatPromptTemplate.from_template("List 3 cons of {topic}") | llm | StrOutputParser()
}

result = RunnableParallel(parallel_dict).invoke({"topic": "remote work"})
print(f"Pros:\n{result['pros']}\n")
print(f"Cons:\n{result['cons']}\n")

# =============================================================================
# EXAMPLE 5: RunnableLambda - Custom Functions
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: RunnableLambda - Custom Functions in Chain")
print("=" * 60)

from langchain_core.runnables import RunnableLambda

# Custom function to process text
def uppercase_text(text):
    return text.upper()

def count_words(text):
    return {"text": text, "word_count": len(text.split())}

# Chain with custom functions
chain = (
    ChatPromptTemplate.from_template("Write a sentence about {topic}")
    | llm
    | StrOutputParser()
    | RunnableLambda(count_words)
)

result = chain.invoke({"topic": "machine learning"})
print(f"Result: {result['text']}")
print(f"Word count: {result['word_count']}\n")

# =============================================================================
# EXAMPLE 6: RunnableBranch - Conditional Routing
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: RunnableBranch - Conditional Logic")
print("=" * 60)

from langchain_core.runnables import RunnableBranch

# Different chains for different languages
french_chain = (
    ChatPromptTemplate.from_template("Respond in French: {query}")
    | llm
    | StrOutputParser()
)

spanish_chain = (
    ChatPromptTemplate.from_template("Respond in Spanish: {query}")
    | llm
    | StrOutputParser()
)

english_chain = (
    ChatPromptTemplate.from_template("Respond in English: {query}")
    | llm
    | StrOutputParser()
)

# Branch based on language
branch = RunnableBranch(
    (lambda x: x["language"] == "french", french_chain),
    (lambda x: x["language"] == "spanish", spanish_chain),
    english_chain  # default
)

result1 = branch.invoke({"language": "french", "query": "Hello, how are you?"})
print(f"French: {result1}\n")

result2 = branch.invoke({"language": "spanish", "query": "Hello, how are you?"})
print(f"Spanish: {result2}\n")

result3 = branch.invoke({"language": "unknown", "query": "Hello, how are you?"})
print(f"Default (English): {result3}\n")

# =============================================================================
# EXAMPLE 7: Streaming
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: Streaming with LCEL")
print("=" * 60)

chain = (
    ChatPromptTemplate.from_template("Write a short story about {topic}")
    | llm
    | StrOutputParser()
)

print("Streaming response: ", end="")
for chunk in chain.stream({"topic": "a robot learning to paint"}):
    print(chunk, end="", flush=True)
print("\n")

# =============================================================================
# EXAMPLE 8: Batch Processing
# =============================================================================
print("=" * 60)
print("EXAMPLE 8: Batch Processing")
print("=" * 60)

chain = (
    ChatPromptTemplate.from_template("What is the capital of {country}?")
    | llm
    | StrOutputParser()
)

countries = [
    {"country": "France"},
    {"country": "Japan"},
    {"country": "Brazil"}
]

results = chain.batch(countries)
for country, result in zip(countries, results):
    print(f"{country['country']}: {result}")
print()

# =============================================================================
# EXAMPLE 9: Fallbacks and Retry
# =============================================================================
print("=" * 60)
print("EXAMPLE 9: Fallbacks for Reliability")
print("=" * 60)

# Primary chain with higher temperature
primary_llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o-mini",
    temperature=0.9
)
primary_chain = (
    ChatPromptTemplate.from_template("Explain {concept} in simple terms")
    | primary_llm
    | StrOutputParser()
)

# Fallback chain (more conservative temperature)
fallback_llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.3
)
fallback_chain = (
    ChatPromptTemplate.from_template("Explain {concept} in simple terms")
    | fallback_llm
    | StrOutputParser()
)

# Chain with fallback
chain_with_fallback = primary_chain.with_fallbacks([fallback_chain])

try:
    result = chain_with_fallback.invoke({"concept": "quantum entanglement"})
    print(f"Result: {result}\n")
except Exception as e:
    print(f"Error: {e}\n")

# =============================================================================
# EXAMPLE 10: Complex RAG-like Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 10: Complex Chain with Context")
print("=" * 60)

# Simulated retrieval function
def retrieve_context(query):
    # In real RAG, this would search a vector database
    contexts = {
        "python": "Python is a high-level programming language known for its simplicity.",
        "javascript": "JavaScript is a programming language primarily used for web development.",
        "rust": "Rust is a systems programming language focused on safety and performance."
    }
    return contexts.get(query["topic"], "No context found")

# RAG chain: Retrieve -> Format -> Generate
rag_chain = (
    RunnablePassthrough.assign(context=RunnableLambda(retrieve_context))
    | ChatPromptTemplate.from_template(
        """Answer the question based on the context below.
        
Context: {context}

Question: {question}

Answer:"""
    )
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke({
    "topic": "python",
    "question": "What makes this language special?"
})
print(f"RAG Result: {result}\n")

# =============================================================================
# EXAMPLE 11: Configurable Chains
# =============================================================================
print("=" * 60)
print("EXAMPLE 11: Configurable Chains")
print("=" * 60)

from langchain_core.runnables import ConfigurableField

# Create configurable LLM
configurable_llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.7
).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM"
    )
)

chain = (
    ChatPromptTemplate.from_template("Tell me about {topic}")
    | configurable_llm
    | StrOutputParser()
)

# Use with different temperatures
result1 = chain.invoke(
    {"topic": "creativity"},
    config={"configurable": {"llm_temperature": 0.2}}  # More focused
)
print(f"Temperature 0.2 (focused):\n{result1}\n")

result2 = chain.invoke(
    {"topic": "creativity"},
    config={"configurable": {"llm_temperature": 1.0}}  # More creative
)
print(f"Temperature 1.0 (creative):\n{result2}\n")

# =============================================================================
# EXAMPLE 12: Async LCEL
# =============================================================================
print("=" * 60)
print("EXAMPLE 12: Async LCEL")
print("=" * 60)

import asyncio

async def async_example():
    chain = (
        ChatPromptTemplate.from_template("What is {topic}?")
        | llm
        | StrOutputParser()
    )
    
    # Async invoke
    result = await chain.ainvoke({"topic": "asyncio"})
    print(f"Async result: {result}\n")
    
    # Async streaming
    print("Async streaming: ", end="")
    async for chunk in chain.astream({"topic": "coroutines"}):
        print(chunk, end="", flush=True)
    print("\n")

# Run async example
asyncio.run(async_example())

"""
KEY TAKEAWAYS:
--------------
1. LCEL uses the pipe (|) operator for clean composition
2. All LCEL chains support: invoke, batch, stream, and async variants
3. RunnablePassthrough: Pass data through while adding transformations
4. RunnableParallel: Execute multiple operations in parallel (use dict or explicit)
5. RunnableLambda: Wrap custom Python functions
6. RunnableBranch: Conditional routing based on input
7. Streaming: Built-in support with .stream()
8. Batch: Process multiple inputs efficiently with .batch()
9. Fallbacks: Add reliability with .with_fallbacks()
10. Configurable: Make chains flexible with ConfigurableField
11. Async: Full async support with ainvoke, astream, abatch

LCEL PATTERNS:
--------------
1. Simple Chain: prompt | llm | parser
2. Multi-Step: chain1 | chain2 | chain3
3. Parallel: RunnableParallel({key1: chain1, key2: chain2})
4. Conditional: RunnableBranch((condition, chain), default_chain)
5. RAG: retrieve | format | generate
6. Map-Reduce: batch | parallel_process | aggregate
7. With Context: RunnablePassthrough.assign(extra=transform)

WHEN TO USE LCEL:
-----------------
✅ Building new chains (recommended approach)
✅ Need streaming support
✅ Async operations required
✅ Want parallel execution
✅ Need composable, reusable components
✅ Want built-in retry/fallback

NEXT STEPS:
-----------
- 04_tools.py - Learn to integrate external tools
- 05_memory.py - Add conversation memory
"""

print("=" * 60)
print("LCEL concepts complete!")
print("=" * 60)
