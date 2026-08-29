"""
Pattern: Parallel fan-out / fan-in
Scenario: Research a company from three independent angles at the
same time, each branch using its own TOOL (financial lookup, product
lookup, news search), then merge into one summary. Independent
branches run concurrently instead of one after another.
"""

from concurrent.futures import ThreadPoolExecutor
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from llm_client import get_llm

llm = get_llm()

company = "Tesla"


@tool
def get_financials(company_name: str) -> str:
    """Get mocked recent financial figures for a company."""
    return f"{company_name} Q2 revenue: $25.5B, up 6% YoY."


@tool
def get_product_news(company_name: str) -> str:
    """Get mocked recent product highlights for a company."""
    return f"{company_name} shipped a new battery pack with 20% more range."


@tool
def get_general_news(company_name: str) -> str:
    """Get mocked recent general news headlines for a company."""
    return f"{company_name} announced a new factory location in Q2."


branches = {
    "financial": ("Summarize the company's financials.", get_financials),
    "product": ("Summarize the company's product highlights.", get_product_news),
    "news": ("Summarize recent news about the company.", get_general_news),
}


def run_branch(name_branch):
    name, (instruction, tool_fn) = name_branch
    llm_with_tool = llm.bind_tools([tool_fn])
    messages = [HumanMessage(content=f"{instruction} Company: {company}. Use the available tool.")]
    response = llm_with_tool.invoke(messages)
    messages.append(response)

    for call in response.tool_calls or []:
        result = tool_fn.invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    if response.tool_calls:
        response = llm_with_tool.invoke(messages)

    return name, response.content


# ---- Fan-out: run all branches concurrently, each calling its own tool ----
with ThreadPoolExecutor(max_workers=len(branches)) as pool:
    results = dict(pool.map(run_branch, branches.items()))

print("BRANCH RESULTS:")
for name, output in results.items():
    print(f"\n[{name}]\n{output}")

# ---- Fan-in: merge results into one summary ----
merged_input = "\n\n".join(f"{name.upper()}:\n{output}" for name, output in results.items())
final_summary = llm.invoke(
    f"Combine the following research into one short company profile:\n\n{merged_input}"
).content

print("\nFINAL MERGED SUMMARY:\n", final_summary)
