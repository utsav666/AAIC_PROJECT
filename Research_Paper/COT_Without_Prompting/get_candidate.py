import re
from collections import Counter
from statistics import mean
from openai import OpenAI
from dotenv import load_dotenv
import os
from open_ai_client import get_client,get_model

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

client = get_client()

MODEL = get_model()

def generate_candidates(question, k=5):
    prompt = f"""
Solve the following problem multiple times independently.

Question: {question}

Return {k} answers only:
1.
2.
3.
...
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    lines = res.choices[0].message.content.split("\n")
    answers = [re.sub(r"^\d+\.\s*", "", l).strip() for l in lines if l.strip()]

    return answers[:k]