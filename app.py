from flask import Flask, render_template, request, send_from_directory
import os
import pytesseract
from PIL import Image
from collections import Counter
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
INDEX_FOLDER = "index"


def generate_summary(text):
    lines = text.split("\n")
    cleaned = []
    ignore_words = [
        "name", "roll", "date", "page", "class", "section"
    ]

    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        skip = False
        for word in ignore_words:
            if word in line.lower():
                skip = True
                break
        if not skip:
            cleaned.append(line)

    cleaned.sort(key=len, reverse=True)
    return cleaned[:5]


def generate_master_summary(text):

    lines = text.split("\n")

    summary = []

    seen = set()

    ignore_words = [
        "name",
        "roll",
        "date",
        "page",
        "class",
        "section"
    ]

    for line in lines:

        line = line.strip()

        if len(line) < 40:
            continue

        lower = line.lower()

        skip = False

        for word in ignore_words:

            if word in lower:
                skip = True
                break

        if skip:
            continue

        if lower in seen:
            continue

        seen.add(lower)

        summary.append(line)

    summary.sort(key=lambda x: len(x.split()), reverse=True)

    return summary[:10]


def extract_keywords(text):
    words = text.lower().split()
    stop_words = {
        "the", "is", "a", "an", "and", "or",
        "to", "of", "in", "on", "for",
        "with", "this", "that", "it",
        "are", "was", "were", "be",
        "as", "by", "at", "from"
    }
    cleaned = []

    for word in words:
        word = ''.join(c for c in word if c.isalnum())
        if len(word) < 4:
            continue
        if word in stop_words:
            continue
        cleaned.append(word)

    counter = Counter(cleaned)
    return counter.most_common(10)


def search_notes(query):
    results = []
    files = os.listdir(UPLOAD_FOLDER)

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file)
        text = ""

        try:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                text = pytesseract.image_to_string(Image.open(path))
            else:
                with open(path, "r", errors="ignore") as f:
                    text = f.read()

            if query.lower() in text.lower():
                results.append(file)
        except:
            pass

    return results


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
@app.route("/")
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["note"]

    if file and file.filename:

        file.save(
            os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )
        )

        create_index(file.filename)

    return home()


@app.route("/search", methods=["POST"])
def search():

    query = request.form["query"]

    results = search_index(query)

    indexed_notes = len(os.listdir(INDEX_FOLDER))

    return render_template(
        "search.html",
        query=query,
        results=results,
        indexed_notes=indexed_notes
    )


@app.route("/note/<filename>")
def note(filename):

    path = os.path.join(UPLOAD_FOLDER, filename)

    with open(path, "r") as f:
        content = f.read()

    return f"""
    <h1>{filename}</h1>
    <pre>{content}</pre>
    <br>
    <a href="/">Back to Home</a>
    """


@app.route("/image/<filename>")
def image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/ocr/<filename>")
def ocr(filename):

    path = os.path.join(UPLOAD_FOLDER, filename)

    text = pytesseract.image_to_string(Image.open(path))

    return f"""
    <h1>OCR Result</h1>

    <h3>{filename}</h3>

    <pre>{text}</pre>

    <br>

    <a href="/summary/{filename}">Better Summary</a>

    <br><br>

    <a href="/keywords/{filename}">Keywords</a>

    <br><br>

    <a href="/questions/{filename}">Revision Questions</a>

    <br><br>

    <a href="/">Back to Home</a>
    """


@app.route("/summary/<filename>")
def summary(filename):

    text = get_index_text(filename)

    summary_lines = generate_summary(text)

    html = f"<h1>Better Summary</h1><h3>{filename}</h3><ul>"

    for line in summary_lines:
        html += f"<li>{line}</li>"

    html += "</ul><br><a href='/'>Back to Home</a>"

    return html


@app.route("/keywords/<filename>")
def keywords(filename):

    text = get_index_text(filename)

    keywords = extract_keywords(text)

    html = f"<h1>Keywords</h1><h3>{filename}</h3><ul>"

    for word, count in keywords:
        html += f"<li>{word} ({count})</li>"

    html += "</ul><br><a href='/'>Back to Home</a>"

    return html




@app.route("/questions/<filename>")
def questions(filename):

    text = get_index_text(filename)

    keywords = extract_keywords(text)

    html = f"<h1>Revision Questions</h1><h3>{filename}</h3><ol>"

    for word, count in keywords:
        html += f"<li>What is {word}?</li>"

    html += "</ol><br><a href='/'>Back to Home</a>"

    return html


@app.route("/smart/<filename>")
def smart_note(filename):

    text = get_index_text(filename)

    summary = generate_summary(text)

    keywords = extract_keywords(text)

    questions = []

    for word, count in keywords:
        questions.append(f"What is {word}?")

    return render_template(
        "note.html",
        filename=filename,
        text=text,
        summary=summary,
        keywords=keywords,
        questions=questions
    )



@app.route("/universal")
def universal():

    all_text = ""

    files = os.listdir(INDEX_FOLDER)

    for file in files:

        path = os.path.join(INDEX_FOLDER, file)

        try:

            with open(path, "r", encoding="utf-8") as f:

                all_text += "\n\n"

                all_text += f.read()

        except:

            pass

    all_text = clean_combined_text(all_text)

    summary = generate_master_summary(all_text)

    keywords = extract_keywords(all_text)

    questions = []

    for word, count in keywords:

        questions.append(f"What is {word}?")

    return render_template(
        "universal.html",
        summary=summary,
        keywords=keywords,
        questions=questions,
        total_notes=len(files)
    )


if __name__ == "__main__":
    app.run(debug=True)