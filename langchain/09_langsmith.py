"""
LangSmith - Monitoring and Debugging LangChain Applications
============================================================

THEORY:
-------
LangSmith is a platform for debugging, testing, evaluating, and monitoring
LLM applications. It provides observability for LangChain applications.

Key Features:
1. Tracing - See every step of chain/agent execution
2. Debugging - Identify issues in prompts and chains
3. Testing - Create test cases for your chains
4. Evaluation - Measure chain performance
5. Monitoring - Production app monitoring
6. Datasets - Manage test datasets
7. Feedback - Collect user feedback
8. Analytics - Performance metrics

LangChain vs LangSmith:
-----------------------

LANGCHAIN:
- Framework for building LLM apps
- Provides components (chains, agents, tools)
- Development library
- Open source
- Used during development AND production
- Handles application logic

LANGSMITH:
- Platform for monitoring and improving LLM apps
- Provides observability and debugging
- Monitoring/DevOps tool
- Commercial service (free tier available)
- Used during development AND production
- Handles observability and analytics

WHEN TO USE WHAT:
-----------------

Use LangChain When:
✅ Building LLM applications
✅ Need chains, agents, tools
✅ Integrating multiple LLMs
✅ Need prompt templates
✅ Building conversational AI
✅ Creating RAG systems

Use LangSmith When:
✅ Debugging LangChain apps
✅ Need to trace execution
✅ Want to monitor production apps
✅ Evaluate prompt performance
✅ Track costs and latency
✅ Manage test datasets
✅ A/B test different prompts

YOU TYPICALLY USE BOTH:
- LangChain to build
- LangSmith to monitor, debug, and improve
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# EXAMPLE 1: Setting Up LangSmith
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: LangSmith Setup")
print("=" * 60)

print("""
SETUP STEPS:
------------

1. Create LangSmith Account:
   - Go to https://smith.langchain.com
   - Sign up for free account
   - Create a new project

2. Get API Key:
   - Navigate to Settings -> API Keys
   - Create new API key
   - Copy the key

3. Set Environment Variables:
   
   In your .env file:
   ```
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   LANGCHAIN_API_KEY=your_api_key_here
   LANGCHAIN_PROJECT=your_project_name
   ```

4. Install LangSmith:
   ```
   pip install langsmith
   ```

That's it! LangChain will automatically send traces to LangSmith.
""")

# =============================================================================
# EXAMPLE 2: Basic Tracing
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Basic Tracing with LangSmith")
print("=" * 60)

# Enable tracing (set in .env for real use)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langchain-tutorial"

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.7
)

# This chain will be automatically traced
chain = (
    ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    | llm
    | StrOutputParser()
)

print("Executing chain (will be traced in LangSmith)...")
result = chain.invoke({"topic": "programming"})
print(f"Result: {result}\n")

print("""
What you'll see in LangSmith:
- Complete execution trace
- Input and output for each step
- Latency for each component
- Token usage
- Cost estimation
- Any errors that occurred

Check your LangSmith dashboard to see the trace!
""")

# =============================================================================
# EXAMPLE 3: Tracing Complex Chains
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: Tracing Complex Chains")
print("=" * 60)

from langchain_core.runnables import RunnablePassthrough

# Multi-step chain
complex_chain = (
    RunnablePassthrough.assign(
        summary=ChatPromptTemplate.from_template(
            "Summarize this topic in one sentence: {topic}"
        ) | llm | StrOutputParser()
    )
    | RunnablePassthrough.assign(
        details=lambda x: (
            ChatPromptTemplate.from_template(
                "Expand on this summary: {summary}"
            ) | llm | StrOutputParser()
        ).invoke({"summary": x["summary"]})
    )
)

print("Executing complex chain...")
result = complex_chain.invoke({"topic": "quantum computing"})
print(f"Summary: {result['summary']}")
print(f"Details: {result['details'][:100]}...\n")

print("""
In LangSmith you'll see:
- Each step of the chain
- How data flows between steps
- Which step takes longest
- Where errors occur (if any)
- Full input/output at each stage
""")

# =============================================================================
# EXAMPLE 4: Tracing Agents
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Tracing Agents with Tools")
print("=" * 60)

from langchain.agents import tool, AgentExecutor, create_openai_functions_agent

@tool
def calculator(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        return f"Result: {eval(expression)}"
    except:
        return "Error in calculation"

@tool
def word_counter(text: str) -> str:
    """Count words in text."""
    return f"Word count: {len(text.split())}"

tools = [calculator, word_counter]

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_openai_functions_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

print("Executing agent (tracing enabled)...")
result = agent_executor.invoke({"input": "What is 25 * 4?"})
print(f"Result: {result['output']}\n")

print("""
Agent traces in LangSmith show:
- Agent's reasoning process
- Which tools were called
- Tool inputs and outputs
- Decision-making at each step
- Why certain tools were chosen
- Full conversation flow
""")

# =============================================================================
# EXAMPLE 5: Custom Run Names and Metadata
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Adding Metadata to Traces")
print("=" * 60)

from langchain_core.runnables import RunnableConfig

# Add custom metadata to trace
config = RunnableConfig(
    run_name="customer_query_analysis",
    tags=["production", "customer-service"],
    metadata={
        "user_id": "user_123",
        "session_id": "session_456",
        "environment": "production"
    }
)

print("Executing with metadata...")
result = chain.invoke(
    {"topic": "customer support"},
    config=config
)
print(f"Result: {result}\n")

print("""
Metadata helps you:
- Filter traces by tag
- Track specific users or sessions
- Differentiate dev/staging/prod
- Add custom identifiers
- Organize traces by feature
""")

# =============================================================================
# EXAMPLE 6: Using LangSmith Client Directly
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: LangSmith Client for Advanced Features")
print("=" * 60)

try:
    from langsmith import Client
    
    # Initialize client
    client = Client()
    
    print("LangSmith Client Features:\n")
    
    # List recent runs
    print("1. List Recent Runs")
    print("   runs = client.list_runs(project_name='your-project')\n")
    
    # Create dataset
    print("2. Create Test Dataset")
    print("   dataset = client.create_dataset('test-dataset')")
    print("   client.create_examples(...)\n")
    
    # Add feedback
    print("3. Add Feedback to Runs")
    print("   client.create_feedback(run_id, key='user_rating', score=5)\n")
    
    # Get project stats
    print("4. Get Project Statistics")
    print("   stats = client.get_project_stats(project_name='your-project')\n")
    
except ImportError:
    print("Install langsmith: pip install langsmith\n")

# =============================================================================
# EXAMPLE 7: Creating Test Datasets
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: Test Datasets for Evaluation")
print("=" * 60)

print("""
CREATING TEST DATASETS:
-----------------------

1. In LangSmith UI:
   - Go to Datasets tab
   - Click "New Dataset"
   - Add test examples manually

2. Programmatically:
   
   from langsmith import Client
   
   client = Client()
   
   # Create dataset
   dataset = client.create_dataset("my-test-set")
   
   # Add examples
   examples = [
       {"input": {"topic": "AI"}, "output": "Expected response..."},
       {"input": {"topic": "ML"}, "output": "Expected response..."}
   ]
   
   for example in examples:
       client.create_example(
           inputs=example["input"],
           outputs=example["output"],
           dataset_id=dataset.id
       )

3. Run Evaluations:
   
   from langchain.smith import run_on_dataset
   
   results = run_on_dataset(
       client=client,
       dataset_name="my-test-set",
       llm_or_chain_factory=lambda: chain,
       evaluation=your_evaluation_function
   )

Benefits:
- Regression testing
- Compare prompt versions
- A/B testing
- Performance benchmarks
""")

# =============================================================================
# EXAMPLE 8: Evaluation Functions
# =============================================================================
print("=" * 60)
print("EXAMPLE 8: Custom Evaluation Functions")
print("=" * 60)

print("""
EVALUATION PATTERNS:
--------------------

1. Exact Match:
   def exact_match_eval(run, example):
       prediction = run.outputs["output"]
       reference = example.outputs["output"]
       return {"score": 1 if prediction == reference else 0}

2. Contains Check:
   def contains_eval(run, example):
       prediction = run.outputs["output"]
       keywords = example.outputs["keywords"]
       score = sum(kw in prediction for kw in keywords) / len(keywords)
       return {"score": score}

3. LLM-as-Judge:
   def llm_judge_eval(run, example):
       evaluator_llm = ChatOpenAI(model="gpt-4")
       prompt = f'''
       Rate this response from 1-10:
       Input: {example.inputs}
       Response: {run.outputs["output"]}
       '''
       score = evaluator_llm.invoke(prompt)
       return {"score": score}

4. Custom Metrics:
   def custom_eval(run, example):
       prediction = run.outputs["output"]
       
       # Multiple metrics
       length_ok = 50 < len(prediction) < 200
       has_code = "```" in prediction
       
       return {
           "length_ok": length_ok,
           "has_code": has_code,
           "overall": length_ok and has_code
       }
""")

# =============================================================================
# EXAMPLE 9: Monitoring Production
# =============================================================================
print("=" * 60)
print("EXAMPLE 9: Production Monitoring")
print("=" * 60)

print("""
PRODUCTION MONITORING:
----------------------

1. Always-On Tracing:
   - Set LANGCHAIN_TRACING_V2=true in production
   - Monitor all runs in real-time
   - Get alerts on errors

2. Sampling for Cost:
   - Use sampling to reduce tracing costs
   
   import random
   
   def should_trace():
       return random.random() < 0.1  # 10% sampling
   
   os.environ["LANGCHAIN_TRACING_V2"] = str(should_trace())

3. User Feedback:
   from langsmith import Client
   
   client = Client()
   
   # After user rates response
   client.create_feedback(
       run_id=run_id,
       key="user_rating",
       score=user_rating,
       comment=user_comment
   )

4. Dashboard Metrics:
   - Average latency
   - Token usage and costs
   - Error rates
   - User satisfaction scores
   - Most used tools/chains
   - Performance over time

5. Alerts:
   - Set up alerts for high error rates
   - Monitor latency spikes
   - Track cost anomalies
""")

# =============================================================================
# EXAMPLE 10: Debugging with LangSmith
# =============================================================================
print("=" * 60)
print("EXAMPLE 10: Debugging Workflow")
print("=" * 60)

print("""
DEBUGGING WORKFLOW:
-------------------

1. Identify Issue:
   - Check LangSmith dashboard for errors
   - Look at failed runs
   - Filter by error type

2. Inspect Trace:
   - Click on failed run
   - See exact step that failed
   - View input/output at each step
   - Check token usage

3. Reproduce Locally:
   - Copy input from trace
   - Run locally with same input
   - Add debugging logs

4. Fix and Test:
   - Modify prompt/chain
   - Run on test dataset
   - Compare results in LangSmith

5. Deploy:
   - Push changes
   - Monitor in production
   - Verify fix in dashboard

COMMON ISSUES TO DEBUG:
-----------------------
- Hallucinations: Check if context is included
- Formatting errors: Inspect output parser
- Tool failures: Check tool inputs
- Latency: Identify slow components
- Cost spikes: Find token-heavy operations
""")

# =============================================================================
# EXAMPLE 11: A/B Testing Prompts
# =============================================================================
print("=" * 60)
print("EXAMPLE 11: A/B Testing with LangSmith")
print("=" * 60)

print("""
A/B TESTING PROMPTS:
--------------------

1. Create Two Versions:
   
   prompt_a = ChatPromptTemplate.from_template(
       "Explain {topic} in simple terms"
   )
   
   prompt_b = ChatPromptTemplate.from_template(
       "Explain {topic} as if teaching a 5-year-old"
   )
   
   chain_a = prompt_a | llm | StrOutputParser()
   chain_b = prompt_b | llm | StrOutputParser()

2. Tag Variants:
   
   config_a = RunnableConfig(tags=["prompt-a", "experiment-1"])
   config_b = RunnableConfig(tags=["prompt-b", "experiment-1"])

3. Run in Production:
   
   import random
   
   if random.random() < 0.5:
       result = chain_a.invoke(input, config=config_a)
   else:
       result = chain_b.invoke(input, config=config_b)

4. Analyze in LangSmith:
   - Filter by tag
   - Compare metrics:
     * User satisfaction
     * Latency
     * Token usage
     * Error rates
   - Determine winner

5. Roll Out Winner:
   - Deploy winning variant
   - Monitor performance
   - Iterate with new tests
""")

# =============================================================================
# EXAMPLE 12: Best Practices
# =============================================================================
print("=" * 60)
print("EXAMPLE 12: LangSmith Best Practices")
print("=" * 60)

print("""
LANGSMITH BEST PRACTICES:
-------------------------

1. Project Organization:
   ✅ Separate projects for dev/staging/prod
   ✅ Use descriptive project names
   ✅ Archive old projects

2. Tagging Strategy:
   ✅ Tag by feature: ["search", "chat", "summarization"]
   ✅ Tag by version: ["v1.0", "v2.0"]
   ✅ Tag by environment: ["dev", "prod"]
   ✅ Tag experiments: ["experiment-123"]

3. Metadata:
   ✅ Add user_id for per-user analysis
   ✅ Add session_id for conversation tracking
   ✅ Add custom business metrics
   ✅ Include timestamps

4. Cost Management:
   ✅ Use sampling in high-volume production
   ✅ Don't trace internal dev experiments
   ✅ Archive old traces
   ✅ Monitor your LangSmith usage

5. Testing:
   ✅ Create datasets for critical flows
   ✅ Run evals before deployment
   ✅ Compare prompt versions
   ✅ Track regression tests

6. Monitoring:
   ✅ Set up error alerts
   ✅ Monitor latency trends
   ✅ Track user feedback
   ✅ Review traces weekly

7. Team Collaboration:
   ✅ Share interesting traces
   ✅ Document common issues
   ✅ Create evaluation standards
   ✅ Review metrics together

8. Security:
   ✅ Don't log sensitive data
   ✅ Rotate API keys regularly
   ✅ Control team access
   ✅ Audit trace data
""")

"""
KEY TAKEAWAYS:
--------------

LANGCHAIN VS LANGSMITH:
-----------------------
LangChain: Framework to BUILD LLM apps
LangSmith: Platform to MONITOR and IMPROVE LLM apps

Use both together for best results!

LANGSMITH FEATURES:
-------------------
1. Tracing - See every step of execution
2. Debugging - Identify and fix issues
3. Testing - Create and run test datasets
4. Evaluation - Measure performance
5. Monitoring - Track production metrics
6. Feedback - Collect user ratings
7. A/B Testing - Compare variants
8. Analytics - Understand usage patterns

WHEN TO USE LANGSMITH:
----------------------
✅ During development for debugging
✅ In production for monitoring
✅ For testing before deployment
✅ When optimizing prompts
✅ For cost and latency analysis
✅ When tracking user feedback
✅ For team collaboration

SETUP CHECKLIST:
----------------
□ Create LangSmith account
□ Get API key
□ Set environment variables
□ Enable tracing
□ Create project
□ Start building with LangChain
□ Check traces in dashboard
□ Create test datasets
□ Set up evaluations
□ Monitor production

RESOURCES:
----------
- LangSmith: https://smith.langchain.com
- Docs: https://docs.smith.langchain.com
- Python SDK: pip install langsmith
- Discord: LangChain community

NEXT STEPS:
-----------
Now that you understand all LangChain concepts, practice by:
1. Building a complete RAG application
2. Creating an agent with multiple tools
3. Implementing a multi-agent system
4. Monitoring everything with LangSmith

Review the README.md for practice exercises!
"""

print("=" * 60)
print("LangSmith concepts complete!")
print("=" * 60)
print("\nYou've completed all LangChain tutorials!")
print("Check the README.md for practice exercises and next steps.")
