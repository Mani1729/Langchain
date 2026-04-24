"""
LangGraph - Advanced Agent Framework
=====================================

THEORY:
-------
LangGraph is LangChain's library for building stateful, multi-actor applications with LLMs.
It extends LangChain with graph-based agent orchestration for complex, controllable workflows.

WHY LANGGRAPH?
--------------
In LangChain 0.2+, the classic AgentExecutor and agent creation functions were moved to LangGraph
because agents need:
1. State Management - Track conversation and tool results
2. Cycles - Allow repeated tool calls and reasoning loops
3. Control Flow - Explicit routing between nodes
4. Persistence - Save and resume agent state
5. Human-in-the-Loop - Pause for human approval
6. Streaming - Stream intermediate steps

KEY CONCEPTS:
-------------
1. StateGraph - Defines the flow of your application
2. Nodes - Functions that process state (LLM calls, tool executions)
3. Edges - Connections between nodes (conditional or unconditional)
4. State - Shared data structure passed between nodes
5. Checkpointer - Persistence layer for state
6. Prebuilt Agents - Ready-to-use agent implementations

REACT PATTERN IN LANGGRAPH:
---------------------------
ReAct (Reasoning + Acting) is a framework where agents:
1. THINK - Reason about what to do next
2. ACT - Call a tool with specific inputs
3. OBSERVE - See the tool's result
4. REPEAT - Continue until task is complete
5. RESPOND - Provide final answer

LangGraph's create_react_agent implements this pattern as a graph:
- Agent Node: LLM decides on action
- Tools Node: Executes selected tools
- Conditional Edge: Routes based on agent decision
- State: Maintains message history

AGENT EXECUTOR VS LANGGRAPH:
-----------------------------
Old Way (AgentExecutor):
- Black box execution
- Limited control over flow
- Hard to customize
- No built-in persistence

New Way (LangGraph):
- Explicit graph structure
- Full control over each step
- Easy to customize nodes/edges
- Built-in checkpointing
- Stream intermediate steps
- Human-in-the-loop support

GRAPH STRUCTURE:
----------------
        START
          |
          v
    +----------+
    |  Agent   | <---- (Reasoning)
    |   LLM    |
    +----------+
          |
          v (should_continue?)
      /       \
     /         \
    v           v
[Tools]     [END]
    |
    +---> (back to Agent)

STATE MANAGEMENT:
-----------------
LangGraph uses TypedDict or Pydantic models to define state:
- Messages: Chat history
- Agent scratchpad: Internal reasoning
- Custom fields: Any additional data

State reducers determine how updates merge:
- add_messages: Append new messages
- override: Replace value
- custom: Your own logic
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Note: LangGraph requires installation
# Run: pip install langgraph

try:
    from langgraph.graph import StateGraph, MessagesState, START, END
    from langgraph.graph.message import add_messages
    from langgraph.prebuilt import ToolNode
    from langgraph.checkpoint.memory import MemorySaver
    from langchain.agents import create_agent
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
    
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("=" * 60)
    print("⚠️  LangGraph not installed!")
    print("=" * 60)
    print("To use LangGraph agents, install it:")
    print("  pip install langgraph")
    print("\nLangGraph provides:")
    print("  - create_agent (ReAct pattern - latest API)")
    print("  - AgentExecutor-like functionality")
    print("  - State management for agents")
    print("  - Human-in-the-loop capabilities")
    print("  - Agent checkpointing and persistence")
    print("=" * 60)
    sys.exit(0)

# Configure Azure OpenAI
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o-mini",
    temperature=0
)

# =============================================================================
# EXAMPLE 1: Simple ReAct Agent with create_react_agent
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: ReAct Agent with create_agent (Latest API)")
print("=" * 60)

@tool
def calculator(expression: str) -> str:
    """Useful for performing mathematical calculations. 
    Input should be a valid Python mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_word_count(text: str) -> str:
    """Count the number of words in a given text."""
    word_count = len(text.split())
    return f"The text contains {word_count} words"

# Define tools
tools = [calculator, get_word_count]

# Create ReAct agent using prebuilt function
# This is the modern replacement for AgentExecutor!
react_agent = create_agent(llm, tools)

print("\nReAct Agent Structure:")
print("- Agent uses ReAct pattern (Reason -> Act -> Observe)")
print("- Automatically loops until task is complete")
print("- Built-in tool calling and result processing")

# Test the agent
print("\n--- Query 1: Simple Calculation ---")
result = react_agent.invoke({
    "messages": [HumanMessage(content="What is 127 multiplied by 43?")]
})
print(f"Final Answer: {result['messages'][-1].content}")

print("\n--- Query 2: Word Count ---")
result = react_agent.invoke({
    "messages": [HumanMessage(content="How many words in 'LangGraph makes agent building easier'?")]
})
print(f"Final Answer: {result['messages'][-1].content}")

# =============================================================================
# EXAMPLE 2: ReAct Agent with Conversation History
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: ReAct Agent with Memory")
print("=" * 60)

# Add checkpointer for conversation persistence
memory = MemorySaver()
agent_with_memory = create_agent(llm, tools, checkpointer=memory)

# Use thread_id to maintain conversation context
config = {"configurable": {"thread_id": "conversation-1"}}

print("\n--- First Query ---")
result = agent_with_memory.invoke({
    "messages": [HumanMessage(content="Calculate 15 plus 27")]
}, config)
print(f"Answer: {result['messages'][-1].content}")

print("\n--- Follow-up Query (uses memory) ---")
result = agent_with_memory.invoke({
    "messages": [HumanMessage(content="Now multiply that result by 3")]
}, config)
print(f"Answer: {result['messages'][-1].content}")

print("\n--- New Thread (fresh context) ---")
config2 = {"configurable": {"thread_id": "conversation-2"}}
result = agent_with_memory.invoke({
    "messages": [HumanMessage(content="What was the previous calculation?")]
}, config2)
print(f"Answer: {result['messages'][-1].content}")

# =============================================================================
# EXAMPLE 3: Custom StateGraph Agent (Manual ReAct Pattern)
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: Custom StateGraph Agent")
print("=" * 60)

# Define custom state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    iterations: int

@tool
def weather_tool(city: str) -> str:
    """Get weather for a city."""
    weather_db = {
        "london": "Rainy, 15°C",
        "paris": "Sunny, 22°C",
        "tokyo": "Cloudy, 18°C"
    }
    return weather_db.get(city.lower(), "Weather data not available")

custom_tools = [calculator, weather_tool]
tool_map = {tool.name: tool for tool in custom_tools}

# Bind tools to LLM
llm_with_tools = llm.bind_tools(custom_tools)

# Define agent node
def call_agent(state: AgentState) -> AgentState:
    """Agent node: LLM decides what to do"""
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response],
        "iterations": state.get("iterations", 0) + 1
    }

# Define tool execution node
def call_tools(state: AgentState) -> AgentState:
    """Tools node: Execute selected tools"""
    last_message = state["messages"][-1]
    tool_messages = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        print(f"  Calling tool: {tool_name}({tool_args})")
        
        if tool_name in tool_map:
            result = tool_map[tool_name].invoke(tool_args)
            print(f"  Tool result: {result}")
            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
    
    return {"messages": tool_messages}

# Define conditional edge logic
def should_continue(state: AgentState) -> str:
    """Determine if agent should continue or end"""
    last_message = state["messages"][-1]
    
    # Check max iterations
    if state.get("iterations", 0) >= 5:
        return "end"
    
    # If LLM didn't call tools, we're done
    if not last_message.tool_calls:
        return "end"
    
    # Continue to tools
    return "continue"

# Build the graph
graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("agent", call_agent)
graph_builder.add_node("tools", call_tools)

# Add edges
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)
graph_builder.add_edge("tools", "agent")

# Compile the graph
custom_agent = graph_builder.compile()

print("\nCustom Graph Structure:")
print("  START -> agent -> [conditional] -> tools -> agent -> END")
print("  Agent decides, tools execute, repeat until done")

# Test custom agent
print("\n--- Query: Combined Operations ---")
result = custom_agent.invoke({
    "messages": [HumanMessage(content="What's the weather in London? Also calculate 100 + 50")],
    "iterations": 0
})
print(f"\nFinal Answer: {result['messages'][-1].content}")

# =============================================================================
# EXAMPLE 4: Agent with Streaming
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Streaming Agent Output")
print("=" * 60)

print("\n--- Streaming Query ---")
print("Query: Calculate 25 * 4 and tell me the result")

for chunk in react_agent.stream({
    "messages": [HumanMessage(content="Calculate 25 * 4 and tell me the result")]
}):
    print(f"Step: {list(chunk.keys())}")
    if "agent" in chunk:
        messages = chunk["agent"]["messages"]
        if messages and messages[-1].content:
            print(f"  Agent: {messages[-1].content[:100]}")
    elif "tools" in chunk:
        print(f"  Tools: Executing...")

# =============================================================================
# EXAMPLE 5: Multi-Tool ReAct Agent with Complex Reasoning
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Complex Multi-Step ReAct Agent")
print("=" * 60)

@tool
def search_database(query: str) -> str:
    """Search internal database for company information."""
    db = {
        "employees": "500 employees",
        "revenue": "$10 million annual revenue",
        "founded": "Founded in 2020"
    }
    for key, value in db.items():
        if key in query.lower():
            return value
    return "No information found"

@tool
def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text. Returns: positive, negative, or neutral."""
    positive_words = ['good', 'great', 'excellent', 'happy']
    negative_words = ['bad', 'terrible', 'hate', 'sad']
    
    text_lower = text.lower()
    if any(word in text_lower for word in positive_words):
        return "positive"
    elif any(word in text_lower for word in negative_words):
        return "negative"
    return "neutral"

# Create comprehensive agent
complex_tools = [calculator, weather_tool, search_database, analyze_sentiment]
complex_agent = create_agent(llm, complex_tools)

print("\n--- Complex Multi-Step Query ---")
result = complex_agent.invoke({
    "messages": [HumanMessage(content="""
        Please do the following:
        1. Search for information about employees
        2. Calculate 500 divided by 10
        3. Analyze the sentiment of 'This is excellent work'
    """)]
})

print(f"\nAgent completed task!")
print(f"Final Answer: {result['messages'][-1].content}")

# =============================================================================
# EXAMPLE 6: Visualizing the Agent Graph
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: Understanding Agent Graph Structure")
print("=" * 60)

print("\nReAct Agent Graph Visualization:")
print("""
┌─────────┐
│  START  │
└────┬────┘
     │
     ▼
┌─────────────┐
│   Agent     │ ◄─────┐
│   (LLM)     │       │
│ - Reasoning │       │
│ - Decision  │       │
└──────┬──────┘       │
       │              │
       ▼              │
   (should_continue?) │
       │              │
    ┌──┴──┐           │
    │     │           │
    ▼     ▼           │
  END  ┌──────────┐   │
       │  Tools   │───┘
       │ Execute  │
       └──────────┘

State Flow:
1. Agent receives messages
2. LLM decides: Use tool or finish?
3. If tool: Execute & add result to messages
4. Loop back to Agent with updated state
5. If done: Return final answer
""")

print("\nState Structure:")
print({
    "messages": [
        "HumanMessage: User query",
        "AIMessage: Agent decision/reasoning",
        "ToolMessage: Tool results",
        "AIMessage: Final answer"
    ],
    "iterations": "Counter to prevent infinite loops"
})

"""
KEY DIFFERENCES: AgentExecutor vs LangGraph
===========================================

AgentExecutor (Deprecated):
✗ Black box - hard to debug
✗ Limited customization
✗ No built-in streaming of steps
✗ No human-in-the-loop
✗ No state persistence
✗ No graph visualization

LangGraph create_react_agent:
✓ Transparent graph structure
✓ Fully customizable nodes/edges
✓ Stream intermediate steps
✓ Easy human-in-the-loop
✓ Built-in checkpointing
✓ Visual graph representation
✓ Better error handling
✓ Async support

REACT PATTERN COMPONENTS:
=========================

1. State Management:
   - MessagesState: Built-in message tracking
   - Custom state: Add your own fields
   - Reducers: Control how state updates

2. Agent Node:
   - LLM with bound tools
   - Decides next action
   - Returns AIMessage with tool_calls or content

3. Tools Node:
   - Executes selected tools
   - Returns ToolMessages
   - Handles errors gracefully

4. Conditional Edges:
   - Route based on agent decision
   - Check for tool_calls
   - Implement max iterations
   - Add custom logic

5. Checkpointing:
   - MemorySaver: In-memory persistence
   - SqliteSaver: Database persistence
   - Custom: Implement your own

WHEN TO USE LANGGRAPH:
======================
✓ Need complex agent workflows
✓ Want full control over agent logic
✓ Require state persistence
✓ Need human-in-the-loop
✓ Want to stream intermediate steps
✓ Building production agents
✓ Need multi-agent coordination
✓ Require debugging visibility

BEST PRACTICES:
===============
1. Start with create_react_agent for simple cases
2. Use custom StateGraph for complex workflows
3. Always add max_iterations check
4. Implement proper error handling
5. Use checkpointers for persistence
6. Stream for better UX
7. Add logging for debugging
8. Test tool combinations
9. Validate state updates
10. Monitor token usage

REACT PATTERN FLOW:
===================
1. Initialize: Start with user query
2. Reason: LLM analyzes what to do
3. Act: Select and call appropriate tool
4. Observe: Receive tool result
5. Repeat: Continue with updated context
6. Respond: Provide final answer

This pattern allows agents to:
- Break down complex tasks
- Use tools dynamically
- Adapt based on results
- Handle multi-step reasoning
- Recover from errors

MIGRATION FROM OLD AGENTS:
==========================
Old Code:
```python
from langchain.agents import AgentExecutor, create_react_agent
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": query})
```

New Code (Latest - LangChain v1.0+):
```python
from langchain.agents import create_agent
agent = create_agent(llm, tools)
result = agent.invoke({"messages": [HumanMessage(content=query)]})
```

Benefits:
- Cleaner API
- Better state management
- Built-in streaming
- Easier customization
- Better debugging

NEXT STEPS:
===========
- Explore multi-agent systems in LangGraph
- Implement human-in-the-loop workflows
- Use checkpointers for production
- Build custom agent architectures
- Integrate with LangSmith for monitoring
"""

print("=" * 60)
print("✓ LangGraph Agent Concepts Complete!")
print("=" * 60)
print("\nYou now understand:")
print("  - ReAct pattern implementation")
print("  - create_agent (latest API - modern AgentExecutor)")
print("  - Custom StateGraph agents")
print("  - State management and persistence")
print("  - Streaming agent outputs")
print("  - Graph-based agent architecture")
