from flask import (
    Blueprint,
    render_template,
    send_from_directory,
)

from services.brain import Brain

import os

from services.index_service import get_index_text
from services.ocr_service import extract_text_from_image

from services.revision_service import (
    generate_summary,
    extract_keywords,
)

note_bp = Blueprint("note", __name__)

brain = Brain(mode="online")

@note_bp.route("/note/<filename>")
def note(filename):

    path = os.path.join("uploads", filename)

    with open(path, "r") as f:
        content = f.read()

    return f"""
    <h1>{filename}</h1>
    <pre>{content}</pre>
    <br>
    <a href="/">Back to Home</a>
    """

@note_bp.route("/image/<filename>")
def image(filename):

    return send_from_directory("uploads", filename)

@note_bp.route("/ocr/<filename>")
def ocr(filename):

    path = os.path.join("uploads", filename)

    text = extract_text_from_image(path)

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

@note_bp.route("/summary/<filename>")
def summary(filename):

    text = get_index_text(filename)

    summary_lines = brain.generate_summary(text)

    html = f"<h1>Better Summary</h1><h3>{filename}</h3><ul>"

    for line in summary_lines:
        html += f"<li>{line}</li>"

    html += "</ul><br><a href='/'>Back to Home</a>"

    return html

@note_bp.route("/keywords/<filename>")
def keywords(filename):

    text = get_index_text(filename)

    keywords = brain.generate_keywords(text)

    html = f"<h1>Keywords</h1><h3>{filename}</h3><ul>"

    for word, count in keywords:
        html += f"<li>{word} ({count})</li>"

    html += "</ul><br><a href='/'>Back to Home</a>"

    return html

@note_bp.route("/questions/<filename>")
def questions(filename):

    text = get_index_text(filename)

    keywords = extract_keywords(text)

    html = f"<h1>Revision Questions</h1><h3>{filename}</h3><ol>"

    for word, count in keywords:
        html += f"<li>What is {word}?</li>"

    html += "</ol><br><a href='/'>Back to Home</a>"

    return html

@note_bp.route("/smart/<filename>")
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