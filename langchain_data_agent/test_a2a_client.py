"""Simple test client for the A2A Data Agent server."""

import asyncio
import logging
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Test the A2A server with sample queries."""
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=120.0) as http:
        # Fetch agent card
        logger.info(f"Fetching agent card from {base_url}/.well-known/agent-card.json")
        resolver = A2ACardResolver(httpx_client=http, base_url=base_url)
        card = await resolver.get_agent_card()
        
        # Display agent info
        print("\n" + "="*70)
        print(f"🤖 Agent: {card.name}")
        print(f"📝 Description: {card.description}")
        print(f"🔧 Version: {card.version}")
        print(f"🌐 URL: {card.url}")
        print("\n💡 Capabilities:")
        print(f"   - Streaming: {card.capabilities.streaming}")
        print(f"   - State History: {card.capabilities.state_transition_history}")
        print("\n🎯 Available Skills:")
        for skill in card.skills:
            print(f"   - {skill.name}: {skill.description}")
        print("="*70 + "\n")
        
        # Create client
        client = ClientFactory(ClientConfig(httpx_client=http)).create(card=card)
        
        # Test queries
        questions = [
            "How many active employees are there?",
            "What is the average PGC tenure by paygrade?",
            "Show me the distribution of employees by pillar",
        ]
        
        for question in questions:
            print(f"\n{'─'*70}")
            print(f"❓ Question: {question}")
            print('─'*70)
            
            message = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text=question))],
                message_id=uuid4().hex,
            )
            
            try:
                async for event in client.send_message(message):
                    if isinstance(event, Message):
                        for part in event.parts:
                            if hasattr(part, "root") and hasattr(part.root, "text"):
                                print(f"💬 {part.root.text}")
                    else:
                        task, _ = event
                        if task.status.state == "completed" and task.artifacts:
                            for artifact in task.artifacts:
                                for part in artifact.parts:
                                    if hasattr(part, "root") and hasattr(part.root, "text"):
                                        print(f"✅ {part.root.text}")
            except Exception as e:
                logger.error(f"Error processing query: {e}", exc_info=True)
        
        print(f"\n{'='*70}")
        print("✨ Test completed!")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
