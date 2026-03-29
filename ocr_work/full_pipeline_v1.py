# extract_hindi_images_openai.py
# ─────────────────────────────────────────────────────────────

import base64
import json
import re
from pathlib import Path
from typing import List, Tuple
import os

import cv2
import numpy as np
import pandas as pd
from openai import OpenAI

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

PRIMARY_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-4o-mini"

INPUT_DIR = Path("input")   # folder with page_0.png etc
OUTPUT_DIR = Path("output")

OUTPUT_CSV = OUTPUT_DIR / "land_records.csv"
OUTPUT_TXT = OUTPUT_DIR / "land_records.txt"
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─────────────────────────────────────────────────────────────
# IMAGE PROCESSING
# ─────────────────────────────────────────────────────────────

def preprocess_image(img_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    denoised = cv2.fastNlMeansDenoising(enhanced, h=8)

    blur = cv2.GaussianBlur(denoised, (0, 0), 3)
    sharpened = cv2.addWeighted(denoised, 1.6, blur, -0.6, 0)

    return sharpened


def ndarray_to_b64_jpeg(img: np.ndarray) -> str:
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf.tobytes()).decode()


def make_crops(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    h, w = img.shape[:2]
    split = w // 3

    return [
        ("full", img),
        ("left", img[:, :split]),
        ("right", img[:, split:]),
    ]


# ─────────────────────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────────────────────

OCR_PROMPT = """
Extract ALL visible Hindi text from this land record image.
Return ONLY raw text.
"""

STRUCTURE_PROMPT = """
Extract structured data from this Hindi land record text.

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
"""


# ─────────────────────────────────────────────────────────────
# OPENAI CALLS
# ─────────────────────────────────────────────────────────────

def vision_call(model, image_b64, prompt):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
        max_tokens=4000,
    )
    return resp.choices[0].message.content.strip()


def text_call(model, prompt):
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    return resp.choices[0].message.content.strip()


def safe_json_parse(text):
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {}


# ─────────────────────────────────────────────────────────────
# PROCESSING
# ─────────────────────────────────────────────────────────────

def process_image(image_path: Path):
    print(f"Processing {image_path.name}...")

    img = cv2.imread(str(image_path))
    img = preprocess_image(img)

    crops = make_crops(img)

    # PASS 1: OCR
    texts = []
    for _, crop in crops:
        b64 = ndarray_to_b64_jpeg(crop)

        try:
            txt = vision_call(PRIMARY_MODEL, b64, OCR_PROMPT)
        except:
            txt = vision_call(FALLBACK_MODEL, b64, OCR_PROMPT)

        texts.append(txt)

    combined_text = "\n".join(texts)

    # PASS 2: STRUCTURE
    try:
        structured = text_call(
            PRIMARY_MODEL,
            STRUCTURE_PROMPT + "\n" + combined_text,
        )
    except:
        structured = text_call(
            FALLBACK_MODEL,
            STRUCTURE_PROMPT + "\n" + combined_text,
        )

    return safe_json_parse(structured)


# ─────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────

def save_outputs(records: List[dict]):
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)

    # TEXT OUTPUT
    lines = []
    for i, r in enumerate(records, 1):
        lines.append(f"\n--- Record {i} ---")
        for k, v in r.items():
            lines.append(f"{k}: {v}")

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ CSV saved → {OUTPUT_CSV}")
    print(f"✅ TXT saved → {OUTPUT_TXT}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    image_files = sorted(INPUT_DIR.glob("*.png"))

    if not image_files:
        print("❌ No images found in input_images/")
        return

    all_records = []

    for img_path in image_files:
        try:
            data = process_image(img_path)
            all_records.append(data)
        except Exception as e:
            print(f"Error processing {img_path.name}: {e}")

    save_outputs(all_records)


if __name__ == "__main__":
    main()