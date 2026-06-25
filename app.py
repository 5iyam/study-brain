from flask import Flask, render_template, request, send_from_directory
import os
import pytesseract
from PIL import Image
from collections import Counter

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"


def generate_summary(text):

    lines = text.split("\n")

    cleaned = []

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


@app.route("/")
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["note"]

    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return home()


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

    path = os.path.join(UPLOAD_FOLDER, filename)

    text = pytesseract.image_to_string(Image.open(path))

    summary_lines = generate_summary(text)

    html = f"""
    <h1>Better Summary</h1>

    <h3>{filename}</h3>

    <ul>
    """

    for line in summary_lines:
        html += f"<li>{line}</li>"

    html += """
    </ul>

    <br>

    <a href="/">Back to Home</a>
    """

    return html


@app.route("/keywords/<filename>")
def keywords(filename):

    path = os.path.join(UPLOAD_FOLDER, filename)

    text = pytesseract.image_to_string(Image.open(path))

    keywords = extract_keywords(text)

    html = f"""
    <h1>Keywords</h1>

    <h3>{filename}</h3>

    <ul>
    """

    for word, count in keywords:
        html += f"<li>{word} ({count})</li>"

    html += """
    </ul>

    <br>

    <a href="/">Back to Home</a>
    """

    return html


@app.route("/questions/<filename>")
def questions(filename):

    path = os.path.join(UPLOAD_FOLDER, filename)

    text = pytesseract.image_to_string(Image.open(path))

    keywords = extract_keywords(text)

    html = f"""
    <h1>Revision Questions</h1>

    <h3>{filename}</h3>

    <ol>
    """

    for word, count in keywords:
        html += f"<li>What is {word}?</li>"

    html += """
    </ol>

    <br>

    <a href="/">Back to Home</a>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)