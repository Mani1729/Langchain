# 🎯 Quick Reference Guide - Azure OpenAI with LangChain

## Your Azure OpenAI Configuration

```python
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o",
    model="gpt-4o",
    temperature=0.7
)
```

## Quick Commands

```powershell
# Test connection
python 00_test_connection.py

# Run tutorials in order
python 01_basics_and_setup.py      # Basics
python 02_prompting_concepts.py    # Prompting
python 03_lcel.py                  # LCEL
python 04_tools.py                 # Tools
python 05_memory.py                # Memory
python 06_chain_building.py        # Chains
python 07_agents.py                # Agents
python 08_multi_agent.py           # Multi-Agent
python 09_langsmith.py             # Monitoring
```

## Common Patterns

### Simple LLM Call
```python
response = llm.invoke("Your question here")
print(response.content)
```

### With Prompt Template
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Explain {topic} in simple terms")
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "AI"})
```

### With Memory
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
# Use with chains or agents
```

### With Tools
```python
from langchain.agents import tool

@tool
def my_tool(input: str) -> str:
    """Tool description"""
    return f"Processed: {input}"
```

### Creating Agent
```python
from langchain.agents import create_openai_functions_agent, AgentExecutor

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "Your query"})
```

## File Overview

| File | Topic | Key Concepts |
|------|-------|--------------|
| 00 | Test Connection | Verify setup |
| 01 | Basics | LLM calls, streaming, caching |
| 02 | Prompting | Templates, few-shot, examples |
| 03 | LCEL | Chains, pipes, runnables |
| 04 | Tools | Custom tools, function calling |
| 05 | Memory | Conversation history |
| 06 | Chains | Sequential, parallel, routing |
| 07 | Agents | ReAct, tool selection |
| 08 | Multi-Agent | Collaboration, orchestration |
| 09 | LangSmith | Monitoring, debugging |

## Learning Checklist

- [ ] Test connection (00)
- [ ] Complete basics (01)
- [ ] Learn prompting (02)
- [ ] Master LCEL (03)
- [ ] Create tools (04)
- [ ] Add memory (05)
- [ ] Build chains (06)
- [ ] Create agent (07)
- [ ] Multi-agent system (08)
- [ ] Setup monitoring (09)
- [ ] Build a project
- [ ] Do practice exercises

## Your Advantages

✅ **GPT-4o Model**: Most capable OpenAI model
✅ **Azure OpenAI**: Enterprise-grade reliability
✅ **Pre-configured**: No setup required
✅ **Complete Examples**: 100+ working code examples
✅ **Practice Exercises**: 10 exercises + 5 projects

## Need Help?

1. Check `AZURE_SETUP.md` for detailed info
2. Read `README.md` for complete guide
3. Run `00_test_connection.py` to verify setup
4. Each tutorial file has detailed comments

## Next Steps

1. ✅ Run: `python 00_test_connection.py`
2. ✅ Start: `python 01_basics_and_setup.py`
3. ✅ Continue through all 9 tutorials
4. ✅ Complete practice exercises
5. ✅ Build a real project!

---

**You're all set to master LangChain!** 🚀
