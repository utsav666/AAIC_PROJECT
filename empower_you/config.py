"""Configuration for Empower You platform."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# LLM Provider: "openai", "azure_openai", "claude", "claude_merck"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

STANDARDS = ["8th", "9th", "10th", "11th", "12th"]

HOBBY_OPTIONS = [
    "Drawing / Painting", "Coding / Computers", "Sports / Athletics",
    "Music / Singing", "Reading / Writing", "Science Experiments",
    "Public Speaking / Debate", "Gaming", "Cooking / Baking",
    "Photography / Filmmaking", "Dancing", "Volunteering / Social Work",
    "Gardening / Nature", "Building / Fixing Things", "Business / Selling",
]

CAREER_DIMENSIONS = [
    "thinking_style",    # analytical / creative / social / practical
    "energy_source",     # people / ideas / things / data
    "core_driver",       # impact / mastery / freedom / security / expression
    "risk_profile",      # explorer / builder / maintainer
    "environment_fit",   # structured / flexible / solo / collaborative
    "domain_attraction", # tech / health / arts / business / nature / service
]
