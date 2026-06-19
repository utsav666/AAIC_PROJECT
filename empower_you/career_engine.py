"""Career prediction engine. Uses signals from answers + hobbies to recommend paths."""

import llm

SYSTEM_PROMPT = """You are a world-class career counselor for Indian students in 8th-12th standard.

You will receive:
1. Student's profile (name, standard, hobbies)
2. Their psychometric signals (extracted from scenario-based questions)

Your job:
- Analyze their thinking style, interests, values, and strengths
- Recommend exactly 3 career paths (ranked by fit)
- For each path, give: career name, why it fits them, what to do next
- Be specific to the Indian education system (streams, exams, colleges)
- Be encouraging, warm, and realistic
- Speak directly to the student using their name

Output format (strictly follow):
CAREER 1: [Career Name]
WHY: [2-3 sentences why this fits]
NEXT STEPS: [What to do from their current standard]

CAREER 2: [Career Name]
WHY: [2-3 sentences]
NEXT STEPS: [What to do]

CAREER 3: [Career Name]
WHY: [2-3 sentences]
NEXT STEPS: [What to do]

SUMMARY: [A warm, encouraging 2-3 line summary for the student]"""


def build_profile_text(user_info: dict, signals: dict, answers: dict = None, questions: list = None) -> str:
    """Convert user info and signals into a readable prompt."""
    lines = [
        f"Student Name: {user_info['name']}",
        f"Standard: {user_info['standard']}",
        f"Hobbies: {', '.join(user_info['hobbies'])}",
        "",
        "Psychometric Signals:",
    ]
    for dimension, values in signals.items():
        top = max(values, key=values.get)
        lines.append(f"  {dimension}: {top} (score: {values[top]})")

    # Include open text answers for richer AI analysis
    if answers and questions:
        text_answers = []
        for q in questions:
            if q.get("input_type") == "text" and q["id"] in answers:
                text_answers.append(f"  Q: {q['title']} → \"{answers[q['id']]}\"")
        if text_answers:
            lines.append("")
            lines.append("Open Responses:")
            lines.extend(text_answers)

    return "\n".join(lines)


def extract_signals(answers: dict, questions: list) -> dict:
    """Extract career dimension signals from all question types."""
    signals = {}

    def _add_signal(dim, value, weight=1):
        if dim.endswith("_alt"):
            dim = dim.replace("_alt", "")
        if dim not in signals:
            signals[dim] = {}
        signals[dim][value] = signals[dim].get(value, 0) + weight

    for q in questions:
        qid = q["id"]
        if qid not in answers:
            continue

        input_type = q.get("input_type", "mcq")
        answer = answers[qid]

        if input_type == "mcq":
            # Standard multiple choice
            for option in q["options"]:
                if option["key"] == answer:
                    for dim, value in option["signals"].items():
                        _add_signal(dim, value)
                    break

        elif input_type == "slider":
            # Slider returns 1-5: 1-2 = left, 4-5 = right, 3 = neutral
            val = int(answer)
            if val <= 2:
                for dim, value in q["left_signals"].items():
                    _add_signal(dim, value, weight=(3 - val))
            elif val >= 4:
                for dim, value in q["right_signals"].items():
                    _add_signal(dim, value, weight=(val - 2))

        elif input_type == "ranking":
            # Ranking: top items get more weight
            ranked = answer  # list of keys in order
            for rank, key in enumerate(ranked):
                weight = len(q["items"]) - rank  # top = highest weight
                for item in q["items"]:
                    if item["key"] == key:
                        for dim, value in item["signals"].items():
                            _add_signal(dim, value, weight=weight)
                        break

        elif input_type == "text":
            # Text answers stored as-is, passed to LLM for analysis
            pass

    return signals


def predict_career(user_info: dict, signals: dict, answers: dict = None, questions: list = None) -> str:
    """Call LLM to predict career paths."""
    profile_text = build_profile_text(user_info, signals, answers, questions)
    return llm.chat(SYSTEM_PROMPT, profile_text)
