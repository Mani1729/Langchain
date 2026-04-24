"""
Agents in LangChain
===================

THEORY:
-------
Agents use LLMs to decide which tools to call and in what order.
Unlike chains (predefined steps), agents make dynamic decisions.

Key Concepts:
1. Agent - LLM that decides what actions to take
2. Tools - Functions the agent can call
3. AgentExecutor - Runtime that executes agent decisions
4. ReAct - Reasoning + Acting framework
5. Agent Types - Different reasoning strategies

Agent Components:
- LLM: The decision-making brain
- Tools: Available actions
- Prompt: Instructions and formatting
- Memory: Conversation history (optional)
- Output Parser: Interpret agent's decisions

Agent Types:
1. ReAct Agent - Reason about what to do, then act
2. OpenAI Functions Agent - Uses OpenAI's function calling
3. Structured Chat Agent - For multi-input tools
4. Self-Ask Agent - Breaks down questions
5. Plan-and-Execute Agent - Plans then executes

ReAct Pattern:
1. Thought: Agent thinks about what to do
2. Action: Agent chooses a tool to use
3. Action Input: Agent specifies tool parameters
4. Observation: Tool returns result
5. Repeat until done
6. Final Answer: Agent provides final response
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0
)

# =============================================================================
# EXAMPLE 1: Simple Agent with Tool Calling
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Simple Agent with Tool Calling")
print("=" * 60)

@tool
def calculator(expression: str) -> str:
    """Useful for performing mathematical calculations. 
    Input should be a valid Python mathematical expression like '5 + 3' or '10 * 2'."""
    try:
        result = eval(expression)
        return f"The result is {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def word_counter(text: str) -> str:
    """Count the number of words in a given text.
    Input should be a string of text."""
    word_count = len(text.split())
    return f"The text contains {word_count} words"

# Create tools list
tools = [calculator, word_counter]
tool_map = {tool.name: tool for tool in tools}

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

def run_agent(query: str, max_iterations: int = 3):
    """Simple agent loop"""
    print(f"\nQuery: {query}")
    messages = [HumanMessage(content=query)]
    
    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        # LLM decides what to do
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        # Check if LLM wants to use tools
        if not response.tool_calls:
            print(f"Final Answer: {response.content}")
            return response.content
        
        # Execute tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            print(f"Tool: {tool_name}, Args: {tool_args}")
            
            # Call the tool
            if tool_name in tool_map:
                tool_result = tool_map[tool_name].invoke(tool_args)
                print(f"Tool Result: {tool_result}")
                
                # Add tool result to messages
                messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call['id']
                ))
    
    return "Max iterations reached"

# Test the agent
result1 = run_agent("What is 127 multiplied by 43?")
result2 = run_agent("How many words are in 'LangChain makes building LLM applications easy'?")

# =============================================================================
# EXAMPLE 2: Multi-Step Agent Reasoning
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Multi-Step Agent Reasoning")
print("=" * 60)

# Agent that needs multiple tool calls
result = run_agent("Calculate 15 plus 27, then tell me how many words are in the phrase 'artificial intelligence'")

# =============================================================================
# EXAMPLE 3: Agent with Multiple Tool Types
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: Agent with Various Tool Types")
print("=" * 60)

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city.
    Input should be a city name."""
    # Simulated weather data
    weather_db = {
        "london": "Rainy, 15°C",
        "paris": "Sunny, 22°C",
        "tokyo": "Cloudy, 18°C",
        "new york": "Snowy, 2°C"
    }
    return weather_db.get(city.lower(), "Weather data not available")

@tool
def search_database(query: str) -> str:
    """Search internal database for information.
    Input should be a search query."""
    # Simulated database
    db = {
        "ceo": "The CEO is John Smith",
        "headquarters": "Headquarters is in San Francisco",
        "employees": "The company has 500 employees"
    }
    for key, value in db.items():
        if key in query.lower():
            return value
    return "No information found"

# Add new tools to our tool map
multi_tools = [calculator, word_counter, get_weather, search_database]
multi_tool_map = {tool.name: tool for tool in multi_tools}
llm_multi_tools = llm.bind_tools(multi_tools)

def run_multi_tool_agent(query: str):
    """Agent with multiple tools"""
    print(f"\nQuery: {query}")
    messages = [HumanMessage(content=query)]
    
    for i in range(3):
        response = llm_multi_tools.invoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            print(f"Answer: {response.content}")
            return response.content
        
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            print(f"Using tool: {tool_name}({tool_args})")
            
            if tool_name in multi_tool_map:
                tool_result = multi_tool_map[tool_name].invoke(tool_args)
                print(f"Result: {tool_result}")
                messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call['id']
                ))
    return "Complete"

result = run_multi_tool_agent("What's the weather in London? Also, who is the CEO?")

# =============================================================================
# EXAMPLE 4: Agent with Multi-Step Reasoning
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Agent with Multi-Step Reasoning")
print("=" * 60)

# The agent can chain multiple tool calls together
result = run_agent("Calculate 10 + 5, then multiply that result by 3")

# =============================================================================
# EXAMPLE 5: Custom Agent Decision Making
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Agent Decision Making Process")
print("=" * 60)

@tool
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of text.
    Returns: positive, negative, or neutral."""
    positive_words = ['good', 'great', 'excellent', 'happy', 'love']
    negative_words = ['bad', 'terrible', 'hate', 'sad', 'awful']
    
    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"

@tool
def recommend_action(sentiment: str) -> str:
    """Recommend action based on sentiment.
    Input: positive, negative, or neutral"""
    recommendations = {
        "positive": "Continue with current approach!",
        "negative": "Need improvement. Consider revisions.",
        "neutral": "Maintain status quo. Monitor situation."
    }
    return recommendations.get(sentiment.lower(), "No recommendation available")

decision_tools = [analyze_sentiment, recommend_action]
decision_tool_map = {tool.name: tool for tool in decision_tools}
llm_decision = llm.bind_tools(decision_tools)

def run_decision_agent(query: str):
    """Agent that chains decision-making tools"""
    messages = [HumanMessage(content=query)]
    
    for _ in range(3):
        response = llm_decision.invoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            print(f"Final Answer: {response.content}")
            return response.content
        
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            result = decision_tool_map[tool_name].invoke(tool_call['args'])
            print(f"Tool: {tool_name}, Result: {result}")
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call['id']))
    
    return "Complete"

result = run_decision_agent("Analyze this review and recommend action: 'The product is excellent and I love it!'")



"""
KEY TAKEAWAYS:
--------------
1. Agents use LLMs to dynamically decide which tools to use
2. ReAct pattern: Thought -> Action -> Observation loop
3. AgentExecutor runs the agent with tools
4. Tools must have clear names and descriptions
5. Agents can use multiple tools in sequence
6. Memory allows agents to remember context
7. Error handling prevents agent failures
8. Max iterations prevents infinite loops
9. Return intermediate steps for debugging
10. Different agent types for different use cases

AGENT TYPES:
------------
1. OpenAI Functions Agent - Best for OpenAI models
2. ReAct Agent - Explicit reasoning steps
3. Structured Chat Agent - For complex tool inputs
4. Self-Ask Agent - Breaks down complex questions
5. Plan-and-Execute - Plans then executes strategy

WHEN TO USE AGENTS:
-------------------
✅ Need dynamic tool selection
✅ Multi-step reasoning required
✅ Don't know sequence of operations in advance
✅ Need to respond to intermediate results
✅ Complex problem solving
✅ Interactive applications
❌ Simple, predictable workflows (use chains instead)
❌ When you need guaranteed execution order

AGENT DESIGN BEST PRACTICES:
-----------------------------
1. Clear Tool Descriptions - Critical for agent decisions
2. Limit Tool Count - Too many tools confuse the agent
3. Set Max Iterations - Prevent runaway execution
4. Handle Errors - Tools can fail
5. Add Memory - For conversational agents
6. Log Intermediate Steps - For debugging
7. Test Tool Combinations - Ensure they work together
8. Use Appropriate Model - More capable models = better agents
9. Validate Tool Outputs - Don't trust blindly
10. Set Timeouts - Prevent long-running operations

NEXT STEPS:
-----------
- 08_multi_agent.py - Multi-agent systems
- 09_langsmith.py - LangSmith for monitoring
"""

print("=" * 60)
print("Agents concepts complete!")
print("=" * 60)
