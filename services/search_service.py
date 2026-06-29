"""
Search Service

Handles all searching operations.

Functions:
- search_notes()
- search_index()
"""

# ==================================================
# Imports
# ==================================================

import os
#import pytesseract
#from PIL import Image
import re

# ==================================================
# Constants
# ==================================================

UPLOAD_FOLDER = "uploads"
INDEX_FOLDER = "index"

# ==================================================
# Search Functions
# ==================================================

# def search_notes(query):
#     results = []
#     files = os.listdir(UPLOAD_FOLDER)

#     for file in files:
#         path = os.path.join(UPLOAD_FOLDER, file)
#         text = ""

#         try:
#             if file.lower().endswith((".png", ".jpg", ".jpeg")):
#                 text = pytesseract.image_to_string(Image.open(path))
#             else:
#                 with open(path, "r", errors="ignore") as f:
#                     text = f.read()

#             if query.lower() in text.lower():
#                 results.append(file)
#         except:
#             pass

#     return results


def search_index(query):
    results = []
    files = os.listdir(INDEX_FOLDER)
    image_extensions = [".png", ".jpg", ".jpeg"]

    for file in files:
        path = os.path.join(INDEX_FOLDER, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            score = text.lower().count(query.lower())

            if score == 0:
                continue

            pos = text.lower().find(query.lower())
            start = max(0, pos - 60)
            end = min(len(text), pos + 120)
            snippet = "..." + text[start:end] + "..."

            snippet = re.sub(
    re.escape(query),
    lambda m: f"<mark>{m.group(0)}</mark>",
    snippet,
    flags=re.IGNORECASE
)

            base_name = os.path.splitext(file)[0]
            display_name = base_name + ".txt"
            file_type = "text"

            for ext in image_extensions:
                if os.path.exists(
                    os.path.join(UPLOAD_FOLDER, base_name + ext)
                ):
                    display_name = base_name + ext
                    file_type = "image"
                    break

            if score == 1:
                relevance = "⭐ Fair Match"
            elif score <= 3:
                relevance = "⭐⭐ Good Match"
            elif score <= 6:
                relevance = "⭐⭐⭐ Very Good Match"
            elif score <= 10:
                relevance = "⭐⭐⭐⭐ Excellent Match"
            else:
                relevance = "⭐⭐⭐⭐⭐ Perfect Match"

            results.append({
                "file": display_name,
                "score": score,
                "relevance": relevance,
                "snippet": snippet,
                "type": file_type
            })

        except Exception:
            pass

    results.sort(key=lambda x: x["score"], reverse=True)
    return results