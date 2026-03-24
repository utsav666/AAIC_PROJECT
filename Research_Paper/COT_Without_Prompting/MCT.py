import math
from open_ai_client import get_client, get_model

class Node:
    def __init__(self, text, parent=None):
        self.text = text
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def ucb(self, c=1.4):
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + c * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )


def expand(node, question):
    prompt = f"Question: {question}\nAnswer so far: {node.text}\nContinue."

    client = get_client()
    MODEL = get_model()

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    child = Node(res.choices[0].message.content.strip(), parent=node)
    node.children.append(child)
    return child


def evaluate(node, question):
    prompt = f"""
Question: {question}
Answer: {node.text}

Score correctness from 0 to 1.
Only return number.
"""

    client = get_client()
    MODEL = get_model()

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        return float(res.choices[0].message.content.strip())
    except:
        return 0.5


def backpropagate(node, reward):
    while node:
        node.visits += 1
        node.value += reward
        node = node.parent


def select(node):
    while node.children:
        node = max(node.children, key=lambda n: n.ucb())
    return node


def mcts(question, iterations=20):
    root = Node("")

    for _ in range(iterations):
        node = select(root)
        child = expand(node, question)
        reward = evaluate(child, question)
        backpropagate(child, reward)

    best = max(root.children, key=lambda n: n.visits)

    confidence = best.value / best.visits if best.visits > 0 else 0

    return {
        "answer": best.text,
        "confidence": confidence
    }