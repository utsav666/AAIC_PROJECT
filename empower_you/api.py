"""API service layer. All business logic goes through here.
Can be converted to FastAPI endpoints later with minimal changes."""

import re
from questions import get_all_questions, get_question_by_id, get_showcase_tasks
from career_engine import extract_signals, predict_career
from media import get_career_media
from config import STANDARDS, HOBBY_OPTIONS


# ─── User Info ───

def get_form_options() -> dict:
    """Return options for the user info form."""
    return {
        "standards": STANDARDS,
        "hobbies": HOBBY_OPTIONS,
    }


def validate_user_info(name: str, standard: str, hobbies: list) -> tuple:
    """Validate user input. Returns (is_valid, error_message)."""
    if not name or len(name.strip()) < 2:
        return False, "Please enter your name (at least 2 characters)."
    if standard not in STANDARDS:
        return False, "Please select a valid standard."
    if len(hobbies) < 1:
        return False, "Please select at least 1 hobby."
    return True, ""


# ─── Questions ───

def get_questions() -> list:
    """Return all psychometric questions."""
    return get_all_questions()


def get_question(question_id: str) -> dict:
    """Return a single question."""
    return get_question_by_id(question_id)


def get_showcase_for_hobbies(hobbies: list) -> list:
    """Return audio-visual showcase tasks matching student's hobbies."""
    return get_showcase_tasks(hobbies)


# ─── Career Prediction ───

def evaluate_career(user_info: dict, answers: dict) -> dict:
    """Main API: takes user info + answers, returns career prediction + media."""
    questions = get_all_questions()

    # Step 1: Extract signals from answers
    signals = extract_signals(answers, questions)

    # Step 2: Get AI career prediction (include text answers for richer analysis)
    prediction_text = predict_career(user_info, signals, answers, questions)

    # Step 3: Parse career names from prediction
    career_names = _parse_career_names(prediction_text)

    # Step 4: Get media for each career
    media = {name: get_career_media(name) for name in career_names}

    return {
        "prediction": prediction_text,
        "careers": career_names,
        "media": media,
        "signals": signals,
    }


def _parse_career_names(prediction_text: str) -> list:
    """Extract career names from LLM output."""
    names = []
    for line in prediction_text.split("\n"):
        if line.strip().startswith("CAREER"):
            match = re.search(r"CAREER \d+:\s*(.+)", line)
            if match:
                names.append(match.group(1).strip())
    return names
