"""
Pattern: Generator -> Critic (Reflection)
Scenario: Draft a customer refund-rejection email. A critic runs a
deterministic policy-check TOOL (not just an LLM opinion) plus an LLM
review before the draft is considered final.
"""

from langchain_core.tools import tool
from llm_client import get_llm

llm = get_llm(temperature=0.3)

request = "Write an email rejecting a refund request because the return window (30 days) has expired."

POLICY_RULES = """
Rules the email MUST follow:
1. Must not promise a refund or exception.
2. Must not blame the customer.
3. Must offer one alternative (store credit or discount on next order).
"""

MAX_ATTEMPTS = 3
BANNED_PHRASES = ["we will refund", "exception", "your fault", "you should have"]


@tool
def check_banned_phrases(draft: str) -> str:
    """Scan a draft email for banned phrases that violate refund policy."""
    hits = [p for p in BANNED_PHRASES if p in draft.lower()]
    return f"violations: {hits}" if hits else "no banned phrases found"


def generate(feedback: str = "") -> str:
    prompt = request
    if feedback:
        prompt += f"\n\nRevise based on this feedback:\n{feedback}"
    return llm.invoke(prompt).content


def critique(draft: str) -> str:
    tool_result = check_banned_phrases.invoke({"draft": draft})
    prompt = f"""
    {POLICY_RULES}

    Draft email:
    {draft}

    Automated phrase-check tool result: {tool_result}

    Combine the tool result with your own review.
    Reply with exactly "APPROVED" if no violations,
    otherwise reply with a short list of violations to fix.
    """
    return llm.invoke(prompt).content.strip()


draft = generate()
for attempt in range(1, MAX_ATTEMPTS + 1):
    verdict = critique(draft)
    print(f"\nAttempt {attempt} draft:\n{draft}")
    print(f"\nCritic verdict: {verdict}")

    if verdict.upper().startswith("APPROVED"):
        print("\nFINAL APPROVED EMAIL:\n", draft)
        break

    draft = generate(feedback=verdict)
else:
    print("\nMax attempts reached without approval. Escalating to human review.")
