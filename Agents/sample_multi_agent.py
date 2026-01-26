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

# ------------------------
# ORCHESTRATOR FLOW
# ------------------------

def multi_agent_system(query: str):
    print(f"\n🔍 User Query: {query}")

    # Step 1: Research
    research_output = research_executor.invoke({"input": query})
    print("\n📑 Research Output:\n", research_output["output"])

    # Step 2: Data Analysis
    analysis_output = analyst_executor.invoke({"input": f"Provide data analysis for: {query}"})
    print("\n📊 Analyst Output:\n", analysis_output["output"])

    # Step 3: Finance
    finance_output = finance_executor.invoke({"input": f"Provide financial/economic analysis for: {query}"})
    print("\n💰 Finance Output:\n", finance_output["output"])

    # Step 4: Policy Advice
    policy_output = policy_executor.invoke({"input": f"Provide policy recommendations for: {query}"})
    print("\n🏛️ Policy Output:\n", policy_output["output"])

    # Step 5: Final Report
    final_input = f"""
    Research Findings: {research_output['output']}
    Data Insights: {analysis_output['output']}
    Financial Analysis: {finance_output['output']}
    Policy Recommendations: {policy_output['output']}
    Write a full structured report.
    """
    final_report = writer_executor.invoke({"input": final_input})
    print("\n📝 Final Report:\n", final_report["output"])

    return final_report["output"]

# ------------------------
# RUN EXAMPLE
# ------------------------
if __name__ == "__main__":
    query = "Create a policy report on the adoption of electric vehicles in India."
    report = multi_agent_system(query)
