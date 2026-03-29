# advanced_hindi_ocr_v4.py

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

# CONFIG
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

PRIMARY_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT_CSV = OUTPUT_DIR / "records.csv"
OUTPUT_TXT = OUTPUT_DIR / "records.txt"


# ─────────────────────────────────────────────
# IMAGE PROCESSING (KEEP IT LIGHT)
# ─────────────────────────────────────────────

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    return enhanced


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


def to_b64(img):
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf.tobytes()).decode()


# ─────────────────────────────────────────────
# PROMPT (VERY IMPORTANT)
# ─────────────────────────────────────────────

PROMPT = """
You are reading a FULL PAGE of a handwritten Hindi land record.

IMPORTANT:
- This page contains ONE record only
- Information is spread across the page in columns

Extract structured data.

Return JSON ONLY:

{
  "owner_name": "",
  "plot_number": "",
  "plot_area": "",
  "location": "",
  "document_date": "",
  "document_type": "",
  "additional_details": ""
}

Guidelines:
- Owner name is usually on LEFT side
- Plot numbers and area are in middle columns
- Dates and notes on right side
- Do NOT create multiple records
- If unsure, leave blank
"""


# ─────────────────────────────────────────────
# MODEL CALL
# ─────────────────────────────────────────────

def call_model(img, model=PRIMARY_MODEL):
    b64 = to_b64(img)

    resp = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                },
                {"type": "text", "text": PROMPT}
            ]
        }],
        max_tokens=2000
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
# PROCESS
# ─────────────────────────────────────────────

def process_image(path):
    print(f"\nProcessing {path.name}")

    img = cv2.imread(str(path))

    img = deskew(img)
    img = preprocess(img)

    try:
        out = call_model(img)
    except:
        out = call_model(img, FALLBACK_MODEL)

    data = safe_json(out)

    return data


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

    print("\n✅ DONE")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    images = sorted(INPUT_DIR.glob("*.png"))

    all_records = []

    for img in images:
        record = process_image(img)
        if record:
            all_records.append(record)

    save(all_records)


if __name__ == "__main__":
    main()