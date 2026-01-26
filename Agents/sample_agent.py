import os
import openai
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from langchain.utilities import WikipediaAPIWrapper
wiki = WikipediaAPIWrapper()

# Load variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")

# Use the key with OpenAI
openai.api_key = api_key

# Define custom system instructions
system_message = """You are a helpful travel assistant.
You can use tools like Wikipedia, Currency Converter, and Weather.
Always explain your reasoning step by step in simple words,
and when using tools, clearly include their results in your final answer."""

# Build a ChatPromptTemplate
custom_prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")  # scratchpad for tool calls
])
# # Example call
# response = openai.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": "Hello!"}]
# )

# print(response.choices[0].message.content)

#####TOOL CREATION#######
@tool
def wikipedia_search(query: str) -> str:
    """Search for information on Wikipedia about a travel destination."""
    return wiki.run(query)

@tool
def currency_converter(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency using a fixed rate (for demo purposes).Please calaculate it correctly"""
    rates = {"USD": 83.0, "EUR": 90.0, "INR": 1.0}  # mock rates
    if from_currency not in rates or to_currency not in rates:
        return "Currency not supported."
    converted = amount * (rates[to_currency] / rates[from_currency])
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"

@tool
def get_weather(city: str) -> str:
    """Get today's weather for a city (mocked)."""
    fake_weather = {
        "Paris": "Sunny, 25°C",
        "London": "Rainy, 18°C",
        "New Delhi": "Hot, 34°C"
    }
    return fake_weather.get(city, "Weather data not available")

# Define LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# List of tools
tools = [wikipedia_search, currency_converter, get_weather]

# Create agent with tool-calling ability
agent = create_openai_functions_agent(llm, tools,custom_prompt)

# Wrap in executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example 1: Info about a city
#print(agent_executor.invoke({"input": "Tell me about Paris"}))

# # Example 2: Convert money
# print(agent_executor.invoke({"input": "Convert 100 USD to INR"}))

# # Example 3: Get weather
# print(agent_executor.invoke({"input": "What is the weather in London today?"}))

# # Example 4: Multi-step
print(agent_executor.invoke({"input": "I'm planning a trip to New Delhi. Tell me about it and also convert 200 USD to INR"}))
