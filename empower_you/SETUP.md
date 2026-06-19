# Empower You — Setup & Code Instructions

## Project Structure

```
empower_you/
├── app.py              # Streamlit UI (thin layer, 5 phases)
├── api.py              # API service layer (all logic routes through here)
├── llm.py              # Flexible LLM provider (OpenAI/Azure/Claude/Merck)
├── career_engine.py    # Signal extraction + AI career prediction
├── questions.py        # Hybrid question bank (MCQ, slider, text, ranking, showcases)
├── media.py            # Audio-visual content mapped to careers
├── config.py           # Configuration loader
├── .env                # API keys and provider config
├── requirements.txt    # Python dependencies
└── README.md           # Project overview
```

## Quick Start

### 1. Install Dependencies

```bash
cd empower_you
pip install -r requirements.txt
```

### 2. Configure `.env`

Copy `.env.example` to `.env` and fill in your API keys. See `.env` file for all supported providers.

### 3. Run the App

```bash
streamlit run app.py
```

Opens at: http://localhost:8501

---

## Code Design Principles

1. **API Separation** — `app.py` (UI) never touches `career_engine` or `llm` directly. Everything goes through `api.py`. This makes it easy to swap to FastAPI later.

2. **Single Responsibility** — Each file does one thing:
   - `questions.py` = question data
   - `career_engine.py` = signal extraction + LLM call
   - `llm.py` = LLM provider abstraction
   - `media.py` = career video/content mapping
   - `app.py` = UI rendering only

3. **Flexible LLM** — Switch providers by changing one line in `.env`. No code changes needed.

4. **No Aptitude Questions** — All questions are scenarios, superpowers, tradeoffs, reactions. AI extracts signals indirectly.

---

## How to Add More Questions

Edit `questions.py`. Each question needs:

**MCQ:**
```python
{
    "id": "q_new",
    "input_type": "mcq",
    "title": "🎯 Title",
    "question": "Your question text",
    "options": [
        {"key": "A", "text": "Option text", "signals": {"dimension": "value"}},
    ],
}
```

**Slider:**
```python
{
    "id": "q_new",
    "input_type": "slider",
    "title": "⚖️ Title",
    "question": "What to slide between",
    "left_label": "Left extreme",
    "right_label": "Right extreme",
    "left_signals": {"dimension": "value"},
    "right_signals": {"dimension": "value"},
}
```

**Open Text (AI-analyzed):**
```python
{
    "id": "q_new",
    "input_type": "text",
    "title": "✍️ Title",
    "question": "Open-ended question",
    "placeholder": "Hint text...",
    "ai_analyze": True,
}
```

**Ranking:**
```python
{
    "id": "q_new",
    "input_type": "ranking",
    "title": "🏆 Title",
    "question": "Rank these items",
    "items": [
        {"key": "item1", "text": "Display text", "signals": {"dimension": "value"}},
    ],
}
```

---

## How to Add More Careers (Media)

Edit `media.py`. Add an entry to `CAREER_MEDIA`:

```python
"career name in lowercase": {
    "icon": "🎯",
    "video": "https://www.youtube.com/watch?v=VIDEO_ID",
    "tagline": "One-liner about this career.",
    "day_in_life": "2-3 sentences describing a typical day.",
}
```

The matching is fuzzy — if the LLM returns "Software Engineer" and you have "software engineer" in the dict, it will match.

---

## How to Add Showcase Tasks

Edit `questions.py` → `SHOWCASE_TASKS` dict. Key must match a hobby from `config.py`:

```python
"Hobby Name": {
    "title": "🎬 Task Title",
    "instruction": "What to upload",
    "upload_type": "video",  # video, audio, or image
    "signals": {"dimension": "value"},
}
```

---

## Career Dimensions (Signal System)

All questions map to these 6 dimensions:

| Dimension | Possible Values |
|-----------|----------------|
| `thinking_style` | analytical, creative, social, practical |
| `energy_source` | people, ideas, things, data, physical |
| `core_driver` | impact, mastery, freedom, security, expression |
| `risk_profile` | explorer, builder, maintainer |
| `environment_fit` | structured, flexible, solo, collaborative |
| `domain_attraction` | tech, health, arts, business, nature, service, sports |

Each answer adds weight to one or more dimension values. The AI uses the strongest signals to recommend careers.

---

## Converting to FastAPI (Later)

`api.py` is designed to become FastAPI routes with minimal changes:

```python
# Current (called by Streamlit):
result = api.evaluate_career(user_info, answers)

# Future (FastAPI endpoint):
@app.post("/api/evaluate")
def evaluate(request: EvaluateRequest):
    return api.evaluate_career(request.user_info, request.answers)
```

No business logic changes needed — just add route decorators.
