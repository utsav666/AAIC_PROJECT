# advanced_hindi_ocr_v5.py
# ─────────────────────────────────────────────────────────────

import base64
import json
import re
from pathlib import Path
import os

import cv2
import numpy as np
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

PRIMARY_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT_CSV = OUTPUT_DIR / "records.csv"
OUTPUT_TXT = OUTPUT_DIR / "records.txt"

# ─────────────────────────────────────────────
# IMAGE PROCESSING
# ─────────────────────────────────────────────

def deskew(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray < 200))

    if len(coords) == 0:
        return img

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)

    return cv2.warpAffine(img, M, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    return enhanced


def split_regions(img):
    h, w = img.shape[:2]

    return {
        "left": img[:, :int(w*0.35)],
        "middle": img[:, int(w*0.35):int(w*0.7)],
        "right": img[:, int(w*0.7):]
    }


def to_b64(img):
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf.tobytes()).decode()


# ─────────────────────────────────────────────
# MODEL CALLS
# ─────────────────────────────────────────────

def vision_call(img, prompt, model=PRIMARY_MODEL):
    b64 = to_b64(img)

    resp = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": prompt}
            ]
        }],
        max_tokens=2000
    )

    return resp.choices[0].message.content.strip()


def text_call(text, prompt, model=PRIMARY_MODEL):
    resp = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt + "\n\n" + text
        }],
        max_tokens=1500
    )

    return resp.choices[0].message.content.strip()


def safe_json(text):
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {}


# ─────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────

OCR_PROMPT = """
Extract ALL visible Hindi text exactly as written.
Do NOT summarize.
Return plain text only.
"""

STRUCTURE_PROMPT = """
You are given OCR text from a Hindi land record.

Extract ONE record only.

Return JSON:

{
  "owner_name": "",
  "plot_number": "",
  "plot_area": "",
  "location": "",
  "document_date": "",
  "document_type": "",
  "additional_details": ""
}

Rules:
- DO NOT invent data
- Use only given text
- If missing, leave blank
- If multiple values exist, choose most complete
"""

# ─────────────────────────────────────────────
# CLEANING + VALIDATION
# ─────────────────────────────────────────────

def normalize_numbers(text):
    if not text:
        return text
    return text.translate(str.maketrans("०१२३४५६७८९", "0123456789"))


def clean_record(record):
    if not record:
        return record

    for key in record:
        if isinstance(record[key], str):
            record[key] = record[key].strip()

    record["plot_number"] = normalize_numbers(record.get("plot_number", ""))
    record["plot_area"] = normalize_numbers(record.get("plot_area", ""))
    record["document_date"] = normalize_numbers(record.get("document_date", ""))

    return record


def validate_record(r):
    score = 0

    if r.get("owner_name"):
        score += 1

    if re.search(r"\d", r.get("plot_number", "")):
        score += 1

    if re.search(r"\d", r.get("plot_area", "")):
        score += 1

    if re.search(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", r.get("document_date", "")):
        score += 1

    return score


def add_confidence(record):
    score = validate_record(record)

    if score >= 4:
        record["confidence"] = "HIGH"
    elif score >= 2:
        record["confidence"] = "MEDIUM"
    else:
        record["confidence"] = "LOW"

    return record


def retry_missing_fields(text, record):
    missing = [k for k, v in record.items() if not v and k != "confidence"]

    if not missing:
        return record

    retry_prompt = f"""
Fill ONLY missing fields: {missing}

Return JSON only.
"""

    retry = text_call(text, retry_prompt)
    retry_json = safe_json(retry)

    for k in missing:
        if retry_json.get(k):
            record[k] = retry_json[k]

    return record


# ─────────────────────────────────────────────
# PROCESS IMAGE
# ─────────────────────────────────────────────

def process_image(path):
    print(f"\nProcessing {path.name}")

    img = cv2.imread(str(path))
    img = deskew(img)
    img = preprocess(img)

    regions = split_regions(img)

    texts = []

    for part in regions.values():
        try:
            txt = vision_call(part, OCR_PROMPT)
        except:
            txt = vision_call(part, OCR_PROMPT, FALLBACK_MODEL)

        texts.append(txt)

    full_text = "\n".join(texts)

    structured = text_call(full_text, STRUCTURE_PROMPT)
    record = safe_json(structured)

    # Cleaning + validation
    record = clean_record(record)
    record = retry_missing_fields(full_text, record)
    record = clean_record(record)
    record = add_confidence(record)

    return record


# ─────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────

def save(records):
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        for i, r in enumerate(records, 1):
            f.write(f"\n--- Record {i} ---\n")
            for k, v in r.items():
                f.write(f"{k}: {v}\n")

    print("\n✅ Saved CSV and TXT")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    images = sorted(INPUT_DIR.glob("*.png"))

    if not images:
        print("❌ No images found")
        return

    all_records = []

    for img in images:
        record = process_image(img)
        if record:
            all_records.append(record)

    save(all_records)


if __name__ == "__main__":
    main()