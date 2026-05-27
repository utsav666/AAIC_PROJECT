"""
Phase 3 Prompts - Learning & Exam Generation
=============================================
Prompts for LLM to generate practice activities and module exams.
"""

# =============================================================================
# PRACTICE ACTIVITY GENERATION
# =============================================================================
PRACTICE_SYSTEM_PROMPT = """You are a friendly, encouraging dyslexia learning tutor for children.
You generate interactive practice activities that are:
- Age-appropriate and engaging
- Multi-sensory (visual descriptions, sound cues, patterns)
- Scaffolded with hints built in
- Celebrating effort, not just correctness

You MUST respond with valid JSON only."""

PRACTICE_USER_TEMPLATE = """Generate a practice activity for:
- Child Name: {child_name}
- Child Age: {child_age}
- Dyslexia Level: {level}
- Module: {module_name}
- Module Description: {module_description}
- Skills to practice: {skills}
- Activity Number: {activity_number} of 3

Generate ONE engaging activity. Respond with this JSON format:
{{
    "title": "<fun activity title with emoji>",
    "instruction": "<clear, simple instruction for the child>",
    "type": "multiple_choice" or "text_input" or "matching",
    "content": {{
        "question": "<the main question or task>",
        "options": ["<option1>", "<option2>", "<option3>", "<option4>"],
        "correct_answer": "<the correct answer>",
        "hint": "<a helpful hint>",
        "explanation": "<why this answer is correct - educational>"
    }},
    "encouragement": "<fun encouragement message>"
}}

Make it fun and appropriate for a {child_age}-year-old! Use emojis!"""


# =============================================================================
# MODULE EXAM GENERATION
# =============================================================================
EXAM_SYSTEM_PROMPT = """You are a dyslexia assessment specialist creating module exams.
Generate exam questions that:
- Test the specific skills of the module
- Are fair and age-appropriate
- Have clear, unambiguous correct answers
- Cover different aspects of the module
- Do NOT give hints (this is an exam, not practice)

You MUST respond with valid JSON only."""

EXAM_USER_TEMPLATE = """Generate a module exam for:
- Child Name: {child_name}
- Child Age: {child_age}
- Dyslexia Level: {level}
- Module: {module_name}
- Module Description: {module_description}
- Exam Focus: {exam_focus}
- Skills tested: {skills}

Generate exactly 5 exam questions. Respond with this JSON:
{{
    "exam_title": "<Module Name> Exam",
    "total_questions": 5,
    "pass_score": 3,
    "questions": [
        {{
            "id": 1,
            "question": "<clear exam question>",
            "type": "multiple_choice" or "text_input",
            "options": ["<opt1>", "<opt2>", "<opt3>", "<opt4>"],
            "correct_answer": "<exact correct answer>",
            "skill_tested": "<which skill this tests>"
        }},
        ...
    ]
}}

Make questions appropriate for a {child_age}-year-old at dyslexia level {level}.
No hints. Clear right/wrong answers."""


# =============================================================================
# EXAM EVALUATION
# =============================================================================
EVAL_SYSTEM_PROMPT = """You are a dyslexia specialist evaluating a child's exam responses.
Be generous with partial credit — if the child's answer shows understanding even with spelling errors, 
consider it correct (dyslexic children may know the answer but misspell it).

You MUST respond with valid JSON only."""

EVAL_USER_TEMPLATE = """Evaluate this module exam for:
- Child: {child_name}, Age: {child_age}
- Level: {level}, Module: {module_name}
- Pass threshold: 3 out of 5 correct

Exam responses:
{responses_text}

Evaluate each answer (be generous with spelling variations for dyslexic children).
Respond with this JSON:
{{
    "total_correct": <number 0-5>,
    "passed": true/false,
    "score_percentage": <0-100>,
    "question_results": [
        {{
            "id": 1,
            "correct": true/false,
            "child_answer": "<what they answered>",
            "expected": "<correct answer>",
            "feedback": "<brief encouraging feedback>"
        }},
        ...
    ],
    "overall_feedback": "<2-3 sentence encouraging summary>",
    "weak_areas": ["<area needing more practice>"],
    "strong_areas": ["<area child did well in>"]
}}"""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def build_practice_prompt(child_name: str, child_age: int, level: int,
                          module: dict, activity_number: int) -> str:
    """Build prompt for generating a practice activity."""
    return PRACTICE_USER_TEMPLATE.format(
        child_name=child_name,
        child_age=child_age,
        level=level,
        module_name=module["name"],
        module_description=module["description"],
        skills=", ".join(module["skills"]),
        activity_number=activity_number,
    )


def build_exam_prompt(child_name: str, child_age: int, level: int, module: dict) -> str:
    """Build prompt for generating a module exam."""
    return EXAM_USER_TEMPLATE.format(
        child_name=child_name,
        child_age=child_age,
        level=level,
        module_name=module["name"],
        module_description=module["description"],
        exam_focus=module["exam_focus"],
        skills=", ".join(module["skills"]),
    )


def build_eval_prompt(child_name: str, child_age: int, level: int,
                      module_name: str, responses: list[dict]) -> str:
    """Build prompt for evaluating exam responses."""
    responses_text = ""
    for r in responses:
        responses_text += f"\nQ{r['id']}: {r['question']}\n"
        responses_text += f"  Correct Answer: {r['correct_answer']}\n"
        responses_text += f"  Child's Answer: {r['child_answer']}\n"

    return EVAL_USER_TEMPLATE.format(
        child_name=child_name,
        child_age=child_age,
        level=level,
        module_name=module_name,
        responses_text=responses_text,
    )
