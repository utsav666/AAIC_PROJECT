# advanced_hindi_ocr_v3.py
# ─────────────────────────────────────────────────────────────

import base64
import json
import re
from pathlib import Path
from typing import List
import os

import cv2
import numpy as np
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
DEBUG_DIR = Path("debug")

PRIMARY_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT_CSV = OUTPUT_DIR / "records.csv"
OUTPUT_TXT = OUTPUT_DIR / "records.txt"

# ─────────────────────────────────────────────────────────────
# BASIC PREPROCESS (LIGHT)
# ─────────────────────────────────────────────────────────────

def light_preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    return blur


# ─────────────────────────────────────────────────────────────
# HEAVY PREPROCESS (OCR)
# ─────────────────────────────────────────────────────────────

def ocr_preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    thresh = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    return thresh


# ─────────────────────────────────────────────────────────────
# DESKEW
# ─────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────
# ROW DETECTION (IMPROVED)
# ─────────────────────────────────────────────────────────────

def detect_rows(img):
    gray = light_preprocess(img)

    # horizontal projection
    proj = np.sum(gray < 200, axis=1)

    rows = []
    start = None

    for i, val in enumerate(proj):
        if val > 50 and start is None:
            start = i
        elif val <= 50 and start is not None:
            if i - start > 15:
                rows.append((start, i))
            start = None

    return rows


def split_large_rows(rows):
    new_rows = []

    for (y1, y2) in rows:
        h = y2 - y1

        if h > 120:
            mid = (y1 + y2) // 2
            new_rows.append((y1, mid))
            new_rows.append((mid, y2))
        else:
            new_rows.append((y1, y2))

    return new_rows


# ─────────────────────────────────────────────────────────────
# COLUMN SPLIT (CRITICAL)
# ─────────────────────────────────────────────────────────────

def split_columns(row_img):
    h, w = row_img.shape[:2]

    return {
        "left": row_img[:, :int(w*0.3)],     # names
        "middle": row_img[:, int(w*0.3):int(w*0.7)],  # numbers
        "right": row_img[:, int(w*0.7):]     # misc
    }


# ─────────────────────────────────────────────────────────────
# OPENAI
# ─────────────────────────────────────────────────────────────

def to_b64(img):
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf.tobytes()).decode()


def call_model(img, prompt, model=PRIMARY_MODEL):
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
                {"type": "text", "text": prompt}
            ]
        }],
        max_tokens=800
    )

    return resp.choices[0].message.content.strip()


def safe_json(text):
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {}


# ─────────────────────────────────────────────────────────────
# PROMPTS (SPECIALIZED)
# ─────────────────────────────────────────────────────────────

LEFT_PROMPT = "Extract ONLY the Hindi PERSON NAME from this image. Return plain text."
MID_PROMPT = "Extract ONLY numbers like plot number, area. Return plain text."
RIGHT_PROMPT = "Extract any remaining info (date/location). Return plain text."

MERGE_PROMPT = """
Combine the extracted pieces into JSON:

{
  "owner_name": "",
  "plot_number": "",
  "plot_area": "",
  "location": "",
  "document_date": "",
  "document_type": "",
  "additional_details": ""
}

Return JSON only.
"""

# ─────────────────────────────────────────────────────────────
# PROCESS IMAGE
# ─────────────────────────────────────────────────────────────

def process_image(path):
    print(f"\nProcessing {path.name}")

    img = cv2.imread(str(path))
    img = deskew(img)

    rows = detect_rows(img)
    rows = split_large_rows(rows)

    print(f"Detected {len(rows)} rows")

    DEBUG_DIR.mkdir(exist_ok=True)

    records = []

    for idx, (y1, y2) in enumerate(rows):
        row_img = img[y1:y2, :]

        # split columns
        cols = split_columns(row_img)

        left = ocr_preprocess(cols["left"])
        mid = ocr_preprocess(cols["middle"])
        right = ocr_preprocess(cols["right"])

        try:
            name = call_model(left, LEFT_PROMPT)
            nums = call_model(mid, MID_PROMPT)
            extra = call_model(right, RIGHT_PROMPT)

            combined = f"Name: {name}\nNumbers: {nums}\nExtra: {extra}"

            final = call_model(
                row_img,
                MERGE_PROMPT + "\n" + combined
            )

        except:
            final = "{}"

        data = safe_json(final)

        if data:
            records.append(data)

        # save debug rows
        cv2.imwrite(str(DEBUG_DIR / f"{path.stem}_row_{idx}.png"), row_img)

    return records


# ─────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────

def save(records: List[dict]):
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        for i, r in enumerate(records, 1):
            f.write(f"\n--- Record {i} ---\n")
            for k, v in r.items():
                f.write(f"{k}: {v}\n")

    print("\n✅ DONE")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    images = sorted(INPUT_DIR.glob("*.png"))

    all_records = []

    for img in images:
        all_records.extend(process_image(img))

    save(all_records)


if __name__ == "__main__":
    main()