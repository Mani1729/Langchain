# Deepagents Repository Summary

## Overview
Deepagents is an open-source agent harness implementing planning, computer/shell access, and sub-agent delegation. It provides reusable infrastructure for building autonomous agents capable of long-horizon task execution, from hours to days, with human oversight and extensibility through middleware patterns.

## Repository Purpose
- Provide production-ready agent execution harness
- Enable long-running autonomous task execution
- Support hierarchical task delegation (sub-agents)
- Offer extensible middleware architecture
- Implement tools for filesystem and shell access
- Enable human-in-the-loop oversight

## Core Architecture Components

### 1. **Core Library** (`libs/deepagents/`)
- Agent execution engine
- Planning and reasoning
- Tool management
- State persistence

### 2. **CLI Interface** (`libs/deepagents-cli/`)
- Interactive command-line interface
- Agent configuration and management
- Task execution monitoring
- Result visualization

### 3. **Backend Services** (`harbor/`)
- API server for agent interaction
- Persistence layer
- Multi-agent coordination
- Logging and monitoring

### 4. **Additional Components** (`libs/acp/`)
- Extended capabilities
- Custom tool implementations
- Integration modules

## Key Concepts

### Planning Before Execution
- Agent plans entire workflow before execution
- Breaks complex tasks into subtasks
- Reasons about dependencies and constraints
- Adjusts plan based on execution feedback

### Computer Access (Shell & Filesystem)
- Execute arbitrary shell commands
- Read/write filesystem operations
- Directory navigation and exploration
- Environmental variable management

### Sub-Agent Delegation
- Create child agents for specific tasks
- Isolated execution contexts per sub-agent
- Parent-child communication protocol
- Result aggregation from sub-agents

### Middleware Pattern
- Cross-cutting concerns implementation
- Composable functionality stack
- Tool enhancement and monitoring
- State transformation and validation

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Core Framework** | LangChain |
| **LLM** | Claude Sonnet 4.5 (default, customizable) |
| **Language** | Python 3.10+ |
| **CLI** | Typer, Rich |
| **Web UI** | Chainlit (optional) |
| **API** | FastAPI, Uvicorn |
| **Task Management** | Custom state machine |
| **Observability** | LangChain callbacks |
| **Testing** | pytest |

## High-Level Architecture

```
┌──────────────────────────────────────────────────────┐
│              User / External System                  │
│         (Task Request)                               │
└────────────────────────┬─────────────────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │   Deepagents Engine              │
        ├─────────────────────────────────┤
        │                                  │
        │  ┌───────────────────────────┐   │
        │  │  Planning Phase            │   │
        │  │  - Task analysis           │   │
        │  │  - Subtask generation      │   │
        │  │  - Dependency mapping      │   │
        │  │  - Tool selection          │   │
        │  └───────────────────────────┘   │
        │           │                      │
        │  ┌────────▼───────────────────┐   │
        │  │  Middleware Stack          │   │
        │  ├────────────────────────────┤   │
        │  │  1. FilesystemMiddleware   │   │
        │  │  2. SubAgentMiddleware     │   │
        │  │  3. PatchToolCallsMiddleware   │
        │  │  4. TodoListMiddleware     │   │
        │  │  5. SummarizationMiddleware│   │
        │  │  6. HumanInTheLoopMiddleware   │
        │  │  7. AnthropicPromptCaching │   │
        │  └────────────────────────────┘   │
        │           │                      │
        │  ┌────────▼───────────────────┐   │
        │  │  Tool Execution Phase      │   │
        │  │  - Execute planned tasks   │   │
        │  │  - Monitor sub-agents      │   │
        │  │  - Handle errors           │   │
        │  │  - Gather results          │   │
        │  └───────────────────────────┘   │
        │           │                      │
        │  ┌────────▼───────────────────┐   │
        │  │  Result Processing         │   │
        │  │  - Aggregate outputs       │   │
        │  │  - Generate summary        │   │
        │  │  - Plan adjustments        │   │
        │  └───────────────────────────┘   │
        └────────────────┬──────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼──────┐  ┌────▼──────┐  ┌───▼────────┐
    │ Filesystem│  │ Sub-Agents│  │ Shell Exec │
    │Operations │  │           │  │            │
    └───────────┘  └───────────┘  └────────────┘
```

## Design Patterns

### 1. **Middleware Architecture**
- Stack-based composition
- Each middleware handles specific concern
- Middleware can transform tools/results
- Pluggable and testable

### 2. **Planning-First Execution**
- Explicit planning phase
- Task decomposition
- Tool selection reasoning
- Error anticipation

### 3. **Sub-Agent Delegation**
- Hierarchical task decomposition
- Isolated execution contexts
- Independent agent loops
- Result aggregation

### 4. **Tool Extension**
- Custom tool implementation
- Tool registration system
- Parameter validation
- Result handling

### 5. **State Management**
- Long-lived agent state
- Persistent todo lists
- Execution history tracking
- Resumable workflows

## Built-in Tools

### Filesystem Tools
- `ls` - List directory contents
- `read_file` - Read file content
- `write_file` - Create/overwrite files
- `edit_file` - Modify file content
- `glob` - Pattern-based file search

### Text Processing
- `grep` - Search text in files

### Task Management
- `write_todos` - Create/update todo list
- `task_delegation` - Delegate to sub-agent

### Shell Execution
- `execute` - Run arbitrary shell commands
- Environment variable support
- Output streaming
- Error handling

## Middleware Stack

| Middleware | Purpose |
|-----------|---------|
| **FilesystemMiddleware** | File operation logging, sandboxing |
| **SubAgentMiddleware** | Sub-agent creation and coordination |
| **PatchToolCallsMiddleware** | Modify tool calls before execution |
| **TodoListMiddleware** | Manage task lists and progress |
| **SummarizationMiddleware** | Compress long contexts |
| **HumanInTheLoopMiddleware** | Pause for human approval |
| **AnthropicPromptCachingMiddleware** | Optimize token usage |

## File Structure

```
deepagents/
├── libs/
│   ├── deepagents/
│   │   ├── agent.py                # Core agent class
│   │   ├── tools/
│   │   │   ├── filesystem.py
│   │   │   ├── shell.py
│   │   │   └── task_delegation.py
│   │   ├── middleware/
│   │   │   ├── base.py
│   │   │   ├── filesystem.py
│   │   │   ├── sub_agent.py
│   │   │   ├── todo_list.py
│   │   │   ├── summarization.py
│   │   │   ├── human_in_loop.py
│   │   │   └── prompt_caching.py
│   │   └── models.py               # Data models
│   │
│   ├── deepagents-cli/
│   │   ├── cli.py                  # CLI interface
│   │   ├── commands/
│   │   └── formatters/
│   │
│   └── harbor/
│       ├── api.py                  # FastAPI server
│       ├── models.py
│       └── database.py
│
└── README.md
```

## Configuration

### Agent Configuration
```python
from deepagents import Agent

agent = Agent(
    name="researcher",
    model="claude-sonnet-4-5",
    tools=["filesystem", "shell", "web_search"],
    middleware_stack=[
        FilesystemMiddleware(),
        HumanInTheLoopMiddleware(),
        SummarizationMiddleware(),
    ]
)
```

### LLM Configuration
- Model: Claude Sonnet 4.5 (default)
- Temperature: 0.7 (default)
- Max tokens: 4096 (default)
- Context window: 200K

## Integration Points

1. **LangChain**: Core agent framework
2. **Claude API**: LLM backend
3. **Filesystem**: Direct file access (with sandboxing)
4. **Shell**: Command execution (with validation)
5. **External Tools**: Via tool registration
6. **Sub-Agents**: Via delegation middleware
7. **Monitoring**: Via callbacks and logging

## Main Features

1. **Planning**: Explicit task planning before execution
2. **Long-Horizon Execution**: Support for multi-hour/day tasks
3. **Computer Access**: Full filesystem and shell capabilities
4. **Sub-Agent Delegation**: Hierarchical task decomposition
5. **Middleware Stack**: Extensible cross-cutting concerns
6. **Human-in-the-Loop**: Pause points for human oversight
7. **Error Recovery**: Graceful handling and resumption
8. **Observability**: Comprehensive logging and tracing
9. **Prompt Caching**: Token optimization for long contexts
10. **Sandboxing**: Controlled filesystem access

## Use Cases

- Research and data analysis automation
- Code generation and debugging
- File system operations at scale
- Complex multi-step workflows
- Supervised autonomous execution
- Experimentation and exploration
- Batch processing with oversight

## Execution Flow

1. **Task Reception**: Agent receives user task
2. **Planning Phase**: Agent plans workflow with reasoning
3. **Middleware Application**: Each middleware processes plan
4. **Tool Execution**: Execute planned operations
5. **Sub-Agent Delegation**: For complex sub-tasks
6. **Result Aggregation**: Collect all outputs
7. **Summary Generation**: Create concise results
8. **Human Review**: If HITL middleware enabled
9. **Persistence**: Save state and history

## Performance Considerations

- Batch operations for efficiency
- Caching for frequently accessed data
- Prompt caching for long contexts
- Parallel sub-agent execution
- Result streaming for large outputs
- Memory management for long-running tasks

## Security Considerations

- Filesystem sandboxing
- Shell command validation
- API key management
- Sub-agent isolation
- Input validation
- Output sanitization

## Best Practices

1. Define clear task objectives
2. Use sub-agents for parallelizable work
3. Implement HITL for critical decisions
4. Monitor long-running executions
5. Handle errors gracefully
6. Document tool behavior
7. Test middleware interactions
8. Use appropriate logging levels

## Extensibility

- Custom middleware implementation
- Custom tool registration
- Custom result processors
- LLM provider switching
- Callback hooks for monitoring
- Custom state serialization
