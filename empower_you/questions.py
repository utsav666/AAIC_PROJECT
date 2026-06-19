"""Hybrid question bank — MCQ, sliders, open text, rankings, and media uploads.
input_type determines how each question renders in the UI."""

QUESTIONS = [
    # ─── MCQ Questions ───
    {
        "id": "q1",
        "input_type": "mcq",
        "title": "🏝️ The Island Challenge",
        "question": (
            "You're stranded on an island with 5 strangers. "
            "A storm is coming in 3 hours. What do you do FIRST?"
        ),
        "options": [
            {"key": "A", "text": "Start building shelter — you have a plan", "signals": {"thinking_style": "practical", "risk_profile": "builder"}},
            {"key": "B", "text": "Talk to everyone to understand their skills", "signals": {"thinking_style": "social", "energy_source": "people"}},
            {"key": "C", "text": "Explore the island to find the safest spot", "signals": {"thinking_style": "analytical", "risk_profile": "explorer"}},
            {"key": "D", "text": "Comfort the person who is panicking", "signals": {"thinking_style": "social", "core_driver": "impact"}},
            {"key": "E", "text": "Start mapping the island layout", "signals": {"thinking_style": "analytical", "energy_source": "data"}},
        ],
    },
    {
        "id": "q2",
        "input_type": "mcq",
        "title": "⚡ Your Superpower",
        "question": "A wizard gives you ONE superpower for your career. Pick one:",
        "options": [
            {"key": "A", "text": "🧠 Learn any skill in 1 day", "signals": {"core_driver": "mastery", "risk_profile": "explorer"}},
            {"key": "B", "text": "👁️ See what people need before they say it", "signals": {"core_driver": "impact", "energy_source": "people"}},
            {"key": "C", "text": "⚡ Build anything you imagine", "signals": {"core_driver": "expression", "thinking_style": "creative"}},
            {"key": "D", "text": "🗣️ Convince anyone of anything", "signals": {"energy_source": "people", "domain_attraction": "business"}},
            {"key": "E", "text": "🔮 Predict what will happen next year", "signals": {"thinking_style": "analytical", "energy_source": "data"}},
        ],
    },
    {
        "id": "q3",
        "input_type": "mcq",
        "title": "🍽️ Fix the Problem",
        "question": (
            "Your school canteen wastes 30kg of food daily. "
            "You're given full power to fix it. What's your FIRST move?"
        ),
        "options": [
            {"key": "A", "text": "Track the data — what food, when, why", "signals": {"thinking_style": "analytical", "energy_source": "data"}},
            {"key": "B", "text": "Talk to students — understand their eating habits", "signals": {"thinking_style": "social", "energy_source": "people"}},
            {"key": "C", "text": "Build a system — app to pre-order meals", "signals": {"thinking_style": "practical", "domain_attraction": "tech"}},
            {"key": "D", "text": "Start an awareness campaign — posters, assembly talk", "signals": {"thinking_style": "creative", "domain_attraction": "arts"}},
            {"key": "E", "text": "Partner with NGOs to redistribute excess food", "signals": {"core_driver": "impact", "domain_attraction": "service"}},
        ],
    },
    {
        "id": "q4",
        "input_type": "mcq",
        "title": "📰 Click First",
        "question": "Which news headline would you click FIRST?",
        "options": [
            {"key": "A", "text": "17-year-old builds app that saves 1000 trees", "signals": {"domain_attraction": "tech", "core_driver": "impact"}},
            {"key": "B", "text": "Indian athlete breaks world record at Olympics", "signals": {"domain_attraction": "sports", "core_driver": "mastery"}},
            {"key": "C", "text": "New AI can detect cancer 5 years early", "signals": {"domain_attraction": "health", "energy_source": "data"}},
            {"key": "D", "text": "Student's short film wins at Cannes", "signals": {"domain_attraction": "arts", "core_driver": "expression"}},
            {"key": "E", "text": "Teen starts ₹10 crore company from hostel room", "signals": {"domain_attraction": "business", "risk_profile": "explorer"}},
            {"key": "F", "text": "Volunteer group rebuilds flood-damaged village", "signals": {"domain_attraction": "service", "core_driver": "impact"}},
        ],
    },

    # ─── Slider Questions ───
    {
        "id": "q5",
        "input_type": "slider",
        "title": "💼 Money vs. Meaning",
        "question": "Slide toward what matters more to you:",
        "left_label": "💰 High salary, stable job",
        "right_label": "❤️ Meaningful work, daily excitement",
        "left_signals": {"core_driver": "security", "environment_fit": "structured"},
        "right_signals": {"core_driver": "impact", "core_driver_alt": "expression"},
    },
    {
        "id": "q6",
        "input_type": "slider",
        "title": "👥 Solo vs. Team",
        "question": "How do you prefer to work?",
        "left_label": "🧘 Alone, deep focus",
        "right_label": "🎉 With people, energy",
        "left_signals": {"environment_fit": "solo", "energy_source": "ideas"},
        "right_signals": {"environment_fit": "collaborative", "energy_source": "people"},
    },
    {
        "id": "q7",
        "input_type": "slider",
        "title": "🎯 Safe vs. Risky",
        "question": "Your comfort with risk:",
        "left_label": "🛡️ Stable, predictable path",
        "right_label": "🚀 Uncertain, high-reward adventure",
        "left_signals": {"risk_profile": "maintainer", "environment_fit": "structured"},
        "right_signals": {"risk_profile": "explorer", "core_driver": "freedom"},
    },

    # ─── Open Text Questions ───
    {
        "id": "q8",
        "input_type": "text",
        "title": "✍️ Complete the Story",
        "question": (
            "Complete this in 2-3 sentences:\n\n"
            "\"Riya was the first person from her village to ___. "
            "Everyone said it was impossible, but she ___. "
            "Ten years later, she ___.\""
        ),
        "placeholder": "Write your ending here...",
        "ai_analyze": True,  # LLM will analyze this response
    },
    {
        "id": "q9",
        "input_type": "text",
        "title": "💭 Your Dream Day",
        "question": "Describe your perfect work day 10 years from now. What are you doing? Where? With whom?",
        "placeholder": "I wake up and...",
        "ai_analyze": True,
    },

    # ─── Ranking Question ───
    {
        "id": "q10",
        "input_type": "ranking",
        "title": "🏆 What Matters Most",
        "question": "Rank these from MOST important (#1) to LEAST important (#5) for your future career:",
        "items": [
            {"key": "money", "text": "💰 Earning a lot of money", "signals": {"core_driver": "security"}},
            {"key": "fame", "text": "⭐ Being famous / recognized", "signals": {"core_driver": "expression"}},
            {"key": "impact", "text": "🌍 Making the world better", "signals": {"core_driver": "impact"}},
            {"key": "freedom", "text": "🕊️ Freedom to do what I want", "signals": {"core_driver": "freedom"}},
            {"key": "mastery", "text": "🧠 Becoming the best at something", "signals": {"core_driver": "mastery"}},
        ],
    },

    # ─── MCQ Visual/Reaction ───
    {
        "id": "q11",
        "input_type": "mcq",
        "title": "🏢 Your Dream Workspace",
        "question": "Pick the workspace you'd LOVE to be in every day:",
        "options": [
            {"key": "A", "text": "🔬 Quiet lab with microscopes", "signals": {"environment_fit": "solo", "domain_attraction": "health"}},
            {"key": "B", "text": "💻 Buzzing startup with whiteboards", "signals": {"environment_fit": "collaborative", "domain_attraction": "tech"}},
            {"key": "C", "text": "🌿 Outdoor field with notebook & camera", "signals": {"environment_fit": "flexible", "domain_attraction": "nature"}},
            {"key": "D", "text": "🎭 Stage with lights and audience", "signals": {"environment_fit": "collaborative", "domain_attraction": "arts"}},
            {"key": "E", "text": "🏠 Cozy home — my own schedule", "signals": {"environment_fit": "solo", "core_driver": "freedom"}},
        ],
    },
    {
        "id": "q12",
        "input_type": "mcq",
        "title": "🎬 Your Reaction",
        "question": (
            "A surgeon saves a child after a 10-hour operation. How do you feel?"
        ),
        "options": [
            {"key": "A", "text": "Fascinated — HOW did they do that?", "signals": {"thinking_style": "analytical", "core_driver": "mastery"}},
            {"key": "B", "text": "Inspired — I want to help like that", "signals": {"core_driver": "impact", "domain_attraction": "health"}},
            {"key": "C", "text": "Stressed — too much pressure", "signals": {"environment_fit": "flexible", "risk_profile": "maintainer"}},
            {"key": "D", "text": "Curious — I'd rather design the tools", "signals": {"thinking_style": "creative", "domain_attraction": "tech"}},
            {"key": "E", "text": "Moved — I'd tell this story to the world", "signals": {"core_driver": "expression", "domain_attraction": "arts"}},
        ],
    },
]

# ─── Audio-Visual Showcase Tasks (shown based on hobbies) ───
SHOWCASE_TASKS = {
    "Dancing": {
        "title": "💃 Show Us Your Moves!",
        "instruction": "Record a short video (15-60 seconds) of you dancing — any style!",
        "upload_type": "video",
        "signals": {"domain_attraction": "arts", "core_driver": "expression", "energy_source": "physical"},
    },
    "Music / Singing": {
        "title": "🎤 Let Us Hear You!",
        "instruction": "Record yourself singing or playing an instrument (15-60 seconds).",
        "upload_type": "audio",
        "signals": {"domain_attraction": "arts", "core_driver": "expression", "energy_source": "ideas"},
    },
    "Drawing / Painting": {
        "title": "🎨 Show Your Art!",
        "instruction": "Upload a photo of your best artwork — drawing, painting, digital art, anything!",
        "upload_type": "image",
        "signals": {"domain_attraction": "arts", "thinking_style": "creative", "core_driver": "expression"},
    },
    "Photography / Filmmaking": {
        "title": "📸 Your Best Shot!",
        "instruction": "Upload your best photo or a short clip you filmed (max 60 sec).",
        "upload_type": "video",
        "signals": {"domain_attraction": "arts", "thinking_style": "creative", "core_driver": "expression"},
    },
    "Public Speaking / Debate": {
        "title": "🗣️ Make Your Case!",
        "instruction": "Record a 30-60 second video arguing for or against: 'Social media does more harm than good.'",
        "upload_type": "video",
        "signals": {"energy_source": "people", "thinking_style": "social", "domain_attraction": "business"},
    },
    "Coding / Computers": {
        "title": "💻 Show Your Build!",
        "instruction": "Upload a screenshot or short screen-recording of something you built — app, game, website, anything!",
        "upload_type": "image",
        "signals": {"domain_attraction": "tech", "thinking_style": "analytical", "core_driver": "mastery"},
    },
    "Sports / Athletics": {
        "title": "⚽ Your Best Moment!",
        "instruction": "Record a short clip (15-60 sec) of you playing your sport or doing a skill move.",
        "upload_type": "video",
        "signals": {"domain_attraction": "sports", "core_driver": "mastery", "energy_source": "physical"},
    },
    "Cooking / Baking": {
        "title": "🍳 Your Creation!",
        "instruction": "Upload a photo of something you cooked or baked — bonus if you record a quick process video!",
        "upload_type": "image",
        "signals": {"thinking_style": "creative", "thinking_style_alt": "practical", "core_driver": "expression"},
    },
}


def get_all_questions():
    """Return all questions."""
    return QUESTIONS


def get_question_by_id(question_id: str):
    """Return a single question by ID."""
    for q in QUESTIONS:
        if q["id"] == question_id:
            return q
    return None


def get_showcase_tasks(hobbies: list) -> list:
    """Return relevant showcase tasks based on student's hobbies."""
    tasks = []
    for hobby in hobbies:
        if hobby in SHOWCASE_TASKS:
            tasks.append(SHOWCASE_TASKS[hobby])
    return tasks

