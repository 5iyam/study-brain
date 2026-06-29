"""
Index Service

Handles note indexing and indexed text retrieval.

Functions:
- create_index()
- get_index_text()
- clean_combined_text()
"""

# ==================================================
# Imports
# ==================================================

import os
import pytesseract
from PIL import Image


# ==================================================
# Constants
# ==================================================

INDEX_FOLDER = "index"
UPLOAD_FOLDER = "uploads"


# ==================================================
# Index Functions
# ==================================================

def get_index_text(filename):
    index_filename = os.path.splitext(filename)[0] + ".txt"
    index_path = os.path.join(INDEX_FOLDER, index_filename)

    if not os.path.exists(index_path):
        return ""

    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

def clean_combined_text(text):

    lines = text.split("\n")

    cleaned = []

    seen = set()

    for line in lines:

        line = line.strip()

        if len(line) < 5:
            continue

        lower = line.lower()

        if lower in seen:
            continue

        seen.add(lower)

        cleaned.append(line)

    return "\n".join(cleaned)

def create_index(filename):
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    index_filename = os.path.splitext(filename)[0] + ".txt"
    index_path = os.path.join(INDEX_FOLDER, index_filename)
    text = ""

    try:
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = pytesseract.image_to_string(Image.open(upload_path))
        else:
            with open(upload_path, "r", errors="ignore") as f:
                text = f.read()

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(text)

    except Exception as e:
        print("Indexing Error:", e)