"""
Pattern: Supervisor Agent (true multi-agent)
Scenario: Customer support — a supervisor LLM dynamically routes
incoming tickets to specialist SUB-AGENTS (not plain functions).
Each sub-agent has its own persona, prompt, and tools.

The supervisor:
  1. Looks at the ticket
  2. Picks which specialist agent should handle it
  3. Sends the ticket to that agent
  4. Reads the agent's response
  5. Decides: is the ticket resolved, or should another agent handle it?
  6. Repeats until resolved or max rounds hit
"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from llm_client import get_llm

llm = get_llm()


# =============================================
# SUB-AGENT 1: Billing specialist
# Has its own persona, prompt, and tool
# =============================================

@tool
def lookup_invoice(customer_name: str) -> str:
    """Look up a customer's latest invoice."""
    invoices = {
        "priya": "Invoice #1042 — $120 — paid on Aug 10",
        "rahul": "Invoice #1089 — $250 — overdue since Jul 15",
    }
    return invoices.get(customer_name.lower(), "No invoice found.")


def billing_agent(ticket: str) -> str:
    """Billing specialist: answers billing/invoice/payment questions."""
    agent_llm = llm.bind_tools([lookup_invoice])
    messages = [HumanMessage(content=(
        "You are a billing specialist. Use lookup_invoice to find real data. "
        "Answer the customer's billing question.\n\n"
        f"Ticket: {ticket}"
    ))]

    response = agent_llm.invoke(messages)
    messages.append(response)

    for call in response.tool_calls or []:
        result = lookup_invoice.invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    if response.tool_calls:
        response = agent_llm.invoke(messages)

    return response.content


# =============================================
# SUB-AGENT 2: Technical support specialist
# Has its own persona, prompt, and tool
# =============================================

@tool
def check_system_status(service_name: str) -> str:
    """Check if an internal service is currently up or down."""
    statuses = {
        "email": "operational",
        "vpn": "degraded — known issue since 9am",
        "crm": "operational",
    }
    return statuses.get(service_name.lower(), "Unknown service.")


def tech_support_agent(ticket: str) -> str:
    """Tech support specialist: answers IT/system/access questions."""
    agent_llm = llm.bind_tools([check_system_status])
    messages = [HumanMessage(content=(
        "You are a tech support specialist. Use check_system_status to check services. "
        "Answer the customer's technical question.\n\n"
        f"Ticket: {ticket}"
    ))]

    response = agent_llm.invoke(messages)
    messages.append(response)

    for call in response.tool_calls or []:
        result = check_system_status.invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    if response.tool_calls:
        response = agent_llm.invoke(messages)

    return response.content


# =============================================
# SUPERVISOR: routes tickets to sub-agents
# It does NOT do the work — only decides who does
# =============================================

AGENTS = {
    "billing": billing_agent,
    "tech_support": tech_support_agent,
}

MAX_ROUNDS = 4


def run_supervisor(ticket: str):
    history = ""

    for round_num in range(1, MAX_ROUNDS + 1):
        # Supervisor decides which agent should handle this
        decision_prompt = f"""
You are a support supervisor. You do NOT answer tickets yourself.
You decide which specialist should handle the ticket.

Available specialists: billing, tech_support
Reply with EXACTLY one of:
- "billing" if it's about invoices, payments, charges
- "tech_support" if it's about system access, VPN, email, IT issues
- "DONE" if the ticket has already been fully resolved below

Ticket: {ticket}
History: {history if history else "none yet"}
"""
        decision = llm.invoke(decision_prompt).content.strip().lower()
        print(f"\n--- Round {round_num} ---")
        print(f"Supervisor decision: {decision}")

        if "done" in decision:
            print("Supervisor: ticket resolved.")
            return

        agent_fn = AGENTS.get(decision)
        if not agent_fn:
            print(f"Unknown agent '{decision}', defaulting to tech_support.")
            agent_fn = tech_support_agent

        # Delegate to the chosen sub-agent
        agent_response = agent_fn(ticket)
        print(f"{decision} agent response:\n  {agent_response}")

        history += f"\n[{decision} agent]: {agent_response}"

    print("\nMax rounds reached. Escalating to human support.")


# =============================================
# RUN
# =============================================
if __name__ == "__main__":
    print("=== Ticket 1: Billing question ===")
    run_supervisor("Rahul wants to know why his invoice is overdue.")

    print("\n\n=== Ticket 2: Tech question ===")
    run_supervisor("VPN is not connecting for the last 2 hours.")

    print("\n\n=== Ticket 3: Mixed question ===")
    run_supervisor("Can you check my invoice and also is the email server down?")
