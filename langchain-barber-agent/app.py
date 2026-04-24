"""Chainlit application for barbershop booking agent.

This module provides a web-based chat interface using Chainlit
for interacting with the barbershop booking agent.

Usage:
    chainlit run app.py -w
"""

import uuid
from datetime import datetime
from pathlib import Path

import chainlit as cl
import chainlit.data as cl_data
import yaml
from langchain_core.messages import HumanMessage

# Disable Chainlit's data persistence completely
cl_data._data_layer = None


def load_business_config() -> dict:
    """Load business configuration from seed_data.yaml.

    Returns:
        Business configuration dictionary.
    """
    seed_file = Path(__file__).parent / "src" / "utils" / "seed_data.yaml"
    if seed_file.exists():
        with open(seed_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("business", {})
    return {}


@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    # Load business configuration
    business_config = load_business_config()
    business_name = business_config.get("name", "The Barbershop")

    # Create agent
    from src.agent.agent import create_booking_agent

    agent = create_booking_agent(business_name=business_name)

    # Create a unique thread ID for this conversation session
    thread_id = str(uuid.uuid4())

    # Store in session
    cl.user_session.set("agent", agent)
    cl.user_session.set("thread_id", thread_id)
    cl.user_session.set("business_name", business_name)

    # Send welcome message
    await cl.Message(
        content=f"👋 Welcome to **{business_name}**!\n\n"
        f"I'm your booking assistant. I can help you:\n"
        f"- 💇 Book appointments\n"
        f"- 📅 Check availability\n"
        f"- ℹ️ View our services and barbers\n"
        f"- 👤 Manage your profile\n\n"
        f"How can I help you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    # Get agent and config from session
    agent = cl.user_session.get("agent")
    thread_id = cl.user_session.get("thread_id")
    business_name = cl.user_session.get("business_name")

    if not agent:
        await cl.Message(content="⚠️ Agent not initialized. Please refresh the page.").send()
        return

    # Create config with thread ID for checkpointing
    config = {"configurable": {"thread_id": thread_id}}

    # Create user message
    user_message = HumanMessage(content=message.content)

    # Initialize state with new message
    initial_state = {
        "messages": [user_message],
        "business_name": business_name,
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }

    # Create a response message that we'll stream to
    response_msg = cl.Message(content="")
    await response_msg.send()

    try:
        # Invoke agent with checkpoint config
        result = await agent.ainvoke(initial_state, config=config)

        # Extract the final assistant message
        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            response_content = last_message.content

            # Handle tool responses and AI messages
            if hasattr(last_message, "content"):
                response_msg.content = response_content
                await response_msg.update()
            else:
                response_msg.content = "I've processed your request."
                await response_msg.update()
        else:
            response_msg.content = "I'm not sure how to respond to that. Could you rephrase?"
            await response_msg.update()

        # Handle interrupts (Human-in-the-Loop)
        if "__interrupt__" in result:
            interrupts = result["__interrupt__"]
            if interrupts:
                interrupt = interrupts[0]
                value = interrupt.value if hasattr(interrupt, "value") else interrupt

                # Handle different interrupt value structures
                action_requests = []
                if isinstance(value, dict):
                    action_requests = value.get("action_requests", [])
                elif isinstance(value, list):
                    action_requests = value

                # Create approval message
                approval_content = "**⚠️ APPROVAL REQUIRED**\n\n"
                for req in action_requests:
                    tool_name = (
                        req.get("tool")
                        or req.get("action")
                        or req.get("name")
                        or req.get("tool_call", {}).get("name")
                        or "unknown"
                    )
                    description = req.get("description", "Action pending approval")
                    approval_content += f"**Action:** {tool_name}\n**Description:** {description}\n\n"

                    tool_input = (
                        req.get("tool_input")
                        or req.get("args")
                        or req.get("tool_call", {}).get("args")
                    )
                    if tool_input:
                        approval_content += "**Parameters:**\n"
                        for key, val in tool_input.items():
                            approval_content += f"- {key}: {val}\n"

                # Create action buttons for approval
                actions = [
                    cl.Action(name="approve", value="approve", label="✅ Approve"),
                    cl.Action(name="reject", value="reject", label="❌ Reject"),
                ]

                await cl.Message(content=approval_content, actions=actions).send()

    except Exception as e:
        error_msg = f"⚠️ An error occurred: {str(e)}"
        response_msg.content = error_msg
        await response_msg.update()


@cl.action_callback("approve")
async def on_approve(action: cl.Action):
    """Handle approval action."""
    agent = cl.user_session.get("agent")
    thread_id = cl.user_session.get("thread_id")

    if not agent:
        await cl.Message(content="⚠️ Agent not initialized.").send()
        return

    config = {"configurable": {"thread_id": thread_id}}

    # Resume the agent with approval
    command_value = {"resume": "approved"}
    result = await agent.ainvoke(command_value, config=config)

    # Send confirmation
    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        await cl.Message(content=last_message.content).send()
    else:
        await cl.Message(content="✅ Action approved and executed.").send()

    # Remove the action buttons
    await action.remove()


@cl.action_callback("reject")
async def on_reject(action: cl.Action):
    """Handle rejection action."""
    await cl.Message(content="❌ Action rejected. How else can I help you?").send()

    # Remove the action buttons
    await action.remove()
