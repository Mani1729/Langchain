"""
Chain Building in LangChain
============================

THEORY:
-------
Chains combine multiple components (prompts, LLMs, tools, parsers) into 
sequences that accomplish complex tasks. Modern LangChain uses LCEL for chaining.

Key Concepts:
1. Sequential Chains - Execute steps in order
2. Router Chains - Route inputs to different sub-chains
3. Transform Chains - Process data between steps
4. Parallel Chains - Execute multiple chains simultaneously
5. Conditional Chains - Branch based on conditions
6. Chain Composition - Reusable chain components

Chain Types:
1. Simple Chains - Linear execution (A -> B -> C)
2. Sequential Chains - Multiple I/O mappings
3. Router Chains - Dynamic routing based on input
4. Map-Reduce Chains - Process items in parallel, then combine
5. Multi-Step Reasoning - Complex problem solving

Benefits of Chains:
- Modularity and reusability
- Complex workflow orchestration
- Clean, declarative code
- Built-in error handling
- Easy testing and debugging
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.7
)

# =============================================================================
# EXAMPLE 1: Simple Sequential Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Simple Sequential Chain")
print("=" * 60)

# Chain 1: Generate a topic
topic_chain = (
    ChatPromptTemplate.from_template("Suggest a {genre} story topic in 5 words")
    | llm
    | StrOutputParser()
)

# Chain 2: Write story based on topic
story_chain = (
    ChatPromptTemplate.from_template("Write a 3-sentence {genre} story about: {topic}")
    | llm
    | StrOutputParser()
)

# Chain 3: Add a moral
moral_chain = (
    ChatPromptTemplate.from_template("What's the moral of this story: {story}")
    | llm
    | StrOutputParser()
)

# Execute sequentially
genre = "science fiction"
topic = topic_chain.invoke({"genre": genre})
print(f"Topic: {topic}\n")

story = story_chain.invoke({"genre": genre, "topic": topic})
print(f"Story:\n{story}\n")

moral = moral_chain.invoke({"story": story})
print(f"Moral: {moral}\n")

# =============================================================================
# EXAMPLE 2: Combined Sequential Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Combined Sequential Chain")
print("=" * 60)

# Combine all steps into one chain
full_story_chain = (
    {"genre": RunnablePassthrough()}
    | RunnablePassthrough.assign(
        topic=lambda x: topic_chain.invoke({"genre": x["genre"]})
    )
    | RunnablePassthrough.assign(
        story=lambda x: story_chain.invoke({"genre": x["genre"], "topic": x["topic"]})
    )
    | RunnablePassthrough.assign(
        moral=lambda x: moral_chain.invoke({"story": x["story"]})
    )
)

result = full_story_chain.invoke({"genre": "mystery"})
print(f"Complete Result:")
print(f"Genre: {result['genre']}")
print(f"Topic: {result['topic']}")
print(f"Story: {result['story']}")
print(f"Moral: {result['moral']}\n")

# =============================================================================
# EXAMPLE 3: Parallel Execution Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: Parallel Execution Chain")
print("=" * 60)

# Generate multiple perspectives simultaneously
analysis_chain = RunnableParallel(
    technical=ChatPromptTemplate.from_template(
        "Analyze {topic} from a technical perspective in 2 sentences"
    ) | llm | StrOutputParser(),
    
    business=ChatPromptTemplate.from_template(
        "Analyze {topic} from a business perspective in 2 sentences"
    ) | llm | StrOutputParser(),
    
    ethical=ChatPromptTemplate.from_template(
        "Analyze {topic} from an ethical perspective in 2 sentences"
    ) | llm | StrOutputParser()
)

result = analysis_chain.invoke({"topic": "AI in healthcare"})
print("Technical:", result['technical'])
print("\nBusiness:", result['business'])
print("\nEthical:", result['ethical'])
print()

# =============================================================================
# EXAMPLE 4: Router Chain (Conditional Routing)
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Router Chain")
print("=" * 60)

from langchain_core.runnables import RunnableBranch

# Different processing based on input type
code_chain = (
    ChatPromptTemplate.from_template("Explain this code: {content}")
    | llm
    | StrOutputParser()
)

math_chain = (
    ChatPromptTemplate.from_template("Solve this math problem: {content}")
    | llm
    | StrOutputParser()
)

general_chain = (
    ChatPromptTemplate.from_template("Answer this question: {content}")
    | llm
    | StrOutputParser()
)

# Router function
def determine_type(x):
    content = x["content"].lower()
    if "code" in content or "function" in content or "def " in content:
        return "code"
    elif any(op in content for op in ["+", "-", "*", "/", "="]) and any(char.isdigit() for char in content):
        return "math"
    else:
        return "general"

# Create router
router_chain = RunnableBranch(
    (lambda x: determine_type(x) == "code", code_chain),
    (lambda x: determine_type(x) == "math", math_chain),
    general_chain  # default
)

# Test routing
test_inputs = [
    {"content": "def hello(): return 'world'"},
    {"content": "What is 15 + 27?"},
    {"content": "What is the capital of France?"}
]

for inp in test_inputs:
    result = router_chain.invoke(inp)
    print(f"Input: {inp['content']}")
    print(f"Response: {result}\n")

# =============================================================================
# EXAMPLE 5: Map-Reduce Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Map-Reduce Chain")
print("=" * 60)

# Process multiple items, then combine results
def map_reduce_chain(items):
    # Map: Process each item
    map_chain = (
        ChatPromptTemplate.from_template("Summarize in one sentence: {item}")
        | llm
        | StrOutputParser()
    )
    
    summaries = []
    for item in items:
        summary = map_chain.invoke({"item": item})
        summaries.append(summary)
    
    # Reduce: Combine all summaries
    reduce_chain = (
        ChatPromptTemplate.from_template(
            "Combine these summaries into one paragraph:\n\n{summaries}"
        )
        | llm
        | StrOutputParser()
    )
    
    combined = reduce_chain.invoke({"summaries": "\n".join(summaries)})
    return combined

# Example: Summarize multiple articles
articles = [
    "Machine learning is a subset of AI that enables computers to learn from data.",
    "Deep learning uses neural networks with multiple layers to process information.",
    "Natural language processing helps computers understand human language."
]

result = map_reduce_chain(articles)
print(f"Combined Summary:\n{result}\n")

# =============================================================================
# EXAMPLE 6: Transform Chain (Data Processing)
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: Transform Chain with Data Processing")
print("=" * 60)

# Chain with data transformations
def clean_text(text):
    return text.strip().lower().replace("  ", " ")

def count_words(text):
    return len(text.split())

transform_chain = (
    RunnableLambda(clean_text)
    | RunnableLambda(lambda x: {
        "cleaned_text": x,
        "word_count": count_words(x),
        "char_count": len(x)
    })
    | RunnableLambda(lambda x: {
        **x,
        "analysis": f"Text has {x['word_count']} words and {x['char_count']} characters"
    })
)

result = transform_chain.invoke("  Hello   World  from  LangChain  ")
print("Transform Result:")
for key, value in result.items():
    print(f"{key}: {value}")
print()

# =============================================================================
# EXAMPLE 7: Retrieval Chain (RAG Pattern)
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: Retrieval-Augmented Generation (RAG) Chain")
print("=" * 60)

# Simulated knowledge base
knowledge_base = {
    "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
    "javascript": "JavaScript is a versatile programming language primarily used for web development.",
    "typescript": "TypeScript is a superset of JavaScript that adds static typing.",
    "rust": "Rust is a systems programming language focused on safety, speed, and concurrency."
}

def retrieve_documents(query):
    """Simulate document retrieval"""
    query_lower = query.lower()
    relevant_docs = []
    for key, value in knowledge_base.items():
        if key in query_lower:
            relevant_docs.append(value)
    return "\n".join(relevant_docs) if relevant_docs else "No relevant information found."

# RAG chain: Retrieve -> Format -> Generate
rag_chain = (
    RunnablePassthrough.assign(
        context=RunnableLambda(lambda x: retrieve_documents(x["question"]))
    )
    | ChatPromptTemplate.from_template(
        """Answer the question based on the context below.
        
Context: {context}

Question: {question}

Answer:"""
    )
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke({"question": "What is Python used for?"})
print(f"RAG Answer: {result}\n")

# =============================================================================
# EXAMPLE 8: Multi-Step Reasoning Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 8: Multi-Step Reasoning Chain")
print("=" * 60)

# Step 1: Break down the problem
breakdown_chain = (
    ChatPromptTemplate.from_template(
        "Break down this problem into 3 steps: {problem}"
    )
    | llm
    | StrOutputParser()
)

# Step 2: Solve each step
solve_chain = (
    ChatPromptTemplate.from_template(
        "Given these steps:\n{steps}\n\nSolve the original problem: {problem}"
    )
    | llm
    | StrOutputParser()
)

# Combined reasoning chain
reasoning_chain = (
    RunnablePassthrough.assign(
        steps=lambda x: breakdown_chain.invoke({"problem": x["problem"]})
    )
    | RunnablePassthrough.assign(
        solution=lambda x: solve_chain.invoke({
            "steps": x["steps"],
            "problem": x["problem"]
        })
    )
)

problem = "How can I improve the performance of my web application?"
result = reasoning_chain.invoke({"problem": problem})
print(f"Problem: {problem}\n")
print(f"Steps:\n{result['steps']}\n")
print(f"Solution:\n{result['solution']}\n")

# =============================================================================
# EXAMPLE 9: Error Handling in Chains
# =============================================================================
print("=" * 60)
print("EXAMPLE 9: Error Handling in Chains")
print("=" * 60)

def risky_operation(x):
    """Function that might fail"""
    if "error" in x["input"].lower():
        raise ValueError("Intentional error for demonstration")
    return f"Processed: {x['input']}"

# Chain with fallback
safe_chain = RunnableLambda(risky_operation).with_fallbacks([
    RunnableLambda(lambda x: f"Fallback: Could not process '{x['input']}'")
])

# Test with normal input
result1 = safe_chain.invoke({"input": "Hello World"})
print(f"Normal: {result1}")

# Test with error-triggering input
result2 = safe_chain.invoke({"input": "This will error"})
print(f"Error handled: {result2}\n")

# =============================================================================
# EXAMPLE 10: Conditional Chain Execution
# =============================================================================
print("=" * 60)
print("EXAMPLE 10: Conditional Chain Execution")
print("=" * 60)

# Different processing based on length
short_chain = (
    ChatPromptTemplate.from_template("Expand this brief text: {text}")
    | llm
    | StrOutputParser()
)

long_chain = (
    ChatPromptTemplate.from_template("Summarize this long text: {text}")
    | llm
    | StrOutputParser()
)

def is_short(x):
    return len(x["text"].split()) < 10

conditional_chain = RunnableBranch(
    (is_short, short_chain),
    long_chain
)

# Test with short text
short_text = "AI is cool"
result1 = conditional_chain.invoke({"text": short_text})
print(f"Short text result: {result1}\n")

# Test with long text
long_text = "Artificial intelligence is a fascinating field that combines computer science, mathematics, and cognitive psychology to create systems that can perform tasks that typically require human intelligence."
result2 = conditional_chain.invoke({"text": long_text})
print(f"Long text result: {result2}\n")

# =============================================================================
# EXAMPLE 11: Chain with Memory
# =============================================================================
print("=" * 60)
print("EXAMPLE 11: Chain with Conversation Memory")
print("=" * 60)

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Create message store
message_store = {}

def get_session_history(session_id: str):
    if session_id not in message_store:
        message_store[session_id] = ChatMessageHistory()
    return message_store[session_id]

# Create chain with memory
memory_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Remember the user's preferences."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

memory_chain = memory_prompt | llm | StrOutputParser()

chain_with_memory = RunnableWithMessageHistory(
    memory_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Have a conversation
config = {"configurable": {"session_id": "user_001"}}

response1 = chain_with_memory.invoke(
    {"input": "My favorite color is blue."},
    config=config
)
print(f"Response 1: {response1}")

response2 = chain_with_memory.invoke(
    {"input": "What's my favorite color?"},
    config=config
)
print(f"Response 2: {response2}\n")

# =============================================================================
# EXAMPLE 12: Complex Production-Ready Chain
# =============================================================================
print("=" * 60)
print("EXAMPLE 12: Production-Ready Chain Pattern")
print("=" * 60)

# A complete chain with validation, processing, and formatting
class ProductionChain:
    def __init__(self, llm):
        self.llm = llm
        
        # Validation
        self.validator = RunnableLambda(self._validate_input)
        
        # Processing chain
        self.processor = (
            ChatPromptTemplate.from_template("Process this request: {input}")
            | llm
            | StrOutputParser()
        )
        
        # Formatter
        self.formatter = RunnableLambda(self._format_output)
        
        # Complete chain with error handling
        self.chain = (
            self.validator
            | self.processor
            | self.formatter
        ).with_fallbacks([
            RunnableLambda(lambda x: {"success": False, "error": "Processing failed"})
        ])
    
    def _validate_input(self, x):
        if not x.get("input") or len(x["input"]) < 3:
            raise ValueError("Input too short")
        return x
    
    def _format_output(self, output):
        return {
            "success": True,
            "result": output,
            "timestamp": "2024-01-01T00:00:00"
        }
    
    def run(self, user_input):
        return self.chain.invoke({"input": user_input})

# Use production chain
prod_chain = ProductionChain(llm)

# Valid input
result1 = prod_chain.run("Explain quantum computing")
print(f"Valid input result: {result1}\n")

# Invalid input (too short)
result2 = prod_chain.run("Hi")
print(f"Invalid input result: {result2}\n")

"""
KEY TAKEAWAYS:
--------------
1. Chains combine multiple components into workflows
2. Sequential chains execute steps in order
3. Parallel chains execute multiple operations simultaneously
4. Router chains conditionally route to different sub-chains
5. Map-reduce chains process items in parallel, then aggregate
6. Transform chains process data between steps
7. RAG chains retrieve context before generation
8. Use RunnablePassthrough to carry forward data
9. Fallbacks provide error resilience
10. Combine chains with memory for stateful conversations

CHAIN PATTERNS:
---------------
1. Sequential: step1 | step2 | step3
2. Parallel: RunnableParallel({a: chain_a, b: chain_b})
3. Conditional: RunnableBranch((condition, chain), default)
4. RAG: retrieve | format | generate
5. Map-Reduce: map(process_each) | reduce(combine)
6. Validation: validate | process | format
7. With Memory: prompt_with_history | llm | parser
8. With Fallback: risky_chain.with_fallbacks([safe_chain])

WHEN TO USE CHAINS:
-------------------
✅ Multi-step workflows
✅ Complex data processing
✅ Conditional logic
✅ Parallel operations
✅ RAG applications
✅ Production systems with error handling
✅ Reusable components
✅ Clear separation of concerns

BEST PRACTICES:
---------------
1. Keep chains modular and testable
2. Use meaningful variable names
3. Add fallbacks for resilience
4. Validate inputs early
5. Format outputs consistently
6. Log chain execution for debugging
7. Use type hints and documentation
8. Test each component independently

NEXT STEPS:
-----------
- 07_agents.py - Create autonomous agents
- 08_multi_agent.py - Multi-agent systems
"""

print("=" * 60)
print("Chain building concepts complete!")
print("=" * 60)
