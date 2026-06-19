"""Audio-visual content mapped to career paths."""

# Each career has: intro video (YouTube embed), description, icon
CAREER_MEDIA = {
    "software engineer": {
        "icon": "💻",
        "video": "https://www.youtube.com/watch?v=Uo3cL4nrGOk",
        "tagline": "Build the future, one line of code at a time.",
        "day_in_life": "You start your day with a standup meeting, then dive into solving complex problems with code. You collaborate with designers and product managers to build products used by millions.",
    },
    "doctor": {
        "icon": "🩺",
        "video": "https://www.youtube.com/watch?v=wnGPDGMOmso",
        "tagline": "Heal lives. Every single day matters.",
        "day_in_life": "Early rounds at the hospital, diagnosing patients, consulting with specialists. Every case is a puzzle. You combine science with empathy to make people better.",
    },
    "designer": {
        "icon": "🎨",
        "video": "https://www.youtube.com/watch?v=wOrmr7J7NY4",
        "tagline": "Make the world more beautiful and usable.",
        "day_in_life": "You sketch ideas, create wireframes, test prototypes. Your work shapes how millions of people experience apps, products, and spaces.",
    },
    "entrepreneur": {
        "icon": "🚀",
        "video": "https://www.youtube.com/watch?v=ZoqgAy3h4OM",
        "tagline": "See problems. Build solutions. Create jobs.",
        "day_in_life": "No two days are the same. Pitching to investors, building your team, talking to customers, iterating on your product. High risk, high reward.",
    },
    "scientist": {
        "icon": "🔬",
        "video": "https://www.youtube.com/watch?v=HJ9bE3aTnik",
        "tagline": "Discover what nobody else has found yet.",
        "day_in_life": "Design experiments, analyze data, publish research. You push the boundaries of human knowledge in labs, observatories, or field stations.",
    },
    "teacher": {
        "icon": "📚",
        "video": "https://www.youtube.com/watch?v=SFnMTHhKdkw",
        "tagline": "Shape minds. Change generations.",
        "day_in_life": "Prepare lessons that spark curiosity, mentor students, adapt your teaching to each student's needs. You see the lightbulb moment daily.",
    },
    "filmmaker": {
        "icon": "🎬",
        "video": "https://www.youtube.com/watch?v=GxKj_CmtGXI",
        "tagline": "Tell stories that move the world.",
        "day_in_life": "Scriptwriting, directing actors, editing footage. You combine visual storytelling with emotion to create experiences that stay with people forever.",
    },
    "data scientist": {
        "icon": "📊",
        "video": "https://www.youtube.com/watch?v=X3paOmcrTjQ",
        "tagline": "Turn data into decisions that matter.",
        "day_in_life": "Explore datasets, build models, present insights. You help companies and governments make smarter choices using patterns hidden in numbers.",
    },
    "lawyer": {
        "icon": "⚖️",
        "video": "https://www.youtube.com/watch?v=q2ohBEfuF_s",
        "tagline": "Fight for justice. Protect the truth.",
        "day_in_life": "Research cases, argue in court, advise clients. You use logic, language, and law to make sure fairness prevails.",
    },
    "architect": {
        "icon": "🏛️",
        "video": "https://www.youtube.com/watch?v=JEyMfURvPWM",
        "tagline": "Design the spaces where life happens.",
        "day_in_life": "Sketch building designs, work with engineers, visit construction sites. You blend art and science to create functional, beautiful structures.",
    },
    "psychologist": {
        "icon": "🧠",
        "video": "https://www.youtube.com/watch?v=vo4pMVb0R6M",
        "tagline": "Understand minds. Help people heal.",
        "day_in_life": "Counsel individuals, run therapy sessions, conduct research on human behavior. You help people understand themselves and overcome challenges.",
    },
    "journalist": {
        "icon": "📰",
        "video": "https://www.youtube.com/watch?v=5FUz5GzEfcQ",
        "tagline": "Uncover truth. Tell stories that matter.",
        "day_in_life": "Chase stories, interview people, write articles. You keep the public informed and hold powerful people accountable.",
    },
}

# Fallback for careers not in the bank
DEFAULT_MEDIA = {
    "icon": "🌟",
    "video": "",
    "tagline": "Every great career starts with a single step.",
    "day_in_life": "Explore, learn, and grow into the professional you're meant to be.",
}


def get_career_media(career_name: str) -> dict:
    """Get media content for a career. Fuzzy matches on career name."""
    career_lower = career_name.lower()
    for key, media in CAREER_MEDIA.items():
        if key in career_lower or career_lower in key:
            return media
    return DEFAULT_MEDIA
