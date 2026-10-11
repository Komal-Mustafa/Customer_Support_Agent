"""
test_triage.py
Checks that the Triage Agent sends each question to the right specialist.
"""

import time
from agents import Runner
from triage_agent import triage_agent

questions = [
    "Where is my order ORD-1002?",
    "I want a refund for ORD-1006, the watch stopped working",
    "I forgot my password, my email is bilal@example.com",
    "What are your support hours?",
]

for q in questions:
    result = Runner.run_sync(triage_agent, q, max_turns=6)
    print("CUSTOMER:", q)
    print("ANSWERED BY:", result.last_agent.name)
    print("REPLY:", result.final_output)
    print("-" * 50)
    time.sleep(5)  # small pause to protect the free quota