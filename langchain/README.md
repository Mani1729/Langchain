# 🦜🔗 Complete LangChain Learning Guide

Welcome to your comprehensive LangChain learning journey! This repository contains everything you need to master LangChain and build production-ready LLM applications.

## 📚 Learning Path

Follow these files in order for the best learning experience:

### 1️⃣ **Basics and Setup** (`01_basics_and_setup.py`)
**Start here!** Learn the fundamentals:
- Installation and configuration
- Basic LLM calls with different providers
- Message types and streaming
- Output parsers
- Callbacks and monitoring
- Token usage tracking
- Caching strategies

**Key Concepts**: LLM wrappers, temperature, streaming, batch processing

### 2️⃣ **Prompting Concepts** (`02_prompting_concepts.py`)
Master the art of prompt engineering:
- Prompt templates
- Chat prompt templates
- Few-shot prompting
- Example selectors
- Partial variables
- Messages placeholder
- Structured output prompting
- Chain-of-thought

**Key Concepts**: PromptTemplate, few-shot learning, role-based prompting

### 3️⃣ **LCEL - LangChain Expression Language** (`03_lcel.py`)
Learn modern chain composition:
- Basic LCEL chains (pipe operator)
- Multi-step chains
- RunnablePassthrough
- RunnableParallel
- RunnableLambda
- RunnableBranch
- Streaming and batch processing
- Fallbacks and retry
- Async support

**Key Concepts**: Runnables, pipe operator (|), parallel execution

### 4️⃣ **Tools** (`04_tools.py`)
Extend LLM capabilities:
- Creating custom tools
- @tool decorator
- StructuredTool
- Built-in tools (search, Wikipedia)
- Tool calling with bind_tools
- API integration
- File operations
- Error handling

**Key Concepts**: Tool definitions, bind_tools, tool descriptions

### 5️⃣ **Memory** (`05_memory.py`)
Add conversation memory:
- ConversationBufferMemory
- ConversationBufferWindowMemory
- ConversationSummaryMemory
- ConversationSummaryBufferMemory
- ConversationEntityMemory
- Memory with LCEL
- Multi-session management
- Persistent memory

**Key Concepts**: Stateful conversations, session management, memory types

### 6️⃣ **Chain Building** (`06_chain_building.py`)
Build complex workflows:
- Sequential chains
- Parallel execution
- Router chains
- Map-reduce patterns
- Transform chains
- RAG chains
- Multi-step reasoning
- Error handling
- Production patterns

**Key Concepts**: Chain composition, routing, RAG, error resilience

### 7️⃣ **Agents** (`07_agents.py`)
Create autonomous agents:
- ReAct agents
- OpenAI Functions agents
- AgentExecutor
- Tools with agents
- Agent with memory
- Error handling
- Dynamic tool selection
- Custom agents

**Key Concepts**: ReAct pattern, agent reasoning, tool calling

### 8️⃣ **Multi-Agent Systems** (`08_multi_agent.py`)
Coordinate multiple agents:
- Sequential multi-agent
- Parallel agents
- Hierarchical (manager-worker)
- Debate systems
- Agent communication
- Task routing
- Collaborative problem solving
- Coordination patterns

**Key Concepts**: Agent specialization, collaboration, orchestration

### 9️⃣ **LangSmith** (`09_langsmith.py`)
Monitor and improve your apps:
- LangChain vs LangSmith
- Setting up tracing
- Debugging chains and agents
- Creating test datasets
- Evaluation functions
- Production monitoring
- A/B testing
- Best practices

**Key Concepts**: Tracing, evaluation, monitoring, debugging

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install langchain langchain-openai langchain-community
pip install python-dotenv requests
pip install langsmith  # For monitoring (optional)
pip install duckduckgo-search wikipedia  # For built-in tools (optional)
```

Or simply:
```bash
pip install -r requirements.txt
```

### ✅ Ready to Run!

**All tutorial files are pre-configured with your Azure OpenAI credentials**, so you can start learning immediately without any setup!

**Optional**: Create a `.env` file if you want to override settings:

```env
# Azure OpenAI (already configured in code)
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Optional: LangSmith for monitoring
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=langchain-learning
```

### Run the Examples

All files are configured with your Azure OpenAI (gpt-4o), so just run them:

```powershell
# Start with basics
python 01_basics_and_setup.py

# Continue through the sequence
python 02_prompting_concepts.py
python 03_lcel.py
python 04_tools.py
python 05_memory.py
python 06_chain_building.py
python 07_agents.py
python 08_multi_agent.py
python 09_langsmith.py
```

---

## 🎯 Practice Exercises

After completing the tutorials, test your knowledge:

### Beginner Level

1. **Simple Chatbot**
   - Build a chatbot with conversation memory
   - Use ConversationBufferMemory
   - Allow at least 5 turns of conversation

2. **Calculator Tool**
   - Create a custom calculator tool
   - Build an agent that uses it
   - Handle division by zero errors

3. **Prompt Testing**
   - Create 3 different prompt templates
   - Test with the same input
   - Compare outputs

### Intermediate Level

4. **RAG System**
   - Create a simple retrieval function
   - Build a RAG chain using LCEL
   - Ask questions and get context-aware answers

5. **Multi-Tool Agent**
   - Create 3+ custom tools (weather, calculator, search)
   - Build an agent that selects appropriate tools
   - Test with complex queries requiring multiple tools

6. **Sequential Pipeline**
   - Build a content pipeline: Writer → Editor → Fact-Checker
   - Use LCEL to chain them
   - Process a news article topic

### Advanced Level

7. **Multi-Agent Debate**
   - Create 2 agents with opposing views
   - Add a moderator agent
   - Simulate a 3-round debate on a topic

8. **Production-Ready Chatbot**
   - Implement conversation memory
   - Add error handling and fallbacks
   - Use streaming responses
   - Integrate LangSmith monitoring
   - Add user feedback collection

9. **Research Assistant**
   - Create a hierarchical multi-agent system
   - Manager agent coordinates 3 specialists
   - Specialists: Researcher, Analyst, Writer
   - Produce a comprehensive report

10. **Custom Agent Framework**
    - Build a custom agent from scratch
    - Implement your own tool calling logic
    - Add memory and error handling
    - Create at least 2 tools

---

## 🧪 Project Ideas

Build complete applications to solidify your knowledge:

### 1. **Document Q&A System**
- Upload documents
- Create vector embeddings
- RAG-based question answering
- Chat interface with memory

**Concepts Used**: RAG, memory, chains, tools

### 2. **Code Review Agent**
- Accept code snippets
- Agent analyzes for bugs, style, performance
- Multiple specialized agents (security, performance, style)
- Generate detailed review report

**Concepts Used**: Multi-agent, tools, prompting

### 3. **Customer Support Automation**
- Route queries to specialist agents
- Knowledge base search
- Escalation logic
- Conversation memory
- Sentiment analysis

**Concepts Used**: Agents, routing, memory, tools

### 4. **Content Creation Pipeline**
- Topic generation
- Research phase (multi-agent)
- Writing phase
- Editing phase
- SEO optimization
- Fact-checking

**Concepts Used**: Multi-agent, chains, sequential processing

### 5. **Personal AI Assistant**
- Task management
- Email drafting
- Calendar integration
- Web search
- File operations
- Multi-session memory

**Concepts Used**: Tools, agents, memory, LCEL

---

## 📖 Key Concepts Summary

### LangChain Hierarchy

```
Application
    ├── Agents (autonomous decision-making)
    │   ├── Tools (extend capabilities)
    │   ├── Memory (conversation history)
    │   └── LLM (decision engine)
    │
    ├── Chains (predefined workflows)
    │   ├── Prompts (instructions)
    │   ├── LLM (processing)
    │   ├── Parsers (output formatting)
    │   └── Memory (optional)
    │
    └── Components
        ├── LLM Wrappers
        ├── Prompt Templates
        ├── Output Parsers
        ├── Memory Systems
        └── Tools
```

### When to Use What

| Use Case | Solution | Files |
|----------|----------|-------|
| Simple LLM call | Basic chain | 01, 02, 03 |
| Predefined workflow | LCEL chain | 03, 06 |
| Dynamic decisions | Agent | 07 |
| Multiple tools needed | Agent with tools | 04, 07 |
| Need conversation history | Add memory | 05 |
| Complex multi-step | Chain building | 06 |
| Different expertise needed | Multi-agent | 08 |
| Monitor/debug | LangSmith | 09 |

### Decision Tree

```
Start
  │
  ├─ Need dynamic tool selection? ──Yes──> Use Agent (07)
  │                                   │
  │                                   └─ Multiple specialized roles? ──Yes──> Multi-Agent (08)
  │
  ├─ Fixed workflow? ──Yes──> Use Chain (03, 06)
  │                     │
  │                     └─ Need conversation history? ──Yes──> Add Memory (05)
  │
  ├─ External capabilities? ──Yes──> Create Tools (04)
  │
  └─ Need monitoring? ──Yes──> Setup LangSmith (09)
```

---

## 🎓 Interview Preparation

### Common Questions & Answers

**Q: What is LangChain?**
A: LangChain is a framework for building LLM-powered applications. It provides abstractions for prompts, chains, agents, memory, and tools, making it easier to create complex AI applications.

**Q: What's the difference between a chain and an agent?**
A: Chains execute predefined sequences of operations. Agents use LLMs to dynamically decide which actions to take and which tools to use based on the input.

**Q: Explain the ReAct pattern.**
A: ReAct (Reasoning + Acting) is a pattern where the agent alternates between Thought (reasoning), Action (tool selection), Action Input (parameters), and Observation (tool result) until it reaches a Final Answer.

**Q: What is LCEL?**
A: LangChain Expression Language is a declarative way to compose chains using the pipe operator (|). It provides automatic streaming, async support, and built-in error handling.

**Q: When would you use memory?**
A: Use memory when you need stateful conversations where the LLM should remember previous interactions, like chatbots, customer support, or any multi-turn dialogue.

**Q: How do you choose between different memory types?**
A: 
- ConversationBufferMemory: Short conversations, need full history
- ConversationBufferWindowMemory: Long conversations, only need recent context
- ConversationSummaryMemory: Very long conversations, summarize old messages
- ConversationEntityMemory: Need to track specific entities across conversation

**Q: What makes a good tool description?**
A: A good tool description clearly states what the tool does, when to use it, what inputs it expects, and what it returns. It's critical because the LLM uses this to decide whether to call the tool.

**Q: How do you debug LangChain applications?**
A: Use LangSmith for tracing, enable verbose mode on chains/agents, check intermediate steps, use callbacks for logging, and test components independently.

**Q: What's the difference between LangChain and LangSmith?**
A: LangChain is the development framework for building LLM apps. LangSmith is a monitoring/debugging platform for observing, testing, and improving those apps.

**Q: How do you handle errors in production?**
A: Use fallbacks, set max iterations on agents, validate inputs, implement try-catch blocks, use retry mechanisms, monitor with LangSmith, and have graceful degradation strategies.

---

## 📚 Additional Resources

### Official Documentation
- [LangChain Docs](https://python.langchain.com/)
- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [Twitter @LangChainAI](https://twitter.com/langchainai)

### Related Learning
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)

---

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'langchain'`
```bash
pip install langchain langchain-openai
```

**Issue**: `AuthenticationError` from Azure OpenAI
- Verify your Azure OpenAI endpoint is correct
- Check that your API key is valid
- Ensure your deployment name matches (gpt-4o)
- Confirm your Azure OpenAI resource is active

**Issue**: Agent runs forever / hits max iterations
- Set `max_iterations` on AgentExecutor
- Improve tool descriptions
- Use more capable models (gpt-4 vs gpt-3.5-turbo)

**Issue**: Memory not working
- Check you're using the correct memory variable name
- Verify memory is passed to the chain/agent
- For LCEL, use `RunnableWithMessageHistory`

**Issue**: Expensive API costs
- Use caching (`set_llm_cache`)
- Set lower `temperature` for more deterministic outputs
- Use cheaper models for simple tasks
- Implement token limits
- Sample production traces (don't trace everything)

---

## ✅ Learning Checklist

Track your progress:

- [ ] Completed `01_basics_and_setup.py`
- [ ] Completed `02_prompting_concepts.py`
- [ ] Completed `03_lcel.py`
- [ ] Completed `04_tools.py`
- [ ] Completed `05_memory.py`
- [ ] Completed `06_chain_building.py`
- [ ] Completed `07_agents.py`
- [ ] Completed `08_multi_agent.py`
- [ ] Completed `09_langsmith.py`
- [ ] Built a simple chatbot
- [ ] Created custom tools
- [ ] Built a RAG system
- [ ] Created a multi-tool agent
- [ ] Implemented multi-agent system
- [ ] Set up LangSmith monitoring
- [ ] Completed at least 3 practice exercises
- [ ] Built at least 1 complete project

---

## 🎉 What's Next?

After completing this guide, you should:

1. **Build Real Projects**: Apply concepts to real-world problems
2. **Contribute**: Consider contributing to LangChain or creating content
3. **Stay Updated**: LangChain evolves rapidly, follow updates
4. **Explore Advanced Topics**: 
   - LangGraph for complex agent workflows
   - Vector databases (Pinecone, Weaviate, Chroma)
   - Fine-tuning with LangChain
   - Production deployment strategies
   - Security and privacy best practices

5. **Join the Community**: Share your projects, help others, learn together

---

## 📝 Notes

- All examples use OpenAI's GPT models, but can be adapted for other providers
- Code is designed for learning, not production (add error handling, validation, etc.)
- Costs: Be mindful of API usage, especially with agents and long chains
- Keep your API keys secure, never commit them to version control

---

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to improve these examples!

---

## 📄 License

These educational materials are provided for learning purposes. Refer to LangChain's license for the framework itself.

---

**Happy Learning! 🚀**

Remember: The best way to learn is by building. Don't just read the code—run it, modify it, break it, and fix it. That's how you truly master LangChain!
