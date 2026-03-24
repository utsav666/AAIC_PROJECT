from get_candidate import generate_candidates
from reflection import reflect_and_improve
from collections import Counter
from MCT import mcts
import re

# ---------------------------
# HELPERS
# ---------------------------
def extract_final_answer(text):
    match = re.search(r"\d*\.?\d+", text)
    return match.group(0) if match else text


def score_candidates(candidates):
    counter = Counter(candidates)
    
    scored = []
    for ans, freq in counter.items():
        prob = freq / len(candidates)
        scored.append((ans, prob))
    
    return sorted(scored, key=lambda x: x[1], reverse=True)


def is_collapsed(candidates):
    return len(set(candidates)) == 1


# ---------------------------
# MAIN PIPELINE
# ---------------------------
def prism_solver(question):
    
    # Step 1: Generate candidates
    candidates = generate_candidates(question, k=7)

    # Step 2: Score agreement
    scored = score_candidates(candidates)
    best_answer, agreement_score = scored[0]
    print(scored,".....scored......")
    # Step 3: Reflection
    improved = reflect_and_improve(question, best_answer)
    print(improved,".....improved before extrcat....")
    improved = extract_final_answer(improved)
    print(improved,"improved after extract......")

    # ---------------------------
    # Case 1: All same → easy
    # ---------------------------
    if is_collapsed(candidates):
        return {
            "answer": improved,
            "confidence": 1.0,
            "method": "consensus",
            "candidates": candidates
        }

    # ---------------------------
    # Case 2: Medium → no MCTS
    # ---------------------------
    if agreement_score >= 0.6:
        return {
            "answer": improved,
            "confidence": round(agreement_score, 2),
            "method": "self_consistency",
            "candidates": candidates
        }

    # ---------------------------
    # Case 3: Low agreement → MCTS
    # ---------------------------
    mcts_result = mcts(question, iterations=20)

    #final_answer = extract_final_answer(mcts_result["answer"])

    return {
        "answer": mcts_result['answer'],
        "confidence": round(mcts_result["confidence"], 2),
        "method": "mcts",
        "candidates": candidates
    }


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    #q = "A bat and a ball cost 1.10 total. The bat costs 1 dollar more than the ball. How much does the ball cost?"
    q = 'how much is -11 plus 11 ?'
    result = prism_solver(q)

    print("\n=== FINAL RESULT ===")
    print(result)