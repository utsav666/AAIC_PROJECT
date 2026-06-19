# 🚀 Empower You

**AI-Powered Career Guidance Platform for 8th–12th Standard Students**

Discover your perfect career path through scenario-based psychometric assessment, audio-visual showcases, and AI-powered career matching.

---

## What It Does

- Phase 1: Student fills profile (name, class, hobbies)
- Phase 2: Hybrid questions (MCQ, sliders, open text, rankings) — no direct aptitude testing
- Phase 3: Audio-visual showcase uploads (video/audio/image based on hobbies)
- Phase 4: AI predicts top 3 career paths with day-in-life videos
- Phase 5: Analytics report with charts and personality breakdown

---

## AI Architecture (Full Product Vision)

### Where Each AI Pattern Fits

| Pattern | Where It Fits | Why |
|---------|--------------|-----|
| **Simple LLM call** | Current prototype | Single-turn, no memory needed |
| **RAG** | Career data, college info, exam paths, scholarships | Need real, specific, searchable data |
| **Agents** | Adaptive questioning, profile building, career matching | Need reasoning, memory, tool use, multi-step |
| **Multi-Agent** | Full orchestration across phases | Each phase needs a specialist agent |
| **Fine-tuning** | Later — when you have outcome data | Improve accuracy with real student success stories |

### Agent Architecture

```
┌─────────────────────────────────────────────┐
│           Orchestrator Agent                 │
│  (routes to the right sub-agent per phase)  │
├──────────┬──────────┬───────────┬───────────┤
│ Question │ Profile  │  Career   │  Mentor   │
│  Agent   │  Agent   │  Agent    │  Agent    │
└──────────┴──────────┴───────────┴───────────┘
```

| Agent | Role |
|-------|------|
| **Adaptive Question Agent** | Decides what to ask next based on previous answers, generates follow-ups dynamically |
| **Profile Builder Agent** | Continuously builds student's psychometric profile across sessions |
| **Career Matching Agent** | Matches profile → careers using reasoning + tools (search career DB, check eligibility) |
| **Mentor Matching Agent** | Finds right mentor based on student profile + availability |
| **Parent Report Agent** | Generates personalized parent-facing reports in their language |

### RAG — The Knowledge Layer

| RAG Use Case | What's in the Vector DB |
|-------------|------------------------|
| **Career Knowledge Base** | 500+ career descriptions, salary ranges, Indian-specific paths, required exams (JEE/NEET/CLAT/NDA/CA) |
| **College & Course DB** | Colleges, cutoffs, courses, fees — searchable by career path |
| **Exam Roadmaps** | "If you're in 10th and want to be a doctor → here's the exact path" |
| **Mentor Profiles** | Professional backgrounds, expertise, availability |
| **Success Stories** | Real stories of people who took each path |
| **Scholarship DB** | Available scholarships matched to student profile |

### How RAG + Agents Work Together

```
Student answers questions
    → Profile Agent builds profile
    → Career Agent queries RAG: "careers matching {analytical + tech + explorer}"
    → RAG returns top 10 relevant careers with real data
    → Agent reasons over them + student context → picks top 3
    → Roadmap Agent queries RAG: "path from 10th standard to Data Scientist"
    → Returns specific steps (stream choice, exams, colleges)
```

### Additional AI Layers for World-Class

| AI Layer | Technology | Purpose |
|----------|-----------|---------|
| **Vision AI** | GPT-4V / Gemini Vision | Analyze uploaded art, screenshots, design work |
| **Speech AI** | Whisper + custom scoring | Analyze singing, speaking uploads |
| **Video AI** | Video understanding models | Analyze dance, sports clips for skill signals |
| **Recommendation Engine** | Collaborative filtering + LLM | "Students like you also explored..." |
| **Continuous Learning** | Fine-tuned model on outcomes | Improve predictions based on actual career success data |
| **Multilingual** | Translation + TTS | Hindi, Tamil, etc. voice guidance |

### Production Tech Stack

```
Agents:        LangGraph / CrewAI / Autogen
RAG:           LangChain + Pinecone/Weaviate (vector DB)
Embeddings:    OpenAI ada-002 or Cohere
Orchestration: LangGraph (stateful, handles multi-turn adaptive flow)
Media AI:      GPT-4V (images), Whisper (audio), Twelve Labs (video)
Cache:         Redis (session state between agent calls)
DB:            PostgreSQL (user profiles) + Vector DB (career knowledge)
Frontend:      Next.js 14 + React + Framer Motion
Mobile:        React Native / Flutter
```

---

## Current Status

✅ Working Streamlit prototype with:
- Hybrid question engine (MCQ + sliders + text + rankings)
- Flexible LLM provider (OpenAI / Azure / Claude / Merck proxy)
- Audio-visual showcase uploads
- AI career prediction
- Analytics charts in final report

---

## License

Internal project — not for distribution.
