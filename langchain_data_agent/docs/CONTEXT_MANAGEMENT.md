# Context Management in Data Agent

This document explains how context is managed throughout the Data Agent system, covering conversation history, database schema context, and state persistence.

## Overview

The system manages **three types of context**:

1. **Conversation Context** - Message history for multi-turn conversations
2. **Database Schema Context** - Table/column metadata for SQL generation
3. **State Context** - Intermediate processing state in LangGraph

## 1. Conversation Context Management

### Message History

The system maintains conversation history using LangGraph's `add_messages` reducer.

**Key Components:**

```python
# State definition (models/state.py)
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]  # Auto-accumulates messages
    question: str
    # ... other fields
```

The `add_messages` annotation automatically appends new messages to the existing list, preserving conversation history across graph nodes.

### Recent History Window

To avoid token limits and maintain relevance, the system uses a sliding window of recent messages:

```python
# utils/message_utils.py
def get_recent_history(
    messages: list[AnyMessage] | None,
    max_messages: int = 6,
) -> Sequence[AnyMessage]:
    """Get last N messages, excluding system messages.
    
    Default: 6 messages = ~3 conversation turns (user + assistant)
    """
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]
    return non_system[-max_messages:]
```

### Usage in Nodes

Each node that needs conversation context calls `get_recent_history()`:

```python
# nodes/data_nodes.py - SQL Generation Node
def generate_sql(state: AgentState) -> dict:
    # Get recent history (6 messages = ~3 turns)
    history = get_recent_history(state.get("messages", []), max_messages=6)
    
    messages = [
        SystemMessage(content=system_prompt),
        *history,  # Include recent conversation
        HumanMessage(content=question),
    ]
    
    response = llm.invoke(messages)
    # ...
```

**Different limits for different nodes:**
- **SQL Generation**: `max_messages=6` (needs more context)
- **Intent Detection**: `max_messages=4` (simpler routing decision)
- **Response Generation**: `max_messages=4` (focus on recent results)

### Multi-Turn Conversations

The system supports follow-up questions naturally:

```
User: "How many active employees?"
Assistant: [executes query] "There are 1,552 active employees."

User: "What about managers?"  # Context aware!
Assistant: [uses conversation history to understand reference] 
          "There are 127 active managers."
```

## 2. Database Schema Context

### Static Schema (Configured)

Define schema explicitly in YAML for controlled, consistent prompts:

```yaml
data_agents:
  - name: skills
    table_schemas:
      - name: "[dbo].[vw_CG_SkillData]"
        description: "Employee skills and proficiencies"
        columns:
          - name: "userId"
            type: "varchar"
            description: "Employee ID"
          - name: "skill"
            type: "varchar"
            description: "Skill name"
          # ... more columns
```

**Formatted into prompt:**

```python
# nodes/data_nodes.py
def _get_schema_context(self) -> str:
    if self._config.table_schemas:
        return SchemaFormatter.format_schema_context(self._config)
```

### Dynamic Schema (Auto-discovered)

If no `table_schemas` defined, fetch schema dynamically from database:

```python
def _get_schema_context(self) -> str:
    if not self._config.table_schemas:
        if isinstance(self._datasource, SQLDatabase):
            table_info = self._datasource.get_table_info()
            return f"Available tables and schemas:\n\n{table_info}"
    return ""
```

### Schema in System Prompts

Schema context is injected into every SQL generation prompt:

```yaml
system_prompt: |
  You are an SQL assistant.
  
  ## Database Context
  
  {schema_context}  # Injected here!
  
  ## T-SQL Generation Guidelines
  1. Use only tables and columns defined above
  2. Always qualify column names
  # ...
```

**Why rebuild system messages?**

System messages are NOT stored in history - they're rebuilt each time to:
- Include fresh schema context
- Support schema changes without restarting
- Keep token count manageable

```python
# System messages are filtered out from history
non_system = [m for m in messages if not isinstance(m, SystemMessage)]
```

## 3. State Persistence with Checkpointers

### Thread-Based Persistence

LangGraph uses **checkpointers** to persist conversation state across multiple runs:

```python
# agent.py
checkpointer = InMemorySaver()  # Default: in-memory storage

workflow.compile(
    checkpointer=checkpointer,
    name="data_agent_flow"
)
```

### Thread IDs

Each conversation gets a unique `thread_id` for state isolation:

```python
# Chainlit UI (ui/app.py)
thread_id = cl.context.session.id  # Unique per chat session

result = await flow.run(message.content, thread_id=thread_id)
```

**Without thread_id:**
```python
# CLI mode - new UUID per run (no persistence)
if thread_id is None:
    thread_id = uuid4().hex
```

### Checkpointer Types

**InMemorySaver** (default):
- Stores state in RAM
- Lost on restart
- Good for: Development, single-session apps

**Persistent Checkpointers** (optional):
- PostgresCheckpointer
- RedisCheckpointer  
- Custom implementations

```python
from langgraph.checkpoint.postgres import PostgresCheckpointer

checkpointer = PostgresCheckpointer(connection_string="postgresql://...")

workflow.compile(checkpointer=checkpointer)
```

### State Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│  User Query 1: "How many employees?"                    │
│  thread_id: "abc123"                                    │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
    ┌────────────────────────┐
    │  Intent Detection      │ ──► messages: [user, ai]
    │  SQL Generation        │ ──► generated_sql: "SELECT..."
    │  Execute Query         │ ──► result: QueryResult(...)
    │  Generate Response     │ ──► final_response: "1,552 employees"
    └───────────┬────────────┘
                │
                ▼ State saved to checkpointer
    ┌────────────────────────────────────┐
    │  Checkpoint: thread_id="abc123"    │
    │  - messages: [...]                 │
    │  - datasource_name: "datahub"      │
    │  - generated_sql: "..."            │
    └───────────┬────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  User Query 2: "What about managers?"                   │
│  thread_id: "abc123"  (SAME thread!)                    │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼ Load previous state
    ┌────────────────────────────┐
    │  Intent Detection          │ ──► Has access to previous messages!
    │  - Sees: "How many employees?" + "What about managers?"
    │  - Understands context!
    └────────────────────────────┘
```

## 4. Agent State Flow

### State Structure

```python
class AgentState(TypedDict):
    # Input
    question: str
    datasource_name: str
    
    # Context
    messages: Annotated[list[AnyMessage], add_messages]
    schema_context: str
    dialect: str
    
    # Processing
    generated_sql: str
    validation_result: SQLValidationOutput
    retry_count: int
    
    # Output
    result: QueryResult
    final_response: str
    error: str | None
    
    # Visualization
    visualization_requested: bool
    visualization_image: str | None
    visualization_code: str | None
```

### State Updates in Nodes

Each node returns a partial state dict - LangGraph merges it:

```python
def generate_sql(state: AgentState) -> dict:
    # Node only returns fields it updates
    return {
        "generated_sql": sql_query,
        "messages": [AIMessage(content=sql_query, name="sql_generator")],
        # Other fields preserved automatically!
    }
```

### State Transformations

```
START
  ↓ question="How many employees?"
  ↓ datasource_name=""
  ↓ messages=[]
  
Intent Detection
  ↓ datasource_name="datahub"  ← Updated
  ↓ messages=[HumanMessage(...), AIMessage("Detected: datahub")]  ← Added
  
SQL Generation  
  ↓ generated_sql="SELECT COUNT(*) FROM..."  ← Added
  ↓ schema_context="vw_Amigo_Caregiver columns: ..."  ← Added
  ↓ messages=[..., AIMessage("Generated SQL")]  ← Appended
  
Execute Query
  ↓ result=QueryResult(rows=[[1552]], ...)  ← Added
  ↓ messages=[..., AIMessage("Query executed")]  ← Appended
  
Generate Response
  ↓ final_response="There are 1,552 active..."  ← Added
  ↓ messages=[..., AIMessage("Response")]  ← Appended

END → Return OutputState
```

## 5. Context Management Best Practices

### ✅ DO

1. **Use thread_ids for multi-turn conversations**
   ```python
   # Chainlit - persist per session
   thread_id = cl.context.session.id
   result = await flow.run(question, thread_id=thread_id)
   ```

2. **Limit history window appropriately**
   ```python
   # Short-term memory for SQL generation
   history = get_recent_history(messages, max_messages=6)
   ```

3. **Rebuild system prompts with fresh schema**
   ```python
   # Don't cache system messages - rebuild each time
   schema_context = self._get_schema_context()
   system_prompt = prompt_template.format(schema_context=schema_context)
   ```

4. **Use persistent checkpointers in production**
   ```python
   from langgraph.checkpoint.postgres import PostgresCheckpointer
   checkpointer = PostgresCheckpointer(conn_string)
   ```

### ❌ DON'T

1. **Don't include system messages in history**
   ```python
   # System messages change frequently (schema updates)
   non_system = [m for m in messages if not isinstance(m, SystemMessage)]
   ```

2. **Don't pass unlimited history to LLM**
   ```python
   # This will hit token limits!
   messages = [SystemMessage(...), *state["messages"]]  # BAD
   
   # Do this instead:
   history = get_recent_history(state["messages"], max_messages=6)
   messages = [SystemMessage(...), *history]  # GOOD
   ```

3. **Don't share thread_ids across users**
   ```python
   # Each user needs their own thread
   thread_id = f"user_{user_id}_{session_id}"
   ```

## 6. Context in Multi-Agent Routing

### Intent Detection Context

Intent detector sees previous conversation to make routing decisions:

```python
def intent_detection_node(state: AgentState):
    question = state["question"]
    
    # Include recent history for context-aware routing
    history = get_recent_history(state.get("messages", []), max_messages=4)
    
    messages = [
        SystemMessage(content=intent_prompt),
        *history,  # Previous Q&A helps routing!
        HumanMessage(content=question),
    ]
    
    # Route based on question + context
    selected_agent = intent_llm.invoke(messages).content
```

**Example:**
```
Thread 1:
  User: "How many employees?" → Routes to datahub
  User: "What about their skills?" → Routes to skills (context aware!)

Thread 2:
  User: "Show me Python experts" → Routes to skills
  User: "What's their average tenure?" → Could route back to datahub!
```

### Cross-Agent Context Sharing

Currently, each agent sees the full conversation history but not other agents' internal state.

```
┌──────────────────────────────────────────┐
│         Shared Context (All Agents)      │
│  - messages: [user, ai, user, ai, ...]   │
│  - question: "current question"          │
└──────────────────────────────────────────┘
         ↓                    ↓
   ┌──────────┐        ┌──────────┐
   │ DataHub  │        │  Skills  │
   │ Agent    │        │  Agent   │
   │          │        │          │
   │ Private: │        │ Private: │
   │ - sql    │        │ - sql    │
   │ - result │        │ - result │
   └──────────┘        └──────────┘
```

## 7. Debugging Context

### View Message History (CLI)

```bash
# Use -v to see full message history
data-agent query -c employee_analytics "Your question" -v
```

Shows:
- All messages in conversation
- Intent detection decisions
- SQL generated at each step
- Validation results
- Query execution output

### Access State Programmatically

```python
async with DataAgentFlow(config_path="config.yaml") as flow:
    result = await flow.run("Your question", thread_id="debug_thread")
    
    # Access full state
    print("Messages:", result.get("messages"))
    print("SQL:", result.get("generated_sql"))
    print("Schema context:", result.get("schema_context"))
```

## 8. Configuration Examples

### Example 1: Limit Context Window

```python
# Reduce history for faster responses
history = get_recent_history(messages, max_messages=2)  # Only last turn
```

### Example 2: Custom Checkpointer

```python
from langgraph.checkpoint.memory import MemorySaver

# Clear history after each session
checkpointer = MemorySaver()  # Separate from InMemorySaver

flow = DataAgentFlow(config, checkpointer=checkpointer)
```

### Example 3: Thread Management

```python
# CLI - new thread per query (no persistence)
result = await flow.run("Question 1")  # thread_id=uuid()
result = await flow.run("Question 2")  # thread_id=uuid() (different!)

# Chainlit - persistent thread per session
thread_id = session.id
result1 = await flow.run("Question 1", thread_id=thread_id)
result2 = await flow.run("Question 2", thread_id=thread_id)  # Same thread!
```

## Summary

| Context Type | Storage | Scope | Persistence |
|-------------|---------|-------|-------------|
| **Message History** | LangGraph state | Per thread | Checkpointer-dependent |
| **Schema Context** | Rebuilt each call | Per node execution | Not persisted |
| **Agent State** | LangGraph state | Per graph run | Checkpointer-dependent |
| **Thread State** | Checkpointer | Per thread_id | Until cleared |

The system balances **context richness** (for accurate responses) with **token efficiency** (to avoid limits) using sliding windows, thread isolation, and dynamic schema loading.
