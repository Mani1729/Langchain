"""
Multi-Agent Systems in LangChain
=================================

THEORY:
-------
Multi-agent systems involve multiple AI agents working together to solve
complex problems. Each agent has specialized roles and capabilities.

Key Concepts:
1. Agent Roles - Each agent has a specific purpose
2. Communication - Agents share information
3. Coordination - Managing agent interactions
4. Orchestration - Controlling workflow between agents
5. Collaboration - Agents work toward common goal

Multi-Agent Patterns:
1. Sequential - Agents execute in order
2. Parallel - Agents work simultaneously
3. Hierarchical - Manager agent coordinates workers
4. Debate - Agents discuss and reach consensus
5. Swarm - Many agents collaborate
6. Handoff - Agents pass tasks to each other

Benefits:
- Task specialization
- Parallel processing
- Better problem decomposition
- Fault tolerance
- Scalability

Use Cases:
- Research and analysis (multiple perspectives)
- Code review (different reviewers)
- Content creation (writer, editor, fact-checker)
- Customer service (routing to specialists)
- Complex problem solving
"""

# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from langchain.agents import tool, AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    deployment_name="gpt-4o-mini",
    temperature=0.7
)

# =============================================================================
# EXAMPLE 1: Sequential Multi-Agent System
# =============================================================================
print("=" * 60)
print("EXAMPLE 1: Sequential Multi-Agent System")
print("=" * 60)

class WriterAgent:
    """Agent specialized in writing content"""
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(
            "You are a creative writer. Write a short paragraph about: {topic}"
        )
        self.chain = self.prompt | llm | StrOutputParser()
    
    def execute(self, topic):
        print(f"[Writer Agent] Writing about: {topic}")
        result = self.chain.invoke({"topic": topic})
        print(f"[Writer Agent] Output: {result[:100]}...\n")
        return result

class EditorAgent:
    """Agent specialized in editing content"""
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(
            "You are an editor. Improve this text for clarity and grammar:\n\n{text}"
        )
        self.chain = self.prompt | llm | StrOutputParser()
    
    def execute(self, text):
        print(f"[Editor Agent] Editing text...")
        result = self.chain.invoke({"text": text})
        print(f"[Editor Agent] Output: {result[:100]}...\n")
        return result

class FactCheckerAgent:
    """Agent specialized in fact-checking"""
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(
            "You are a fact-checker. Review this text and suggest any factual improvements:\n\n{text}"
        )
        self.chain = self.prompt | llm | StrOutputParser()
    
    def execute(self, text):
        print(f"[Fact Checker Agent] Checking facts...")
        result = self.chain.invoke({"text": text})
        print(f"[Fact Checker Agent] Output: {result[:100]}...\n")
        return result

# Create sequential pipeline
writer = WriterAgent(llm)
editor = EditorAgent(llm)
fact_checker = FactCheckerAgent(llm)

# Execute sequential workflow
topic = "artificial intelligence in healthcare"
draft = writer.execute(topic)
edited = editor.execute(draft)
final = fact_checker.execute(edited)

print(f"Final Output:\n{final}\n")

# =============================================================================
# EXAMPLE 2: Parallel Multi-Agent System
# =============================================================================
print("=" * 60)
print("EXAMPLE 2: Parallel Multi-Agent System")
print("=" * 60)

class ResearchAgent:
    """Agent specialized in research"""
    def __init__(self, llm, specialty):
        self.llm = llm
        self.specialty = specialty
        self.prompt = ChatPromptTemplate.from_template(
            f"You are a {specialty} expert. Provide insights about: {{topic}}"
        )
        self.chain = self.prompt | llm | StrOutputParser()
    
    def execute(self, topic):
        print(f"[{self.specialty} Agent] Researching: {topic}")
        result = self.chain.invoke({"topic": topic})
        print(f"[{self.specialty} Agent] Done\n")
        return {self.specialty: result}

# Create specialized research agents
tech_agent = ResearchAgent(llm, "Technology")
business_agent = ResearchAgent(llm, "Business")
ethics_agent = ResearchAgent(llm, "Ethics")

# Execute in parallel (simulated - in production use async)
topic = "AI in autonomous vehicles"
results = []

for agent in [tech_agent, business_agent, ethics_agent]:
    results.append(agent.execute(topic))

# Combine results
print("=" * 60)
print("Combined Research Results:")
for result in results:
    for key, value in result.items():
        print(f"\n{key} Perspective:")
        print(value[:150] + "...")

# =============================================================================
# EXAMPLE 3: Hierarchical Multi-Agent (Manager + Workers)
# =============================================================================
print("=" * 60)
print("\nEXAMPLE 3: Hierarchical Multi-Agent System")
print("=" * 60)

class ManagerAgent:
    """Manager agent that delegates tasks"""
    def __init__(self, llm, worker_agents):
        self.llm = llm
        self.workers = worker_agents
    
    def execute(self, task):
        print(f"[Manager] Analyzing task: {task}\n")
        
        # Manager decides task breakdown
        planning_prompt = ChatPromptTemplate.from_template(
            """You are a project manager. Break down this task into subtasks:
            
Task: {task}

Available workers: {workers}

List subtasks and which worker should handle each."""
        )
        
        plan = (planning_prompt | self.llm | StrOutputParser()).invoke({
            "task": task,
            "workers": ", ".join(self.workers.keys())
        })
        
        print(f"[Manager] Plan:\n{plan}\n")
        
        # Execute with workers
        results = {}
        for worker_name, worker_agent in self.workers.items():
            print(f"[Manager] Delegating to {worker_name}...")
            results[worker_name] = worker_agent.execute(task)
        
        return results

class WorkerAgent:
    """Generic worker agent"""
    def __init__(self, llm, role):
        self.llm = llm
        self.role = role
    
    def execute(self, task):
        prompt = ChatPromptTemplate.from_template(
            f"You are a {self.role}. Complete this task: {{task}}"
        )
        result = (prompt | self.llm | StrOutputParser()).invoke({"task": task})
        print(f"[{self.role}] Completed task\n")
        return result

# Create hierarchical system
workers = {
    "Researcher": WorkerAgent(llm, "Researcher"),
    "Analyst": WorkerAgent(llm, "Data Analyst"),
    "Writer": WorkerAgent(llm, "Technical Writer")
}

manager = ManagerAgent(llm, workers)

# Execute hierarchical workflow
task = "Create a report on renewable energy trends"
results = manager.execute(task)

print("=" * 60)
print("Worker Results:")
for worker, output in results.items():
    print(f"\n{worker}:")
    print(output[:150] + "...")

# =============================================================================
# EXAMPLE 4: Debate System (Agents Discuss)
# =============================================================================
print("=" * 60)
print("\nEXAMPLE 4: Multi-Agent Debate System")
print("=" * 60)

class DebateAgent:
    """Agent that participates in debates"""
    def __init__(self, llm, position, name):
        self.llm = llm
        self.position = position
        self.name = name
    
    def argue(self, topic, previous_arguments=None):
        context = f"Previous arguments:\n{previous_arguments}\n\n" if previous_arguments else ""
        
        prompt = ChatPromptTemplate.from_template(
            f"""You are {self.name}, arguing {self.position}.
            
Topic: {{topic}}

{context}Make your argument (2-3 sentences):"""
        )
        
        argument = (prompt | self.llm | StrOutputParser()).invoke({"topic": topic})
        print(f"[{self.name}] {argument}\n")
        return argument

# Create debate agents
agent_pro = DebateAgent(llm, "in favor", "Agent Pro")
agent_con = DebateAgent(llm, "against", "Agent Con")
agent_neutral = DebateAgent(llm, "as a neutral moderator", "Moderator")

# Conduct debate
topic = "Remote work should be the default for all companies"
print(f"Debate Topic: {topic}\n")

# Round 1
arg_pro_1 = agent_pro.argue(topic)
arg_con_1 = agent_con.argue(topic, arg_pro_1)

# Round 2
arg_pro_2 = agent_pro.argue(topic, arg_con_1)
arg_con_2 = agent_con.argue(topic, arg_pro_2)

# Moderator summary
print("[Moderator] Summarizing debate...")
summary = agent_neutral.argue(
    topic,
    f"Pro: {arg_pro_1}\n{arg_pro_2}\n\nCon: {arg_con_1}\n{arg_con_2}"
)

# =============================================================================
# EXAMPLE 5: Agent Communication Protocol
# =============================================================================
print("=" * 60)
print("EXAMPLE 5: Agent Communication System")
print("=" * 60)

class Message:
    """Message passed between agents"""
    def __init__(self, sender, recipient, content, message_type="info"):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type
    
    def __repr__(self):
        return f"[{self.sender} -> {self.recipient}] {self.message_type}: {self.content[:50]}..."

class CommunicatingAgent:
    """Agent that can send and receive messages"""
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm
        self.inbox = []
    
    def receive_message(self, message):
        print(f"[{self.name}] Received message from {message.sender}")
        self.inbox.append(message)
    
    def process_messages(self):
        if not self.inbox:
            return "No messages to process"
        
        messages_text = "\n".join([f"{msg.sender}: {msg.content}" for msg in self.inbox])
        
        prompt = ChatPromptTemplate.from_template(
            f"""You are {self.name}. Process these messages and respond:
            
{{messages}}

Your response:"""
        )
        
        response = (prompt | self.llm | StrOutputParser()).invoke({"messages": messages_text})
        self.inbox.clear()
        return response

# Create communicating agents
agent_a = CommunicatingAgent("Alice", llm)
agent_b = CommunicatingAgent("Bob", llm)
agent_c = CommunicatingAgent("Carol", llm)

# Send messages
msg1 = Message("Alice", "Bob", "What's your opinion on the new feature?")
agent_b.receive_message(msg1)

msg2 = Message("Alice", "Carol", "Can you review the documentation?")
agent_c.receive_message(msg2)

# Process messages
print(f"\n[Bob's Response]")
bob_response = agent_b.process_messages()
print(bob_response)

print(f"\n[Carol's Response]")
carol_response = agent_c.process_messages()
print(carol_response)
print()

# =============================================================================
# EXAMPLE 6: Task Routing System
# =============================================================================
print("=" * 60)
print("EXAMPLE 6: Multi-Agent Task Routing")
print("=" * 60)

class RouterAgent:
    """Routes tasks to appropriate specialist agents"""
    def __init__(self, llm, specialists):
        self.llm = llm
        self.specialists = specialists
    
    def route(self, task):
        # Determine which specialist to use
        routing_prompt = ChatPromptTemplate.from_template(
            """You are a task router. Given this task and available specialists, choose the most appropriate one.
            
Task: {task}

Available specialists:
{specialists}

Respond with ONLY the specialist name (one word):"""
        )
        
        specialist_list = "\n".join([f"- {name}: {agent.description}" for name, agent in self.specialists.items()])
        
        chosen = (routing_prompt | self.llm | StrOutputParser()).invoke({
            "task": task,
            "specialists": specialist_list
        })
        
        chosen = chosen.strip().split()[0]  # Get first word
        print(f"[Router] Task routed to: {chosen}\n")
        
        # Execute with chosen specialist
        if chosen in self.specialists:
            return self.specialists[chosen].execute(task)
        else:
            return "Could not route task"

class SpecialistAgent:
    """Specialist agent with specific expertise"""
    def __init__(self, name, description, llm):
        self.name = name
        self.description = description
        self.llm = llm
    
    def execute(self, task):
        prompt = ChatPromptTemplate.from_template(
            f"""You are a {self.description}. Complete this task:
            
{{task}}

Your response:"""
        )
        
        result = (prompt | self.llm | StrOutputParser()).invoke({"task": task})
        print(f"[{self.name}] Task completed\n")
        return result

# Create specialists
specialists = {
    "CodeExpert": SpecialistAgent("CodeExpert", "code and programming expert", llm),
    "DataScientist": SpecialistAgent("DataScientist", "data analysis and statistics expert", llm),
    "Writer": SpecialistAgent("Writer", "content writing and editing expert", llm)
}

# Create router
router = RouterAgent(llm, specialists)

# Test routing
tasks = [
    "Write a blog post about machine learning",
    "Debug this Python code: def add(a b): return a+b",
    "Analyze this dataset and find correlations"
]

for task in tasks:
    print(f"Task: {task}")
    result = router.route(task)
    print(f"Result: {result[:100]}...\n")
    print("=" * 60)

# =============================================================================
# EXAMPLE 7: Collaborative Problem Solving
# =============================================================================
print("=" * 60)
print("EXAMPLE 7: Collaborative Multi-Agent Problem Solving")
print("=" * 60)

class CollaborativeSystem:
    """System where agents collaborate on complex problems"""
    def __init__(self, agents):
        self.agents = agents
    
    def solve_problem(self, problem):
        print(f"Problem: {problem}\n")
        
        insights = []
        
        # Each agent contributes
        for agent in self.agents:
            contribution = agent.contribute(problem, insights)
            insights.append({
                "agent": agent.name,
                "contribution": contribution
            })
        
        # Synthesize insights
        print("\n[System] Synthesizing insights...")
        synthesis = self._synthesize(problem, insights)
        return synthesis
    
    def _synthesize(self, problem, insights):
        insights_text = "\n\n".join([
            f"{i['agent']}: {i['contribution']}"
            for i in insights
        ])
        
        prompt = ChatPromptTemplate.from_template(
            """Synthesize these expert insights into a comprehensive solution:
            
Problem: {problem}

Expert Insights:
{insights}

Comprehensive Solution:"""
        )
        
        return (prompt | llm | StrOutputParser()).invoke({
            "problem": problem,
            "insights": insights_text
        })

class CollaborativeAgent:
    """Agent that contributes to collaborative problem solving"""
    def __init__(self, name, expertise, llm):
        self.name = name
        self.expertise = expertise
        self.llm = llm
    
    def contribute(self, problem, previous_insights):
        context = "\n".join([
            f"{i['agent']}: {i['contribution']}"
            for i in previous_insights
        ]) if previous_insights else "No previous insights"
        
        prompt = ChatPromptTemplate.from_template(
            f"""You are {self.name}, expert in {self.expertise}.
            
Problem: {{problem}}

Previous insights:
{{context}}

Your contribution (2-3 sentences):"""
        )
        
        contribution = (prompt | self.llm | StrOutputParser()).invoke({
            "problem": problem,
            "context": context
        })
        
        print(f"[{self.name}] {contribution}\n")
        return contribution

# Create collaborative team
team = [
    CollaborativeAgent("Alice", "user experience design", llm),
    CollaborativeAgent("Bob", "backend architecture", llm),
    CollaborativeAgent("Carol", "security", llm)
]

system = CollaborativeSystem(team)

# Solve problem collaboratively
problem = "Design a secure online payment system"
solution = system.solve_problem(problem)

print("=" * 60)
print(f"Final Solution:\n{solution}\n")

# =============================================================================
# EXAMPLE 8: Simple Multi-Agent Coordination
# =============================================================================
print("=" * 60)
print("EXAMPLE 8: Multi-Agent Coordination Pattern")
print("=" * 60)

class Coordinator:
    """Coordinates multiple agents"""
    def __init__(self):
        self.agents = {}
        self.task_queue = []
    
    def register_agent(self, name, agent):
        self.agents[name] = agent
        print(f"[Coordinator] Registered agent: {name}")
    
    def assign_task(self, agent_name, task):
        if agent_name in self.agents:
            print(f"[Coordinator] Assigning task to {agent_name}")
            return self.agents[agent_name].execute(task)
        else:
            return f"Agent {agent_name} not found"
    
    def broadcast_task(self, task):
        """Send task to all agents"""
        print(f"[Coordinator] Broadcasting task to all agents")
        results = {}
        for name, agent in self.agents.items():
            results[name] = agent.execute(task)
        return results

class SimpleAgent:
    """Simple agent for coordination example"""
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm
    
    def execute(self, task):
        prompt = ChatPromptTemplate.from_template(
            f"You are {self.name}. Complete this task in one sentence: {{task}}"
        )
        result = (prompt | self.llm | StrOutputParser()).invoke({"task": task})
        print(f"[{self.name}] {result}")
        return result

# Create coordinator
coordinator = Coordinator()

# Register agents
coordinator.register_agent("Agent1", SimpleAgent("Agent1", llm))
coordinator.register_agent("Agent2", SimpleAgent("Agent2", llm))
coordinator.register_agent("Agent3", SimpleAgent("Agent3", llm))

print("\n--- Single Task Assignment ---")
coordinator.assign_task("Agent1", "Summarize the benefits of AI")

print("\n--- Broadcast Task ---")
results = coordinator.broadcast_task("What is the most important tech trend?")
print()

"""
KEY TAKEAWAYS:
--------------
1. Multi-agent systems involve multiple specialized agents
2. Sequential: Agents execute in order (pipeline)
3. Parallel: Agents work simultaneously
4. Hierarchical: Manager agent coordinates workers
5. Debate: Agents discuss to reach consensus
6. Communication: Agents exchange messages
7. Routing: Direct tasks to appropriate specialists
8. Collaboration: Agents contribute different perspectives
9. Coordination: Central coordinator manages agents
10. Specialization improves overall system performance

MULTI-AGENT PATTERNS:
---------------------
1. Pipeline: Agent1 -> Agent2 -> Agent3
2. Parallel: All agents process simultaneously
3. Manager-Worker: One manager, multiple workers
4. Peer-to-Peer: Agents communicate directly
5. Hub-and-Spoke: Central coordinator, peripheral agents
6. Debate: Agents with different viewpoints
7. Ensemble: Combine outputs from multiple agents
8. Handoff: Agents pass tasks based on expertise

WHEN TO USE MULTI-AGENT:
-------------------------
✅ Complex problems needing multiple perspectives
✅ Task requires different expertise areas
✅ Parallel processing for speed
✅ Need specialized roles (writer, editor, etc.)
✅ Collaborative decision-making
✅ System resilience through redundancy
✅ Large-scale distributed systems

DESIGN CONSIDERATIONS:
----------------------
1. Clear Agent Roles - Each agent has specific purpose
2. Communication Protocol - How agents exchange information
3. Coordination Strategy - Who controls workflow
4. Error Handling - What if an agent fails
5. State Management - Shared vs. independent state
6. Performance - Parallel vs. sequential trade-offs
7. Cost - Multiple LLM calls add up
8. Debugging - Harder to trace multi-agent issues

BEST PRACTICES:
---------------
1. Start simple, add complexity as needed
2. Define clear agent responsibilities
3. Implement robust error handling
4. Log all agent interactions
5. Test agents independently first
6. Use async for true parallelism
7. Consider cost of multiple LLM calls
8. Monitor and optimize performance

NEXT STEPS:
-----------
- 09_langsmith.py - Monitor and debug with LangSmith
- README.md - Complete learning guide
"""

print("=" * 60)
print("Multi-agent concepts complete!")
print("=" * 60)
