from open_ai_client import get_model,get_client

def reflect_and_improve(question, answer):
    prompt = f"""
Question: {question}
Proposed Answer: {answer}

Check if this is correct. If wrong, fix it.
Return ONLY final answer.
"""
    client = get_client()
    MODEL = get_model()
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()