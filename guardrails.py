"""
guardrails.py
Input guardrail that blocks questions not related to customer support.
"""
from guardrails import off_topic_guardrail
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from config import model


# 1. The answer shape the checker must return
class TopicCheck(BaseModel):
    is_off_topic: bool
    reason: str


# 2. A small checker agent
topic_checker = Agent(
    name="Topic Checker",
    instructions=(
        "You check if a customer's message is related to an online shop's customer support. "
        "On-topic: orders, order status, delivery, prices, payments, refunds, "
        "login or password problems, shop hours and policies, and simple greetings. "
        "Off-topic: homework, coding, general knowledge, jokes, essays, or anything else. "
        "Set is_off_topic to true only if the message is clearly off-topic."
    ),
    model=model,
    output_type=TopicCheck,
)


# 3. The guardrail function
@input_guardrail(run_in_parallel=False)
async def off_topic_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(topic_checker, input, context=ctx.context)
    check = result.final_output
    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=check.is_off_topic,
    )