# Multi-Agent Communication

This guide explains how to connect multiple data agents to communicate with each other in the langchain_data_agent system.

## Overview

The platform supports multiple approaches for agent-to-agent communication:

1. **Single Configuration with Multiple Agents** (Recommended)
2. **Load All Configurations** (Auto-discovery)
3. **A2A Protocol** (Inter-process communication)

## Approach 1: Combined Configuration File

Create a single YAML file with multiple data agents that share the same intent detection logic.

### Example: Employee Analytics (DataHub + Skills)

See `src/data_agent/config/employee_analytics.yaml` for a complete example.

```yaml
intent_detection_agent:
  llm:
    model: gpt-4o
    provider: azure_openai
  system_prompt: |
    Route to 'datahub' for: employee demographics, tenure, managers, departments
    Route to 'skills' for: skills, capabilities, proficiencies, tools, expertise
    Route to 'skills' if question asks about BOTH employee data AND skills

data_agents:
  - name: datahub
    datasource:
      type: azure_sql
      # ... datahub configuration
    description: Query employee demographics, tenure, managers, departments

  - name: skills
    datasource:
      type: azure_sql
      # ... skills configuration
    description: Query employee skills, capabilities, proficiencies
```

### Usage

```bash
# CLI
data-agent query -c employee_analytics "How many employees have Python skills?"
data-agent query -c employee_analytics "How many active employees are there?"
data-agent chat -c employee_analytics

# Chainlit UI - Select "Employee Analytics" profile
chainlit run src/data_agent/ui/app.py
```

### How It Works

1. User asks a question
2. **Intent Detection Agent** analyzes the question and routes to the appropriate data agent
3. Selected agent generates SQL, executes query, and returns results
4. System maintains conversation context for follow-up questions

### Example Routing

| Question | Routes To |
|----------|-----------|
| "How many active employees?" | `datahub` |
| "What are the top Python skills?" | `skills` |
| "Show me managers with advanced Python skills" | `skills` (has both data) |
| "What's the average tenure by pillar?" | `datahub` |

## Approach 2: Load All Configurations

Use the system's ability to load and merge all YAML files automatically.

```bash
# Load all configs - no -c flag
data-agent query "How many employees have Python skills?"
data-agent chat

# Or explicitly use "all"
data-agent query -c all "What are the top skills?"
```

The system combines all `data_agents` from every YAML file in `src/data_agent/config/`.

### Chainlit UI

Select **"All Agents"** profile to enable automatic routing across all configured agents.

## Approach 3: A2A Protocol (Agent-to-Agent)

For inter-process communication between separate agent instances.

### Start A2A Servers

```bash
# Terminal 1: Skills agent
data-agent a2a -c skills --port 8001

# Terminal 2: DataHub agent  
data-agent a2a -c datahub --port 8002
```

### Python Client Example

```python
import asyncio
import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart
from uuid import uuid4

async def query_multiple_agents():
    async with httpx.AsyncClient(timeout=120.0) as http:
        # Query skills agent
        resolver = A2ACardResolver(httpx_client=http, base_url="http://localhost:8001")
        card = await resolver.get_agent_card()
        client = ClientFactory(ClientConfig(httpx_client=http)).create(card=card)
        
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text="How many employees have Python?"))],
            message_id=uuid4().hex,
        )
        
        async for event in client.send_message(message):
            # Process response
            pass

asyncio.run(query_multiple_agents())
```

## Configuration Tips

### Intent Detection Routing

Make routing rules specific in your intent detection prompt:

```yaml
intent_detection_agent:
  system_prompt: |
    ## Routing Rules
    
    Route to 'datahub' for:
    - Employee counts, demographics
    - Hire dates, tenure calculations
    - Organizational hierarchy
    - Manager/employee relationships
    
    Route to 'skills' for:
    - Skill proficiencies
    - Technology/tool expertise
    - Capability assessments
    - Domain knowledge
    
    If question combines both contexts, prefer 'skills' 
    (it contains employee data + skills)
```

### Avoiding Ambiguity

1. **Name agents descriptively**: `datahub`, `skills`, not `agent1`, `agent2`
2. **Write clear descriptions**: Used by intent detection to route queries
3. **Test edge cases**: Questions that could match multiple agents
4. **Overlap is OK**: Skills view includes employee data, reducing need for joins

## Benefits of Combined Configuration

✅ **Automatic routing** - No manual agent selection needed  
✅ **Single configuration** - Easier to maintain  
✅ **Shared credentials** - Same database, different views  
✅ **Context preservation** - Follow-up questions work naturally  
✅ **Unified UI** - Single Chainlit profile for related data  

## Testing

```bash
# Test intent detection
data-agent query -c employee_analytics "How many active employees?" -v
# Should route to: datahub

data-agent query -c employee_analytics "Who has Python skills?" -v
# Should route to: skills

data-agent query -c employee_analytics "Show managers with cloud skills" -v
# Should route to: skills (has both employee + skill data)
```

## Example Queries

### Employee Analytics Combined Config

```bash
# Demographics (routes to datahub)
data-agent query -c employee_analytics "How many employees per department?"
data-agent query -c employee_analytics "What's the average PGC tenure?"

# Skills (routes to skills)
data-agent query -c employee_analytics "Top 10 most common skills"
data-agent query -c employee_analytics "Show Python proficiency distribution"

# Combined (routes to skills - has both)
data-agent query -c employee_analytics "Managers with advanced Azure skills"
data-agent query -c employee_analytics "Python experts in Cybersecurity pillar"
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│          User Question                          │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│      Intent Detection Agent                     │
│      (Analyzes question intent)                 │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌───────────────┐
│ DataHub Agent │    │ Skills Agent  │
│ (Employee     │    │ (Skills +     │
│  demographics)│    │  Employee)    │
└───────┬───────┘    └───────┬───────┘
        │                    │
        ▼                    ▼
┌───────────────────────────────────┐
│   vw_Amigo_Caregiver              │
│   vw_CG_SkillData                 │
│   (Azure SQL Database)            │
└───────────────────────────────────┘
```

## See Also

- [A2A Protocol Documentation](A2A.md)
- [Configuration Guide](CONFIGURATION.md)
- [Database Setup](DATABASE_SETUP.md)
