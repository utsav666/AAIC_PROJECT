"""
Pattern: Planner -> Executor
Scenario: User wants a short trip budget summary.
The planner LLM breaks the goal into steps (structured list).
The executor runs each step using real tools (price lookups), not free text.
"""

import json
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from llm_client import get_llm

llm = get_llm()

goal = "Plan a 3-day trip budget for Goa for 2 people"


# ---- Tools the executor can call ----
@tool
def get_flight_price(destination: str) -> str:
    """Get round-trip flight price per person to a destination (mocked)."""
    prices = {"goa": 6500, "paris": 45000, "dubai": 22000}
    return f"{prices.get(destination.lower(), 8000)} INR per person"


@tool
def get_hotel_price(destination: str, nights: int) -> str:
    """Get total hotel cost for a destination and number of nights (mocked)."""
    per_night = {"goa": 3000, "paris": 12000, "dubai": 9000}
    total = per_night.get(destination.lower(), 4000) * nights
    return f"{total} INR total for {nights} nights"


tools = [get_flight_price, get_hotel_price]
tool_map = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)


def run_step(step_text: str) -> str:
    """Executor: let the LLM call tools if needed to complete one planned step."""
    messages = [HumanMessage(content=f"Do this step, use tools if it needs real numbers: {step_text}")]
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    for call in response.tool_calls or []:
        result = tool_map[call["name"]].invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    if response.tool_calls:
        response = llm_with_tools.invoke(messages)

    return response.content


# ---- Planner: produce a structured plan ----
planner_prompt = f"""
Break the following goal into 3-5 short, concrete steps.
Include at least one step about flight cost and one about hotel cost.
Return ONLY a JSON list of strings, nothing else.

Goal: {goal}
"""
plan_response = llm.invoke(planner_prompt).content
plan = json.loads(plan_response)

print("PLAN:")
for i, step in enumerate(plan, 1):
    print(f"  {i}. {step}")

# ---- Executor: run each planned step, calling tools as needed ----
results = [run_step(step) for step in plan]

print("\nEXECUTION RESULTS:")
for step, result in zip(plan, results):
    print(f"\n- {step}\n  -> {result}")

# ---- Final synthesis ----
final = llm.invoke(
    "Combine these step results into one short trip budget summary:\n" + "\n".join(results)
).content
print("\nFINAL SUMMARY:\n", final)
