"""
Prompting Concepts in LangChain
================================

THEORY:
-------
Prompting is the art of instructing LLMs to get desired outputs.
LangChain provides powerful abstractions for prompt engineering:

1. PromptTemplate - Dynamic string-based prompts
2. ChatPromptTemplate - For chat models with roles
3. FewShotPromptTemplate - Examples-based learning
4. MessagesPlaceholder - Dynamic message insertion
5. Partial Variables - Pre-fill some template variables

Best Practices:
- Be specific and clear
- Provide examples (few-shot learning)
- Use role-based prompting for chat models
- Structure with delimiters
- Iterate and test
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint="https://your-resource-name.openai.azure.com",
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2025-01-01-preview",
    deployment_name="gpt-4o-mini",
    temperature=0.7
)

# =============================================================================
# EXAMPLE 1: Basic Prompt Template
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Basic Prompt Template")
print("=" * 60)

from langchain_core.prompts import PromptTemplate

# Simple template
template = PromptTemplate(
    input_variables=["product", "audience"],
    template="Write a marketing slogan for {product} targeting {audience}."
)

# Generate prompt
prompt = template.format(product="eco-friendly water bottle", audience="millennials")
print(f"Generated Prompt:\n{prompt}\n")

response = llm.invoke(prompt)
print(f"Response: {response.content}\n")

# Alternative syntax (from_template)
template2 = PromptTemplate.from_template(
    "Translate the following to {language}: {text}"
)
prompt2 = template2.format(language="French", text="Hello, how are you?")
response2 = llm.invoke(prompt2)
print(f"Translation: {response2.content}\n")

# =============================================================================
# EXAMPLE 2: Chat Prompt Templates
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Chat Prompt Templates")
print("=" * 60)

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Method 1: Using tuples
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} that responds in {style} style."),
    ("human", "{user_input}")
])

messages = chat_template.format_messages(
    role="pirate captain",
    style="pirate",
    user_input="Tell me about your ship"
)
response = llm.invoke(messages)
print(f"Response: {response.content}\n")

# Method 2: Using message templates explicitly
system_template = SystemMessagePromptTemplate.from_template(
    "You are an expert {domain} consultant with {years} years of experience."
)
human_template = HumanMessagePromptTemplate.from_template("{question}")

chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])
messages = chat_prompt.format_messages(
    domain="cybersecurity",
    years=15,
    question="What are the top 3 security practices for cloud applications?"
)
response = llm.invoke(messages)
print(f"Expert Response:\n{response.content}\n")

# =============================================================================
# EXAMPLE 3: Few-Shot Prompting
# =============================================================================
print("=" * 60)
print("EXAMPLE 3: Few-Shot Prompting")
print("=" * 60)

from langchain_core.prompts import FewShotPromptTemplate

# Define examples
examples = [
    {
        "input": "happy",
        "output": "sad"
    },
    {
        "input": "tall",
        "output": "short"
    },
    {
        "input": "hot",
        "output": "cold"
    }
]

# Create example template
example_template = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

# Create few-shot template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="Give the antonym of each word:",
    suffix="Input: {word}\nOutput:",
    input_variables=["word"]
)

prompt = few_shot_prompt.format(word="bright")
print(f"Few-Shot Prompt:\n{prompt}\n")
response = llm.invoke(prompt)
print(f"Response: {response.content}\n")

# =============================================================================
# EXAMPLE 4: Few-Shot with Example Selector
# =============================================================================
print("=" * 60)
print("EXAMPLE 4: Dynamic Few-Shot with Example Selector")
print("=" * 60)
print("NOTE: This example uses LengthBasedExampleSelector which doesn't require embeddings.\n")
print("      For semantic similarity selection, you would need an Azure OpenAI embeddings deployment.\n")

from langchain_core.example_selectors import LengthBasedExampleSelector

# More examples for selection
code_examples = [
    {
        "question": "How do I read a file in Python?",
        "answer": "with open('file.txt', 'r') as f:\n    content = f.read()"
    },
    {
        "question": "How do I write to a file in Python?",
        "answer": "with open('file.txt', 'w') as f:\n    f.write('Hello World')"
    },
    {
        "question": "How do I append to a file in Python?",
        "answer": "with open('file.txt', 'a') as f:\n    f.write('New line')"
    },
    {
        "question": "How do I make an HTTP request in Python?",
        "answer": "import requests\nresponse = requests.get('https://api.example.com')"
    },
    {
        "question": "How do I parse JSON in Python?",
        "answer": "import json\ndata = json.loads(json_string)"
    }
]

# Create template
example_template = PromptTemplate(
    input_variables=["question", "answer"],
    template="Q: {question}\nA: {answer}"
)

# Create length-based example selector (selects examples based on input length)
example_selector = LengthBasedExampleSelector(
    examples=code_examples,
    example_prompt=example_template,
    max_length=100  # Maximum length of formatted examples
)

few_shot_with_selector = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_template,
    prefix="Answer the following coding question with Python code:",
    suffix="Q: {question}\nA:",
    input_variables=["question"]
)

# Test with short question (will include more examples)
prompt = few_shot_with_selector.format(question="How do I read JSON?")
print(f"Dynamic Few-Shot Prompt (short question):\n{prompt}\n")
response = llm.invoke(prompt)
print(f"Response: {response.content}\n")

# =============================================================================
# EXAMPLE 5: Partial Variables
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Partial Variables")
print("=" * 60)

from datetime import datetime

# Function to get current date
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")

# Template with partial
prompt_with_date = PromptTemplate(
    input_variables=["topic"],
    template="Today's date is {date}. Write a news headline about {topic}.",
    partial_variables={"date": get_current_date}
)

prompt = prompt_with_date.format(topic="AI breakthroughs")
print(f"Prompt with Date:\n{prompt}\n")
response = llm.invoke(prompt)
print(f"Response: {response.content}\n")

# =============================================================================
# EXAMPLE 6: Messages Placeholder
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: Messages Placeholder for Chat History")
print("=" * 60)

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])

# Simulate conversation history
history = [
    HumanMessage(content="My name is Alice."),
    AIMessage(content="Hello Alice! Nice to meet you."),
    HumanMessage(content="I love programming."),
    AIMessage(content="That's great! Programming is a valuable skill.")
]

messages = chat_prompt.format_messages(
    chat_history=history,
    user_input="What's my name and what do I love?"
)
response = llm.invoke(messages)
print(f"Response with Context: {response.content}\n")

# =============================================================================
# EXAMPLE 7: Structured Output Prompting
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: Prompting for Structured Output")
print("=" * 60)

structured_template = ChatPromptTemplate.from_messages([
    ("system", """You are a data extraction assistant. 
    Extract information and return ONLY a valid JSON object with no additional text.
    Format:
    {{
        "name": "person's name",
        "age": age as integer,
        "skills": ["skill1", "skill2"],
        "experience_years": years as integer
    }}"""),
    ("human", "{text}")
])

messages = structured_template.format_messages(
    text="John Smith is a 32-year-old software engineer with 10 years of experience. He specializes in Python, JavaScript, and cloud computing."
)
response = llm.invoke(messages)
print(f"Structured Output:\n{response.content}\n")

# =============================================================================
# EXAMPLE 8: Prompt Composition
# =============================================================================
print("=" * 60)
print("EXAMPLE 8: Prompt Composition")
print("=" * 60)

# Create reusable prompt components
format_instruction = """Please format your response as follows:
1. Start with a brief summary
2. List main points with bullet points
3. End with a conclusion"""

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert analyst. {format_instructions}"),
    ("human", "Analyze the following: {topic}")
])

messages = analysis_prompt.format_messages(
    format_instructions=format_instruction,
    topic="Impact of AI on healthcare"
)
response = llm.invoke(messages)
print(f"Formatted Analysis:\n{response.content}\n")

# =============================================================================
# EXAMPLE 9: Prompt Piping (Using LCEL)
# =============================================================================
print("=" * 60)
print("EXAMPLE 9: Prompt Piping with LCEL")
print("=" * 60)

from langchain_core.output_parsers import StrOutputParser

# Create a chain: prompt -> llm -> parser
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm | StrOutputParser()

# Execute chain
result = chain.invoke({"topic": "programming"})
print(f"Joke: {result}\n")

# =============================================================================
# EXAMPLE 10: Advanced Prompting Techniques
# =============================================================================
print("=" * 60)
print("EXAMPLE 10: Advanced Prompting Techniques")
print("=" * 60)

# Chain-of-Thought Prompting
cot_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math tutor. Solve problems step by step, showing your reasoning."),
    ("human", "{problem}")
])

messages = cot_prompt.format_messages(
    problem="If a train travels 120 miles in 2 hours, and then 180 miles in 3 hours, what is its average speed?"
)
response = llm.invoke(messages)
print(f"Chain-of-Thought Response:\n{response.content}\n")

# Role-Based Prompting
role_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a {role}. 
    Expertise: {expertise}
    Audience: {audience}
    Tone: {tone}"""),
    ("human", "{question}")
])

messages = role_prompt.format_messages(
    role="Senior Software Architect",
    expertise="Microservices and distributed systems",
    audience="Junior developers",
    tone="Educational and encouraging",
    question="What are the key considerations when designing a microservices architecture?"
)
response = llm.invoke(messages)
print(f"Role-Based Response:\n{response.content}\n")

"""
KEY TAKEAWAYS:
--------------
1. PromptTemplate: For simple string templates
2. ChatPromptTemplate: For chat models with system/human/ai roles
3. Few-Shot Learning: Provide examples to guide the model
4. Example Selectors: Dynamically choose relevant examples
5. Partial Variables: Pre-fill template variables (e.g., current date)
6. MessagesPlaceholder: Insert dynamic conversation history
7. Structured Output: Guide LLM to return specific formats (JSON, lists)
8. Prompt Composition: Build complex prompts from reusable components
9. Chain-of-Thought: Ask model to show reasoning step-by-step
10. Role-Based: Set expertise, audience, and tone for better responses

PROMPTING BEST PRACTICES:
--------------------------
1. Be Specific: "List 5 benefits" vs "Tell me about benefits"
2. Use Examples: Show the format you want
3. Set Context: Define role, expertise, audience
4. Structure Output: Request specific formats (JSON, bullet points)
5. Break Down Complex Tasks: Use chain-of-thought
6. Iterate: Test and refine prompts
7. Use Delimiters: Separate instructions from content (e.g., ```, ---)
8. Specify Length: "In 100 words" or "3 bullet points"

NEXT STEPS:
-----------
- 03_lcel.py - Master LangChain Expression Language for chaining
- 04_tools.py - Learn to call external tools and functions
"""

print("=" * 60)
print("Prompting concepts complete!")
print("=" * 60)
