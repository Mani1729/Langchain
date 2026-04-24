"""
Tools in LangChain
==================

THEORY:
-------
Tools are interfaces that allow LLMs to interact with external systems and APIs.
They extend the capabilities of LLMs beyond text generation.

Key Concepts:
1. Tool - A function/API the LLM can call
2. Tool Definition - Describes what the tool does (name, description, parameters)
3. Tool Calling - LLM decides when and how to use tools
4. Built-in Tools - Pre-made tools (search, calculator, etc.)
5. Custom Tools - Your own functions wrapped as tools

Tool Components:
- name: Identifier for the tool
- description: What the tool does (critical for LLM to understand)
- parameters: Input schema (using Pydantic)
- func: The actual function to execute

Types of Tools:
1. Built-in Tools - DuckDuckGo search, Wikipedia, ArXiv, etc.
2. Custom Tools - @tool decorator or Tool class
3. StructuredTool - For complex parameter schemas
4. API Tools - Call REST APIs
5. Database Tools - Query databases
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0
)

# =============================================================================
# EXAMPLE 1: Simple Custom Tool with @tool Decorator
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Creating Simple Custom Tools")
print("=" * 60)

from langchain.tools import tool

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@tool
def concatenate_strings(str1: str, str2: str) -> str:
    """Concatenate two strings with a space between them."""
    return f"{str1} {str2}"

# Test tools directly
print(f"Tool name: {get_word_length.name}")
print(f"Tool description: {get_word_length.description}")
print(f"Tool result: {get_word_length.invoke('LangChain')}\n")

print(f"Multiply tool result: {multiply_numbers.invoke({'a': 5, 'b': 7})}\n")

# =============================================================================
# EXAMPLE 2: Custom Tool with Tool Class
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Custom Tool with Tool Class")
print("=" * 60)

from langchain_core.tools import Tool

def search_database(query: str) -> str:
    """Simulated database search"""
    database = {
        "python": "Python is a high-level programming language.",
        "javascript": "JavaScript is used for web development.",
        "rust": "Rust is a systems programming language."
    }
    return database.get(query.lower(), "Not found in database")

database_tool = Tool(
    name="DatabaseSearch",
    func=search_database,
    description="Search the internal database for information about programming languages. Input should be a language name."
)

result = database_tool.invoke("Python")
print(f"Database search result: {result}\n")

# =============================================================================
# EXAMPLE 3: StructuredTool for Complex Inputs
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: StructuredTool with Complex Parameters")
print("=" * 60)

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    operation: str = Field(description="The operation: add, subtract, multiply, divide")
    num1: float = Field(description="First number")
    num2: float = Field(description="Second number")

def calculator(operation: str, num1: float, num2: float) -> float:
    """Perform basic arithmetic operations"""
    operations = {
        "add": num1 + num2,
        "subtract": num1 - num2,
        "multiply": num1 * num2,
        "divide": num1 / num2 if num2 != 0 else "Error: Division by zero"
    }
    return operations.get(operation, "Invalid operation")

calculator_tool = StructuredTool.from_function(
    func=calculator,
    name="Calculator",
    description="Perform arithmetic operations. Operations: add, subtract, multiply, divide",
    args_schema=CalculatorInput
)

result = calculator_tool.invoke({
    "operation": "multiply",
    "num1": 15,
    "num2": 3
})
print(f"Calculator result: {result}\n")

# =============================================================================
# EXAMPLE 4: Built-in Tools - Web Search
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Built-in Tools - DuckDuckGo Search")
print("=" * 60)

try:
    from langchain_community.tools import DuckDuckGoSearchRun
    
    search = DuckDuckGoSearchRun()
    result = search.invoke("LangChain framework")
    print(f"Search result: {result[:200]}...\n")
except ImportError:
    print("Install duckduckgo-search: pip install duckduckgo-search\n")

# =============================================================================
# EXAMPLE 5: Built-in Tools - Wikipedia
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Built-in Tools - Wikipedia")
print("=" * 60)

try:
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    result = wikipedia.invoke("Artificial Intelligence")
    print(f"Wikipedia result: {result[:300]}...\n")
except ImportError:
    print("Install wikipedia: pip install wikipedia\n")

# =============================================================================
# EXAMPLE 6: Tool with LLM (Manual Tool Calling)
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: Using Tools with LLM Manually")
print("=" * 60)

from langchain_core.prompts import ChatPromptTemplate

# Create tools list
tools = [get_word_length, multiply_numbers, concatenate_strings]

# Create prompt that describes available tools
tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])

prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a helpful assistant with access to these tools:
{tool_descriptions}

When asked a question, explain which tool you would use and why."""),
    ("human", "{question}")
])

chain = prompt | llm
response = chain.invoke({"question": "How long is the word 'programming'?"})
print(f"LLM Response: {response.content}\n")

# Now actually call the tool
result = get_word_length.invoke("programming")
print(f"Actual tool result: {result}\n")

# =============================================================================
# EXAMPLE 7: Tool Calling with bind_tools (Modern Approach)
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: LLM with Tool Calling (bind_tools)")
print("=" * 60)

@tool
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather for a location.
    
    Args:
        location: The city name
        unit: Temperature unit (celsius or fahrenheit)
    """
    # Simulated weather data
    weather_data = {
        "san francisco": {"celsius": "18°C", "fahrenheit": "64°F", "condition": "Foggy"},
        "new york": {"celsius": "22°C", "fahrenheit": "72°F", "condition": "Sunny"},
        "london": {"celsius": "15°C", "fahrenheit": "59°F", "condition": "Rainy"},
    }
    city_data = weather_data.get(location.lower(), {"celsius": "20°C", "fahrenheit": "68°F", "condition": "Unknown"})
    temp = city_data.get(unit, city_data["celsius"])
    return f"Weather in {location}: {temp}, {city_data['condition']}"

# Bind tools to LLM
llm_with_tools = llm.bind_tools([get_current_weather])

# LLM will decide to call the tool
response = llm_with_tools.invoke("What's the weather in San Francisco?")
print(f"LLM Response with tool calls: {response}\n")

# Check if LLM wants to call tools
if hasattr(response, 'tool_calls') and response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool to call: {tool_call['name']}")
        print(f"Arguments: {tool_call['args']}\n")
        
        # Execute the tool
        result = get_current_weather.invoke(tool_call['args'])
        print(f"Tool result: {result}\n")

# =============================================================================
# EXAMPLE 8: Multiple Tools with Selection
# =============================================================================
print("=" * 60)
print("EXAMPLE 8: Multiple Tools - LLM Selects Appropriate One")
print("=" * 60)

@tool
def book_flight(destination: str, date: str) -> str:
    """Book a flight to a destination on a specific date."""
    return f"Flight booked to {destination} on {date}"

@tool
def book_hotel(city: str, checkin: str, nights: int) -> str:
    """Book a hotel in a city for specified nights."""
    return f"Hotel booked in {city}, checking in {checkin} for {nights} nights"

@tool
def book_restaurant(restaurant: str, time: str, guests: int) -> str:
    """Make a restaurant reservation."""
    return f"Table reserved at {restaurant} for {guests} guests at {time}"

travel_tools = [book_flight, book_hotel, book_restaurant]
llm_with_travel_tools = llm.bind_tools(travel_tools)

# LLM chooses the right tool
queries = [
    "Book a flight to Paris for June 15th",
    "Reserve a table for 4 at Mario's Restaurant at 7pm",
    "Book a hotel in Tokyo from May 1st for 3 nights"
]

for query in queries:
    response = llm_with_travel_tools.invoke(query)
    print(f"Query: {query}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"Selected tool: {tool_call['name']}")
            print(f"Arguments: {tool_call['args']}\n")

# =============================================================================
# EXAMPLE 9: Tool with Error Handling
# =============================================================================
print("=" * 60)
print("EXAMPLE 9: Tool with Error Handling")
print("=" * 60)

@tool
def divide_numbers(numerator: float, denominator: float) -> str:
    """Divide two numbers safely.
    
    Args:
        numerator: The number to divide
        denominator: The number to divide by
    """
    try:
        if denominator == 0:
            return "Error: Cannot divide by zero"
        result = numerator / denominator
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Test error handling
print(divide_numbers.invoke({"numerator": 10, "denominator": 2}))
print(divide_numbers.invoke({"numerator": 10, "denominator": 0}))
print()

# =============================================================================
# EXAMPLE 10: API Tool Example
# =============================================================================
print("=" * 60)
print("EXAMPLE 10: Creating an API Tool")
print("=" * 60)

import requests
from typing import Optional

@tool
def fetch_github_user(username: str) -> str:
    """Fetch GitHub user information.
    
    Args:
        username: GitHub username
    """
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            data = response.json()
            return f"User: {data['name']}, Public Repos: {data['public_repos']}, Followers: {data['followers']}"
        else:
            return f"Error: User not found or API error"
    except Exception as e:
        return f"Error: {str(e)}"

# Test the API tool
result = fetch_github_user.invoke("torvalds")
print(f"GitHub API result: {result}\n")

# =============================================================================
# EXAMPLE 11: Tool with File Operations
# =============================================================================
print("=" * 60)
print("EXAMPLE 11: File Operation Tools")
print("=" * 60)

@tool
def write_file(filename: str, content: str) -> str:
    """Write content to a file.
    
    Args:
        filename: Name of the file to write
        content: Content to write to the file
    """
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@tool
def read_file(filename: str) -> str:
    """Read content from a file.
    
    Args:
        filename: Name of the file to read
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File {filename} not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Test file tools
write_result = write_file.invoke({
    "filename": "test_langchain.txt",
    "content": "This is a test file created by LangChain tools!"
})
print(write_result)

read_result = read_file.invoke({"filename": "test_langchain.txt"})
print(f"File content: {read_result}\n")

# =============================================================================
# EXAMPLE 12: Combining Tools with LCEL
# =============================================================================
print("=" * 60)
print("EXAMPLE 12: Tools in LCEL Chain")
print("=" * 60)

from langchain_core.runnables import RunnableLambda

@tool
def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text (simplified version).
    
    Args:
        text: Text to analyze
    """
    positive_words = ['good', 'great', 'excellent', 'happy', 'wonderful']
    negative_words = ['bad', 'terrible', 'awful', 'sad', 'poor']
    
    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    
    if pos_count > neg_count:
        return "Positive sentiment"
    elif neg_count > pos_count:
        return "Negative sentiment"
    else:
        return "Neutral sentiment"

# Create a chain that uses the tool
from langchain_core.output_parsers import StrOutputParser

sentiment_chain = (
    ChatPromptTemplate.from_template("Generate a {sentiment_type} review of a restaurant")
    | llm
    | StrOutputParser()
    | RunnableLambda(lambda review: {
        "review": review,
        "sentiment": analyze_sentiment.invoke(review)
    })
)

result = sentiment_chain.invoke({"sentiment_type": "positive"})
print(f"Generated review: {result['review']}")
print(f"Detected sentiment: {result['sentiment']}\n")

"""
KEY TAKEAWAYS:
--------------
1. Tools extend LLM capabilities to interact with external systems
2. @tool decorator: Easiest way to create simple tools
3. Tool class: For more control over tool definition
4. StructuredTool: For complex parameter schemas using Pydantic
5. bind_tools(): Modern way to give LLM access to tools
6. Tool description is CRITICAL - LLM uses it to decide when to call tool
7. Tools should have clear, specific names and descriptions
8. Always handle errors in tool functions
9. Built-in tools available: Search, Wikipedia, Calculator, etc.
10. Tools can do anything: API calls, file ops, database queries, etc.

TOOL DESIGN BEST PRACTICES:
----------------------------
1. Clear Names: Use descriptive, action-oriented names
2. Detailed Descriptions: Explain what tool does and when to use it
3. Type Hints: Use Python type hints for parameters
4. Error Handling: Always handle potential errors gracefully
5. Single Responsibility: Each tool should do one thing well
6. Input Validation: Validate inputs before processing
7. Return Strings: Tools typically return string results
8. Document Parameters: Use Pydantic Field descriptions
9. Keep Simple: Tools should be focused and not too complex
10. Test Independently: Tools should work standalone

WHEN TO USE TOOLS:
------------------
✅ Need real-time data (web search, APIs)
✅ Perform calculations or data processing
✅ Access databases or file systems
✅ Call external services
✅ Extend LLM capabilities beyond text generation
✅ Need deterministic operations
✅ Integrate with existing systems

NEXT STEPS:
-----------
- 05_memory.py - Add conversation memory
- 06_chain_building.py - Build complex chains
- 07_agents.py - Let LLMs autonomously use tools
"""

print("=" * 60)
print("Tools concepts complete!")
print("=" * 60)

# Cleanup
import os
if os.path.exists("test_langchain.txt"):
    os.remove("test_langchain.txt")
