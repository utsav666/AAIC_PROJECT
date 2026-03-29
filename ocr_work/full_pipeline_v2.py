# advanced_hindi_ocr_v2.py
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
# IMAGE PROCESSING
# ─────────────────────────────────────────────────────────────

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Shadow removal
    dilated = cv2.dilate(gray, np.ones((7,7), np.uint8))
    bg = cv2.medianBlur(dilated, 21)
    diff = 255 - cv2.absdiff(gray, bg)

    # Normalize
    norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)

    # CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(norm)

    # Sharpen
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    sharp = cv2.filter2D(enhanced, -1, kernel)

    # Threshold
    thresh = cv2.adaptiveThreshold(
        sharp, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    return thresh


def deskew(img):
    coords = np.column_stack(np.where(img > 0))
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


def remove_lines(img):
    horizontal = cv2.morphologyEx(
        img,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
    )

    vertical = cv2.morphologyEx(
        img,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
    )

    cleaned = cv2.subtract(img, horizontal)
    cleaned = cv2.subtract(cleaned, vertical)

    return cleaned


# ─────────────────────────────────────────────────────────────
# ✅ FIXED ROW DETECTION (CONTOUR BASED)
# ─────────────────────────────────────────────────────────────

def detect_rows(img):
    inv = 255 - img

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 5))
    dilated = cv2.dilate(inv, kernel, iterations=2)

    contours, _ = cv2.findContours(
        dilated,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    rows = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if h > 25 and w > 200:
            rows.append((y, y + h))

    rows = sorted(rows, key=lambda x: x[0])

    return rows


def crop_rows(original_img, rows):
    return [original_img[y1:y2, :] for (y1, y2) in rows]


def draw_rows(img, rows):
    vis = img.copy()
    for (y1, y2) in rows:
        cv2.rectangle(vis, (0, y1), (img.shape[1], y2), (0,255,0), 2)
    return vis


# ─────────────────────────────────────────────────────────────
# OPENAI HELPERS
# ─────────────────────────────────────────────────────────────

def to_base64(img):
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf.tobytes()).decode()


def vision_call(image_b64, prompt, model=PRIMARY_MODEL):
    resp = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                },
                {"type": "text", "text": prompt}
            ]
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


# ─────────────────────────────────────────────────────────────
# PROMPT (IMPROVED)
# ─────────────────────────────────────────────────────────────

ROW_PROMPT = """
You are reading ONE ROW from a handwritten Hindi land register table.

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

Rules:
- Only this row
- Do NOT mix multiple rows
- Numbers are critical
- Ignore table lines
- If unclear, leave blank
"""

# ─────────────────────────────────────────────────────────────
# PROCESSING
# ─────────────────────────────────────────────────────────────

def process_image(path):
    print(f"\nProcessing {path.name}")

    original = cv2.imread(str(path))

    # Step 1: preprocess + deskew
    processed = preprocess_image(original)
    processed = deskew(processed)

    # Step 2: detect rows BEFORE removing lines
    rows = detect_rows(processed)

    print(f"Detected {len(rows)} rows")
    print("Sample rows:", rows[:5])

    # Debug visualization
    DEBUG_DIR.mkdir(exist_ok=True)
    debug_img = draw_rows(original, rows)
    cv2.imwrite(str(DEBUG_DIR / f"debug_{path.name}"), debug_img)

    # Step 3: remove lines AFTER row detection
    processed = remove_lines(processed)

    cropped_rows = crop_rows(original, rows)

    records = []

    for i, row_img in enumerate(cropped_rows):
        b64 = to_base64(row_img)

        try:
            out = vision_call(b64, ROW_PROMPT)
        except:
            out = vision_call(b64, ROW_PROMPT, FALLBACK_MODEL)

        data = safe_json(out)

        if data:
            records.append(data)

    return records


# ─────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────

def save(records: List[dict]):
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)

    lines = []
    for i, r in enumerate(records, 1):
        lines.append(f"\n--- Record {i} ---")
        for k, v in r.items():
            lines.append(f"{k}: {v}")

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n✅ Saved CSV and TXT")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    images = sorted(INPUT_DIR.glob("*.png"))

    if not images:
        print("❌ No images found in input/")
        return

    all_records = []

    for img in images:
        records = process_image(img)
        all_records.extend(records)

    save(all_records)


if __name__ == "__main__":
    main()