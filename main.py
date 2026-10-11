"""
main.py
Customer Support chatbot: triage, specialists, guardrail,
manager approval for big refunds, and memory.
Type 'exit' to quit.
"""

import asyncio
from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered
from triage_agent import triage_agent

MAX_TURNS = 8


def ask_manager(item) -> bool:
    """Ask the human manager to approve or reject a waiting tool call."""
    print("\n🔔 MANAGER APPROVAL NEEDED")
    print("   Tool:", item.name)
    print("   Details:", item.arguments)
    answer = input("   Approve? (y/n): ").strip().lower()
    return answer in ("y", "yes")


async def handle_message(message: str, session: SQLiteSession):
    """Run one customer message, including any approval pauses."""
    result = await Runner.run(triage_agent, message, session=session, max_turns=MAX_TURNS)

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
        # Continue the same run, with the same memory
        result = await Runner.run(triage_agent, state, session=session, max_turns=MAX_TURNS)

    return result


async def main():
    session = SQLiteSession("customer_1", "support.db")

    print("=" * 55)
    print("  🛍️  Customer Support Assistant  (type 'exit' to quit)")
    print("=" * 55)

    while True:
        message = input("\nYou: ").strip()
        if not message:
            continue
        if message.lower() in ("exit", "quit"):
            print("Bot: Thank you for contacting us. Goodbye! 👋")
            break

        try:
            result = await handle_message(message, session)
            print(f"Bot [{result.last_agent.name}]: {result.final_output}")

        except InputGuardrailTripwireTriggered:
            print("Bot: Sorry, I can only help with orders, refunds, login and shop questions.")

        except Exception as error:
            text = str(error)
            if "429" in text:
                print("Bot: The AI service is busy or the daily limit was reached. Please try again later.")
            else:
                print(f"Bot: Sorry, something went wrong: {text[:150]}")


if __name__ == "__main__":
    asyncio.run(main())