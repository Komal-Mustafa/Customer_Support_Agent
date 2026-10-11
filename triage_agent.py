"""
triage_agent.py
The Triage Agent: first point of contact.
It never answers questions itself; it only hands off to the right specialist.
"""

from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from config import model
from support_agent import billing_agent, refund_agent, tech_support_agent, general_agent


triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are the first point of contact for customer support. "
        "Your only job is to understand the customer's question and hand off "
        "to the right specialist. Do NOT answer questions yourself.\n"
        "- Order status, order details, prices, payments -> Billing Agent\n"
        "- Refund requests -> Refund Agent\n"
        "- Login problems, passwords, locked accounts -> Tech Support Agent\n"
        "- Shop hours, delivery times, policies, anything else -> General Agent"
    ),
    model=model,
    handoffs=[billing_agent, refund_agent, tech_support_agent, general_agent],
)