"""
Pattern: Human-in-the-loop approval gate
Scenario: Agent looks up an order via a TOOL, drafts a refund action,
but the workflow pauses and requires explicit human approval before
calling the execute_refund TOOL.
"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from llm_client import get_llm

llm = get_llm()

FAKE_ORDERS = {
    "priya": {"order_amount": 45, "item": "wireless mouse"},
}


@tool
def lookup_order(customer_name: str) -> str:
    """Look up a customer's order amount and item by name."""
    order = FAKE_ORDERS.get(customer_name.lower())
    return str(order) if order else "No order found."


def draft_refund(request: str) -> dict:
    llm_with_tool = llm.bind_tools([lookup_order])
    prompt = f"""
    Based on this request, use the lookup_order tool to find the order,
    then propose a refund action.
    Reply in this exact format at the end:
    customer: <name>
    amount: <amount in USD>
    reason: <short reason>

    Request: {request}
    """
    messages = [HumanMessage(content=prompt)]
    response = llm_with_tool.invoke(messages)
    messages.append(response)

    for call in response.tool_calls or []:
        result = lookup_order.invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    if response.tool_calls:
        response = llm_with_tool.invoke(messages)

    text = response.content
    fields = dict(line.split(": ", 1) for line in text.strip().splitlines() if ": " in line)
    return fields


@tool
def execute_refund(customer: str, amount: str) -> str:
    """Execute the refund for a customer (placeholder for a real refund API call)."""
    return f"Refunded {amount} to {customer}."


def request_human_approval(action: dict) -> bool:
    print("\nPROPOSED ACTION (requires approval):")
    for key, value in action.items():
        print(f"  {key}: {value}")
    answer = input("Approve this refund? (yes/no): ").strip().lower()
    return answer == "yes"


if __name__ == "__main__":
    customer_request = "Customer Priya says the product arrived broken and wants $45 back."

    action = draft_refund(customer_request)

    if request_human_approval(action):
        outcome = execute_refund.invoke({"customer": action["customer"], "amount": action["amount"]})
        print(f"\nEXECUTED: {outcome}")
    else:
        print("\nRefund NOT executed. Sent back for revision or manual handling.")
