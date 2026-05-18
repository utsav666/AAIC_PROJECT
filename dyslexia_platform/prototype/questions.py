"""
Assessment Questions Bank
=========================
Age-appropriate questions for dyslexia screening.
"""

# Each question has: question text, type, expected answer, dimension it tests
QUESTIONS_AGE_5_7 = [
    {
        "question": "Which word rhymes with 'cat'? Options: dog, bat, cup",
        "type": "multiple_choice",
        "options": ["dog", "bat", "cup"],
        "expected": "bat",
        "dimension": "phonemic_awareness",
        "hint": "🎵 Which word sounds like 'cat' at the end?",
    },
    {
        "question": "Type the letter you see: **b**",
        "type": "text_input",
        "expected": "b",
        "dimension": "letter_recognition",
        "hint": "Look carefully at which way the bump faces!",
    },
    {
        "question": "Spell the word for this: 🐱 (a small furry pet that says meow)",
        "type": "text_input",
        "expected": "cat",
        "dimension": "reading_spelling",
        "hint": "It starts with a 'k' sound...",
    },
    {
        "question": "Read this sentence: 'The dog ran fast.' — What did the dog do?",
        "type": "text_input",
        "expected": "ran fast",
        "dimension": "comprehension",
        "hint": "What action word tells you what the dog did?",
    },
    {
        "question": "Which word looks different? Options: bad, bad, dad, bad",
        "type": "multiple_choice",
        "options": ["bad (1st)", "bad (2nd)", "dad (3rd)", "bad (4th)"],
        "expected": "dad (3rd)",
        "dimension": "visual_processing",
        "hint": "Look very carefully at each letter in every word!",
    },
]

QUESTIONS_AGE_8_10 = [
    {
        "question": "Say these sounds separately: 'splash' → How many sounds? List them.",
        "type": "text_input",
        "expected": "s-p-l-a-sh (5 sounds)",
        "dimension": "phonemic_awareness",
        "hint": "Try to break the word into individual sounds, not letters.",
    },
    {
        "question": "Which of these is the letter 'd'? Options: b, d, p, q",
        "type": "multiple_choice",
        "options": ["b", "d", "p", "q"],
        "expected": "d",
        "dimension": "letter_recognition",
        "hint": "Think: 'd' has the stick on the right side.",
    },
    {
        "question": "Spell the word: 'something you use to write on paper' ✏️",
        "type": "text_input",
        "expected": "pencil",
        "dimension": "reading_spelling",
        "hint": "It starts with 'pen...'",
    },
    {
        "question": "Read: 'The blue bird flew over the tall tree and landed on the roof.' — Where did the bird land?",
        "type": "text_input",
        "expected": "on the roof",
        "dimension": "comprehension",
        "hint": "Read the end of the sentence carefully.",
    },
    {
        "question": "Which word is spelled correctly? Options: becuase, because, becasue, becouse",
        "type": "multiple_choice",
        "options": ["becuase", "because", "becasue", "becouse"],
        "expected": "because",
        "dimension": "visual_processing",
        "hint": "Sound it out: be-cause.",
    },
    {
        "question": "What word do you get if you remove the 'b' from 'blend'?",
        "type": "text_input",
        "expected": "lend",
        "dimension": "phonemic_awareness",
        "hint": "Just take away the first sound!",
    },
]

QUESTIONS_AGE_11_PLUS = [
    {
        "question": "Rearrange these sounds to make a word: /k/ /a/ /t/ /s/",
        "type": "text_input",
        "expected": "cats",
        "dimension": "phonemic_awareness",
        "hint": "Put the sounds together in order.",
    },
    {
        "question": "Spell: 'the opposite of remember'",
        "type": "text_input",
        "expected": "forget",
        "dimension": "reading_spelling",
        "hint": "for + get = ?",
    },
    {
        "question": "Read: 'Despite the heavy rain, the determined hikers continued up the mountain trail.' — What word best describes the hikers?",
        "type": "text_input",
        "expected": "determined",
        "dimension": "comprehension",
        "hint": "Look for the word that tells you about their attitude.",
    },
    {
        "question": "Which is correct? Options: necessary, neccessary, necesary, neccesary",
        "type": "multiple_choice",
        "options": ["necessary", "neccessary", "necesary", "neccesary"],
        "expected": "necessary",
        "dimension": "visual_processing",
        "hint": "One 'c', two 's's.",
    },
    {
        "question": "If 'un-' means 'not', what does 'uncomfortable' mean?",
        "type": "text_input",
        "expected": "not comfortable",
        "dimension": "phonemic_awareness",
        "hint": "Break it apart: un + comfortable.",
    },
]


def get_questions_for_age(age: int) -> list[dict]:
    """Return appropriate question set based on child's age."""
    if age <= 7:
        return QUESTIONS_AGE_5_7
    elif age <= 10:
        return QUESTIONS_AGE_8_10
    else:
        return QUESTIONS_AGE_11_PLUS
