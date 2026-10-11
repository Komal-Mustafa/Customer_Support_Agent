"""
test_approval.py
Small refunds go through automatically; big refunds need manager approval.
"""

import time
from agents import Runner, InputGuardrailTripwireTriggered
from triage_agent import triage_agent


def ask_manager(item) -> bool:
    """Show the waiting tool call and ask the manager for a decision."""
    print("\n🔔 MANAGER APPROVAL NEEDED")
    print("Tool:", item.name)
    print("Details:", item.arguments)
    answer = input("Approve this refund? (y/n): ").strip().lower()
    return answer in ("y", "yes")


def run_with_approval(question: str):
    result = Runner.run_sync(triage_agent, question, max_turns=8)

    # Keep going while there are tool calls waiting for approval
    while result.interruptions:
        state = result.to_state()
        for item in result.interruptions:
            if ask_manager(item):
                state.approve(item)
            else:
                state.reject(
                    item,
                    rejection_message=(
                        "A manager did not approve this refund. "
                        "Politely tell the customer their refund needs further review."
                    ),
                )
        # Continue the SAME run from where it paused
        result = Runner.run_sync(triage_agent, state, max_turns=8)

    return result


questions = [
    "I want a refund for ORD-1001, the size is wrong",           # Rs 4,500 -> automatic
    "I want a refund for ORD-1006, the watch stopped working",   # Rs 25,000 -> needs approval
]

for q in questions:
    print("\nCUSTOMER:", q)
    try:
        result = run_with_approval(q)
        print("ANSWERED BY:", result.last_agent.name)
        print("REPLY:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("BLOCKED: Sorry, I can only help with orders, refunds, login and shop questions.")
    print("-" * 50)
    time.sleep(5)