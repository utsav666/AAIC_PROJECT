import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from langchain.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
#, DuckDuckGoSearchRun
from duckduckgo_search import DDGS
from langchain_experimental.tools import PythonREPLTool

# LangGraph imports
from langgraph.graph import StateGraph, END
from typing import TypedDict

# ------------------------
# ENV + LLM
# ------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
search_api = os.getenv('SEARCH_KEY')
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=api_key)

# ------------------------
# TOOLS
# ------------------------
wiki = WikipediaAPIWrapper()
#search = DuckDuckGoSearchRun()
#search = DDGS()
search = TavilySearchResults(max_results=3,search_depth='advanced',
                                max_tokens=10000)
python_tool = PythonREPLTool()

@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for information on a given topic."""
    return wiki.run(query)

@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information."""

    return search.run(query)


@tool
def currency_converter(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency using simple exchange rates (mock for demo)."""
    rates = {"USD": 83.0, "EUR": 90.0, "INR": 1.0}
    if from_currency not in rates or to_currency not in rates:
        return "Currency not supported."
    converted = amount * (rates[to_currency] / rates[from_currency])
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"

@tool
def noop_tool(dummy_input: str) -> str:
    """Dummy tool required to initialize agent"""
    return "No action needed."


# ------------------------
# AGENTS
# ------------------------

# Research Agent
research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research agent. Use Wikipedia and web search to gather facts and citations."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
research_agent = create_openai_functions_agent(llm, [wikipedia_search,web_search], research_prompt)
research_executor = AgentExecutor(agent=research_agent, tools=[wikipedia_search,web_search], verbose=True)

# Data Analyst Agent
analyst_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a data analyst. Use Python to analyze trends, compute statistics, and simulate projections."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
analyst_agent = create_openai_functions_agent(llm, [python_tool], analyst_prompt)
analyst_executor = AgentExecutor(agent=analyst_agent, tools=[python_tool], verbose=True)

# Finance Agent
finance_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a financial analyst. Provide economic and market impact assessments."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
finance_agent = create_openai_functions_agent(llm, [currency_converter], finance_prompt)
finance_executor = AgentExecutor(agent=finance_agent, tools=[currency_converter], verbose=True)

# Policy Advisor Agent
policy_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a policy advisor. Suggest government and regulatory recommendations."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
policy_agent = create_openai_functions_agent(llm, [noop_tool], policy_prompt)
policy_executor = AgentExecutor(agent=policy_agent, tools=[noop_tool], verbose=True)

# Writer Agent
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a report writer. Write a structured report with Introduction, Analysis, Financial Impact, Policy Recommendations, and Conclusion."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
writer_agent = create_openai_functions_agent(llm, [noop_tool], writer_prompt)
writer_executor = AgentExecutor(agent=writer_agent, tools=[noop_tool], verbose=True)


###AGENT STATE 


# ------------------------
# STATE DEFINITION
# ------------------------
class AgentState(TypedDict):
    query: str
    research: str
    analysis: str
    finance: str
    policy: str
    report: str


# ------------------------
# NODES (functions)
# ------------------------
def run_research(state: AgentState):
    output = research_executor.invoke({"input": state["query"]})
    state["research"] = output["output"]
    return state


def run_analysis(state: AgentState):
    output = analyst_executor.invoke({"input": f"Provide data analysis for: {state['query']}"})
    state["analysis"] = output["output"]
    return state


def run_finance(state: AgentState):
    output = finance_executor.invoke({"input": f"Provide financial/economic analysis for: {state['query']}"})
    state["finance"] = output["output"]
    return state


def run_policy(state: AgentState):
    output = policy_executor.invoke({"input": f"Provide policy recommendations for: {state['query']}"})
    state["policy"] = output["output"]
    return state


def run_writer(state: AgentState):
    final_input = f"""
    Research Findings: {state['research']}
    Data Insights: {state['analysis']}
    Financial Analysis: {state['finance']}
    Policy Recommendations: {state['policy']}
    Write a full structured report.
    """
    output = writer_executor.invoke({"input": final_input})
    state["report"] = output["output"]
    return state


#------------------------
# Decision Agent
#------------------------
from langchain.prompts import PromptTemplate

decision_prompt = PromptTemplate.from_template(
    """
    You are a classifier.
    Decide if the following query requires FINANCIAL analysis.
    Answer only with 'finance' or 'policy'.

    Query: {query}
    """
)

def should_run_finance(state: AgentState) -> str:
    query = state["query"]
    decision_chain = decision_prompt | llm
    result = decision_chain.invoke({"query": query})
    answer = result.content.strip().lower()
    print(answer,".....ANS....")
    if "finance" in answer:
        return "finance"
    return "policy"


# ------------------------
# ORCHESTRATOR FLOW
# ------------------------
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("research_node", run_research)
graph.add_node("analysis_node", run_analysis)
graph.add_node("finance_node", run_finance)
graph.add_node("policy_node", run_policy)
graph.add_node("writer_node", run_writer)

# Entry point
graph.set_entry_point("research_node")

# Standard flow
graph.add_edge("research_node", "analysis_node")

# Conditional edge after analysis
graph.add_conditional_edges(
    "analysis_node",
    should_run_finance,  # function that decides
    {
        "finance": "finance_node",  # if true → go to finance
        "policy": "policy_node"     # if false → skip finance
    }
)

# Normal continuation
#graph.add_edge("finance_node", "policy_node")
graph.add_edge("finance_node", "writer_node")
graph.add_edge("policy_node", "writer_node")
graph.add_edge("writer_node", END)

# Compile app
app = graph.compile()

# ------------------------
# RUN EXAMPLE
# ------------------------
if __name__ == "__main__":
    query = "what is the policy of adopting diesel vehicle ?"
    inputs = {"query": query}
    result = app.invoke(inputs)
    print("\n📝 Final Report:\n", result["report"])
