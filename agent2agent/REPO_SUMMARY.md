# Agent2Agent Repository Summary

## Overview
Agent2Agent is a demonstration repository showcasing practical implementations of the A2A SDK through concrete multi-agent systems. It provides working examples of agent-to-agent communication patterns, including a simple starter example and a complex multi-framework scheduling system.

## Repository Purpose
- Demonstrate A2A SDK practical usage
- Provide reference implementations for common patterns
- Show multi-agent orchestration with different frameworks
- Illustrate real-world integration scenarios
- Enable developers to learn by example

## Key Subprojects

### 1. A2A Simple (`a2a_simple/`)

**Purpose**: Entry-level example of A2A agent communication

**Components**:
- Single A2A-compliant agent
- Test client for agent communication
- Minimal dependencies for quick learning
- Clear code examples

**Technologies**:
- A2A SDK (Python)
- Python 3.13
- LangChain (basic integration)

**Key Concepts**:
- Agent registration and discovery
- Basic message sending/receiving
- Simple request-response pattern
- Error handling fundamentals

### 2. Friend Scheduling Multi-Agent System (`a2a_friend_scheduling/`)

**Purpose**: Demonstrate complex multi-agent orchestration with framework interoperability

**Architecture Pattern**: Master-Worker with Heterogeneous Agents

**System Components**:
```
Host Agent (Orchestrator)
    ├─→ Kaitlynn Agent (LangGraph)
    ├─→ Nate Agent (CrewAI)
    ├─→ Karley Agent (ADK - Agent Development Kit)
    └─→ Google Calendar API (External Service)
```

**Agent Responsibilities**:
- **Host Agent**: Orchestrates scheduling requests, aggregates responses
- **Kaitlynn (LangGraph)**: Manages availability using LangGraph state machine
- **Nate (CrewAI)**: Handles scheduling using CrewAI task framework
- **Karley (ADK)**: Manages calendar integration via ADK framework

**Technologies**:
- A2A SDK for inter-agent communication
- LangGraph framework (Kaitlynn)
- CrewAI framework (Nate)
- ADK (Agent Development Kit) - Karley
- Google Calendar API for integration
- Python 3.13
- Multi-framework orchestration

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Protocol** | A2A Protocol |
| **Core SDK** | A2A SDK (Python) |
| **Agent Frameworks** | LangGraph, CrewAI, ADK |
| **Python Version** | 3.13 |
| **External Integration** | Google Calendar API |
| **Development** | Virtual environment (venv) |

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│              User / External System                     │
│           (Scheduling Request)                          │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────▼────────────────────┐
        │    Host Agent (A2A Server)         │
        │   ┌─────────────────────────────┐  │
        │   │  Orchestration Logic        │  │
        │   │  - Schedule request parse   │  │
        │   │  - Route to agents          │  │
        │   │  - Aggregate responses      │  │
        │   └─────────────────────────────┘  │
        └────┬──────────┬──────────┬──────────┘
             │          │          │
    ┌────────▼───┐ ┌───▼──────┐ ┌─▼────────────┐
    │ Kaitlynn   │ │   Nate   │ │   Karley     │
    │ (LangGraph)│ │ (CrewAI) │ │   (ADK)      │
    │            │ │          │ │              │
    │ Manages    │ │ Handles  │ │ Manages      │
    │ via State  │ │ with     │ │ calendar     │
    │ Machine    │ │ Tasks    │ │ integration  │
    └────────────┘ └──────────┘ └──────────────┘
         │              │              │
         └──────────────┴──────────────┘
                 │
        ┌────────▼─────────┐
        │ Google Calendar  │
        │ (External API)   │
        └──────────────────┘
```

## Design Patterns

### 1. **Multi-Agent Orchestration**
- Central host agent coordinates multiple specialized agents
- Agents operate independently with common interface
- Framework-agnostic communication via A2A Protocol

### 2. **Framework Interoperability**
- Different agents use different frameworks
- A2A Protocol abstracts framework differences
- Seamless coordination across heterogeneous systems

### 3. **Distributed Availability Management**
- Each agent manages its own availability
- Parallel queries to multiple agents
- Aggregated scheduling decision

### 4. **Master-Worker Pattern**
- Host agent: controller and aggregator
- Friend agents: task executors
- Centralized coordination with distributed execution

## Main Features

1. **Simple A2A Example**: Quick start for understanding A2A
2. **Production-Ready Pattern**: Friend scheduling demonstrates real-world complexity
3. **Multi-Framework Support**: Shows interoperability between LangGraph, CrewAI, ADK
4. **Calendar Integration**: Real-world API integration (Google Calendar)
5. **Parallel Execution**: Agents respond simultaneously for efficiency
6. **Error Handling**: Graceful handling of agent failures
7. **Type Safety**: Clear message contracts via A2A Protocol
8. **Observability**: Logging and tracing of agent interactions

## Key Concepts

### A2A Communication Layer
- Standardized message format for all agents
- Agent discovery and registration
- Automatic message routing
- Built-in error handling

### Scheduling Problem Domain
- Multi-calendar coordination
- Availability aggregation
- Conflict resolution
- Time zone handling

### Framework Abstraction
- Each agent uses native framework features
- A2A Protocol provides communication layer
- No framework pollution across agents
- Language-agnostic at system level

## File Structure

```
agent2agent/
├── a2a_simple/
│   ├── agent.py              # Simple A2A agent
│   ├── client.py             # Test client
│   ├── __main__.py           # Entry point
│   └── README.md             # Quick start guide
│
├── a2a_friend_scheduling/
│   ├── host_agent/
│   │   ├── agent.py          # Orchestration logic
│   │   └── prompts.py        # System prompts
│   │
│   ├── kaitlynn_agent/       # LangGraph implementation
│   │   ├── graph.py          # State machine
│   │   └── agent.py
│   │
│   ├── nate_agent/           # CrewAI implementation
│   │   ├── crew.py           # Crew definition
│   │   └── tasks.py
│   │
│   ├── karley_agent/         # ADK implementation
│   │   ├── agent.py
│   │   └── calendar.py
│   │
│   ├── config/
│   │   └── google_calendar_config.yaml
│   │
│   ├── main.py               # System entry point
│   └── README.md             # Documentation
│
└── README.md                 # Project overview
```

## Configuration

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
pip install a2a-sdk langgraph crewai adk-framework
```

### Google Calendar Integration
- Service account credentials required
- OAuth flow for user authorization
- Calendar API enabled in GCP project
- Scopes: calendar read/write

## Integration Points

1. **A2A Protocol**: Core inter-agent communication
2. **Google Calendar API**: External scheduling data source
3. **LangGraph**: State management for Kaitlynn
4. **CrewAI**: Task orchestration for Nate
5. **ADK**: Framework for Karley
6. **User Input**: Scheduling requests and preferences

## Use Cases

- Learning A2A Protocol implementation
- Multi-agent system design patterns
- Cross-framework agent coordination
- Real-world integration examples
- Proof of concept for complex agents systems

## Running the Examples

### Simple Example
```bash
cd a2a_simple
python -m __main__
```

### Friend Scheduling
```bash
cd a2a_friend_scheduling
python main.py --schedule-query "Find time for all to meet"
```

## Best Practices Demonstrated

1. Clear separation of concerns
2. Standardized interfaces (A2A Protocol)
3. Framework-specific implementations in isolated modules
4. Comprehensive error handling
5. Logging and observability
6. Configuration management
7. Documentation and examples
8. Type hints for clarity

## Learning Path

1. Start with `a2a_simple` for basics
2. Understand message structure and routing
3. Study `friend_scheduling` for complex patterns
4. Learn each framework's agent implementation
5. Understand orchestration logic in host agent
6. Review Google Calendar integration
7. Implement custom agents following patterns
