"""
NeuroLearn KIDS — FastAPI Backend
Run: cd AAIC_PROJECT/dyslexia_platform/prototype && uvicorn backend:app --reload --port 8000
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm_provider import get_llm
from prompts import ASSESSMENT_SYSTEM_PROMPT, build_assessment_prompt
from questions import get_questions_for_age
from video_bank import get_level_modules, get_module, get_total_modules
from phase3_prompts import (
    PRACTICE_SYSTEM_PROMPT,
    EXAM_SYSTEM_PROMPT,
    EVAL_SYSTEM_PROMPT,
    build_practice_prompt,
    build_exam_prompt,
    build_eval_prompt,
)

app = FastAPI(title="NeuroLearn KIDS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request models ─────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    parent_name: str
    parent_email: str = ""
    parent_mobile: str = ""
    password: str = ""
    child_name: str
    child_dob: str = ""
    child_age: int
    child_gender: str = ""
    grade: str = ""
    school: str = ""
    reading_level: str = ""
    concerns: str = ""
    previous_diagnosis: str = "No"
    user_role: str = "parent"


class AssessmentRequest(BaseModel):
    child_name: str
    child_age: int
    responses: list[dict]


class PracticeRequest(BaseModel):
    child_name: str
    child_age: int
    level: int
    module: dict
    practice_num: int


class ExamGenerateRequest(BaseModel):
    child_name: str
    child_age: int
    level: int
    module: dict


class ExamEvaluateRequest(BaseModel):
    child_name: str
    child_age: int
    level: int
    module_name: str
    responses: list[dict]


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/register")
def register(data: RegisterRequest) -> dict:
    """Validate and save registration. Returns session seed data."""
    return {
        "status": "ok",
        "child_name": data.child_name,
        "child_age": data.child_age,
        "user_role": data.user_role,
    }


@app.get("/api/questions/{age}")
def get_questions(age: int) -> dict:
    """Return age-appropriate assessment questions."""
    questions = get_questions_for_age(age)
    return {"questions": questions, "total": len(questions)}


@app.post("/api/assess")
def assess(data: AssessmentRequest) -> dict:
    """Run LLM-powered assessment on submitted question responses."""
    try:
        llm = get_llm()
        prompt = build_assessment_prompt(data.child_name, data.child_age, data.responses)
        return llm.chat_json(ASSESSMENT_SYSTEM_PROMPT, prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/modules/{level}")
def list_modules(level: int) -> dict:
    """Return all modules for a given dyslexia level (1–5)."""
    try:
        return {
            "level": level,
            "data": get_level_modules(level),
            "total": get_total_modules(level),
        }
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/module/{level}/{index}")
def get_module_detail(level: int, index: int) -> dict:
    """Return a single module with metadata."""
    try:
        return {
            "module": get_module(level, index),
            "total": get_total_modules(level),
            "index": index,
            "level_name": get_level_modules(level).get("name", ""),
        }
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/practice")
def generate_practice(data: PracticeRequest) -> dict:
    """Generate an LLM practice activity for a module."""
    try:
        llm = get_llm()
        prompt = build_practice_prompt(
            data.child_name, data.child_age, data.level, data.module, data.practice_num
        )
        return llm.chat_json(PRACTICE_SYSTEM_PROMPT, prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/exam/generate")
def generate_exam(data: ExamGenerateRequest) -> dict:
    """Generate exam questions for a module."""
    try:
        llm = get_llm()
        prompt = build_exam_prompt(data.child_name, data.child_age, data.level, data.module)
        return llm.chat_json(EXAM_SYSTEM_PROMPT, prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/exam/evaluate")
def evaluate_exam(data: ExamEvaluateRequest) -> dict:
    """Evaluate exam answers via LLM and return scored result."""
    try:
        llm = get_llm()
        prompt = build_eval_prompt(
            data.child_name, data.child_age, data.level, data.module_name, data.responses
        )
        return llm.chat_json(EVAL_SYSTEM_PROMPT, prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
