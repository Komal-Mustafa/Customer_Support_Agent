"""
test_guardrail.py
Checks that off-topic questions are blocked and normal ones still work.
"""

import time
from agents import Runner, InputGuardrailTripwireTriggered
from triage_agent import triage_agent

questions = [
    "Where is my order ORD-1003?",            # should pass
    "Can you solve 2x + 5 = 15 for me?",      # should be blocked
    "Write me a poem about cricket",          # should be blocked
    "Hello, I need help with my order",       # should pass
]

for q in questions:
    print("CUSTOMER:", q)
    try:
        result = Runner.run_sync(triage_agent, q, max_turns=6)
        print("ANSWERED BY:", result.last_agent.name)
        print("REPLY:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("BLOCKED: Sorry, I can only help with orders, refunds, login and shop questions.")
    print("-" * 50)
    time.sleep(5)