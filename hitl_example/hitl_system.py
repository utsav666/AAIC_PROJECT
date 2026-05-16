"""
Human in the Loop (HITL) with LangGraph
========================================
Two flows side-by-side:
  1. WITHOUT HITL — LLM generates SQL → auto-executes (dangerous)
  2. WITH HITL    — LLM generates SQL → human reviews → then executes

Requirements:
  pip install langgraph langchain-openai python-dotenv
  Set OPENAI_API_KEY in .env or environment
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ─── Shared State ────────────────────────────────────────────────────────────

class State(TypedDict):
    user_question: str
    generated_sql: str
    human_decision: str        # "approve" | "reject" | "edit"
    final_sql: str
    result: str


# ─── Nodes (Steps) ───────────────────────────────────────────────────────────

def generate_sql(state: State) -> dict:
    """LLM generates SQL from natural language."""
    prompt = (
        f"Convert this question to a SQL query. "
        f"Return ONLY the SQL, nothing else.\n\n"
        f"Question: {state['user_question']}"
    )
    response = llm.invoke(prompt)
    sql = response.content.strip().strip("```sql").strip("```").strip()
    print(f"  🤖 LLM generated: {sql}")
    return {"generated_sql": sql}


def human_review(state: State) -> dict:
    """Pause execution and ask a human to review the SQL."""
    # This is LangGraph's built-in HITL mechanism —
    # it suspends the graph and waits for human input
    decision = interrupt({
        "message": "Please review this SQL before execution",
        "sql": state["generated_sql"],
        "options": "Type: 'approve', 'reject', or the corrected SQL",
    })

    if decision.lower() == "approve":
        return {"human_decision": "approve", "final_sql": state["generated_sql"]}
    elif decision.lower() == "reject":
        return {"human_decision": "reject", "final_sql": ""}
    else:
        # Human provided corrected SQL
        return {"human_decision": "edit", "final_sql": decision}


def execute_sql(state: State) -> dict:
    """Simulate executing the final SQL."""
    sql = state.get("final_sql") or state.get("generated_sql", "")
    if not sql:
        return {"result": "⛔ No SQL to execute (rejected by human)."}
    print(f"  ⚡ Executing: {sql}")
    # In real life: run against your DB here
    return {"result": f"✅ Executed successfully: {sql}"}


def should_execute(state: State) -> Literal["execute_sql", "__end__"]:
    """Route: skip execution if human rejected."""
    if state.get("human_decision") == "reject":
        print("  🚫 Human rejected — skipping execution.")
        return "__end__"
    return "execute_sql"


# ═══════════════════════════════════════════════════════════════════════════════
# FLOW 1: WITHOUT HITL — LLM → Execute (no human check)
# ═══════════════════════════════════════════════════════════════════════════════

def build_no_hitl_graph():
    g = StateGraph(State)
    g.add_node("generate_sql", generate_sql)
    g.add_node("execute_sql", execute_sql)
    g.add_edge(START, "generate_sql")
    g.add_edge("generate_sql", "execute_sql")
    g.add_edge("execute_sql", END)
    return g.compile()


# ═══════════════════════════════════════════════════════════════════════════════
# FLOW 2: WITH HITL — LLM → Human Review → Execute
# ═══════════════════════════════════════════════════════════════════════════════

def build_hitl_graph():
    g = StateGraph(State)
    g.add_node("generate_sql", generate_sql)
    g.add_node("human_review", human_review)
    g.add_node("execute_sql", execute_sql)
    g.add_edge(START, "generate_sql")
    g.add_edge("generate_sql", "human_review")
    g.add_conditional_edges("human_review", should_execute)
    g.add_edge("execute_sql", END)
    # MemorySaver is required for interrupt() to work
    return g.compile(checkpointer=MemorySaver())


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    question = "Delete all users who haven't logged in for 2 years"

    # ── WITHOUT HITL ──────────────────────────────────────────────────────
    print("=" * 65)
    print("❌ WITHOUT HITL — LLM output goes straight to execution")
    print("=" * 65)

    no_hitl = build_no_hitl_graph()
    result = no_hitl.invoke({"user_question": question})
    print(f"  Result: {result['result']}\n")

    # ── WITH HITL ─────────────────────────────────────────────────────────
    print("=" * 65)
    print("✅ WITH HITL — Human reviews before execution")
    print("=" * 65)

    hitl = build_hitl_graph()
    config = {"configurable": {"thread_id": "demo-1"}}

    # Step 1: Run until the graph hits interrupt()
    hitl.invoke({"user_question": question}, config)

    # Step 2: Show what the interrupt returned
    pending = hitl.get_state(config)
    interrupts = pending.tasks
    for task in interrupts:
        if hasattr(task, "interrupts") and task.interrupts:
            info = task.interrupts[0].value
            print(f"\n  🧑 HUMAN REVIEW NEEDED:")
            print(f"     SQL: {info['sql']}")
            print(f"     {info['options']}")

    # Step 3: Get human input and resume
    human_input = input("\n  Your decision: ").strip()

    # Resume the graph with the human's response
    result = hitl.invoke(Command(resume=human_input), config)
    print(f"\n  Result: {result['result']}")

    print("\n" + "=" * 65)
    print("KEY DIFFERENCE:")
    print("  Without HITL → LLM's DELETE runs immediately, no safety check")
    print("  With HITL    → Graph PAUSES, human reviews, then continues")
    print("=" * 65)
