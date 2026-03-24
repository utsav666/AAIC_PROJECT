from open_ai_client import get_client, get_model
from collections import Counter

# ---------------------------
# SINGLE PASS (PUREST FORM)
# ---------------------------
def single_pass(question):
    client = get_client()
    MODEL = get_model()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


# ---------------------------
# MULTI-SAMPLE (SELF-CONSISTENCY WITHOUT PROMPTING)
# ---------------------------
def multi_sample(question, k=5):
    client = get_client()
    MODEL = get_model()

    outputs = []

    for _ in range(k):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
            temperature=0.8
        )

        outputs.append(response.choices[0].message.content.strip())

    return outputs


# ---------------------------
# MAJORITY VOTE
# ---------------------------
def majority_vote(outputs):
    # Use full outputs (no extraction, no forcing)
    counter = Counter(outputs)
    best, freq = counter.most_common(1)[0]

    confidence = freq / len(outputs)

    return {
        "answer": best,
        "confidence": round(confidence, 2),
        "all_outputs": outputs
    }


# ---------------------------
# MAIN
# ---------------------------
def cot_without_prompting_solver(question, k=5):
    
    outputs = multi_sample(question, k=k)

    result = majority_vote(outputs)

    return result


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    q = "A bat and a ball cost 1.10 total. The bat costs 1 dollar more than the ball. How much does the ball cost?"

    result = cot_without_prompting_solver(q, k=5)

    print("\n=== RESULT ===")
    print(result)