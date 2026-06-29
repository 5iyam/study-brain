from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for,
)
import os
import pytesseract
from PIL import Image
from collections import Counter
import re
from services.index_service import (
    get_index_text,
    clean_combined_text,
    create_index,
)
from services.metadata_service import (
    load_metadata,
    save_metadata,
    get_topic,
    get_topics,
    migrate_topics_to_metadata,
)
from services.revision_service import (
    generate_summary,
    generate_master_summary,
    extract_keywords,
    extract_phrase_concepts,
    generate_revision_questions,
    generate_time_revision,
)

from services.search_service import (
    
    search_index,
)
from services.ocr_service import extract_text_from_image
from routes.home import home_bp
from routes.upload import upload_bp
from routes.search import search_bp
from routes.topics import topics_bp
from routes.time import time_bp


app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(search_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(time_bp)

UPLOAD_FOLDER = "uploads"
INDEX_FOLDER = "index"
TOPIC_FILE = "topics.json"



def load_topics():

    if not os.path.exists(TOPIC_FILE):
        return {}

    try:

        import json

        with open(TOPIC_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:

        return {}


def save_topics(topics):

    import json

    with open(TOPIC_FILE, "w", encoding="utf-8") as f:

        json.dump(
            topics,
            f,
            indent=4,
            ensure_ascii=False
        )


import json
from datetime import datetime, timedelta


METADATA_FILE = "metadata.json"



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




if __name__ == "__main__":

    migrate_topics_to_metadata()

    app.run(debug=True)