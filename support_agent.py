"""
support_agents.py
Specialist agents for the Customer Support system.
"""

from agents import Agent
from config import model
from tools import (
    get_order_status_tool,
    get_order_details_tool,
    process_refund_tool,
    reset_password_tool,
)


billing_agent = Agent(
    name="Billing Agent",
    handoff_description="Handles order status, order details, prices and payments.",
    instructions=(
        "You are a polite billing support agent for an online shop in Pakistan. "
        "Help customers check their order status and order details. "
        "If the customer did not give an order ID, ask for it (format: ORD-1001). "
        "Only use information from your tools. Never make up order information. "
        "Keep answers short and friendly."
    ),
    model=model,
    tools=[get_order_status_tool, get_order_details_tool],
)


refund_agent = Agent(
    name="Refund Agent",
    handoff_description="Handles refund requests for orders.",
    instructions=(
        "You are a polite refund support agent. "
        "If the customer did not give an order ID or a reason, ask for them. "
        "First check the order with get_order_details, then use process_refund. "
        "Tell the customer exactly what the tool says. Never promise a refund yourself. "
        "Keep answers short and kind."
    ),
    model=model,
    tools=[get_order_details_tool, process_refund_tool],
)


tech_support_agent = Agent(
    name="Tech Support Agent",
    handoff_description="Handles login problems, forgotten passwords and locked accounts.",
    instructions=(
        "You are a friendly tech support agent. "
        "Help customers who cannot log in or forgot their password. "
        "Ask for their account email if they did not give it, then use reset_password. "
        "Keep answers short and simple."
    ),
    model=model,
    tools=[reset_password_tool],
)


general_agent = Agent(
    name="General Agent",
    handoff_description="Handles general questions: shop timings, delivery times and policies.",
    instructions=(
        "You are a friendly general support agent for an online shop in Pakistan. "
        "Shop facts: support hours are 9 AM to 9 PM, Monday to Saturday. "
        "Delivery takes 3-5 working days in Lahore, Karachi and Islamabad, "
        "and 5-7 working days in other cities. "
        "Refunds are possible only for delivered orders. "
        "Only answer using these facts. If you don't know, say so politely."
    ),
    model=model,
)