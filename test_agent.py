from agents import Runner
from support_agent import billing_agent, refund_agent, tech_support_agent, general_agent

result = Runner.run_sync(billing_agent, "Where is my order ORD-1002?", max_turns=5)
print("BILLING:", result.final_output)