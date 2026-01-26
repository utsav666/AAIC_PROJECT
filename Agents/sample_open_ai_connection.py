import os
import openai
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Load variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")

# Use the key with OpenAI
openai.api_key = api_key

# Example call
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)