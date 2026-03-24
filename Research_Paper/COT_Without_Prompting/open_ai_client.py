from dotenv import load_dotenv
import os
import openai
from openai import OpenAI

load_dotenv()
MODEL = "gpt-3.5-turbo"
def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    #print(api_key)
    client = OpenAI(api_key=api_key)
    return client
def get_model():
    return MODEL
