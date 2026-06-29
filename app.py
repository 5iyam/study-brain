from flask import Flask, render_template, request, send_from_directory
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

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
INDEX_FOLDER = "index"
TOPIC_FILE = "topics.json"




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
    topics = get_topics()
    return render_template(
        "index.html",
        files=files,
        topics=topics
    )


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["note"]
    topic = request.form["topic"].strip()

    if file and file.filename:

        file.save(
            os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )
        )

        create_index(file.filename)

        metadata = load_metadata()

        metadata[file.filename] = {
            "topic": topic,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        save_metadata(metadata)

        

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

    phrase_data = extract_phrase_concepts(all_text)

    keywords = phrase_data

    concepts = phrase_data[:5]


    questions = generate_revision_questions(all_text)

    total_characters = len(all_text)

    reading_time = max(1, total_characters // 1000)

    return render_template(
        "universal.html",
        summary=summary,
        keywords=keywords,
        concepts=concepts,
        questions=questions,
        total_notes=len(files),
        total_characters=total_characters,
        reading_time=reading_time,
    )


@app.route("/topics")
def topics():

    topic_data = get_topics()

    topic_count = {}

    for filename, topic in topic_data.items():

        if topic not in topic_count:
            topic_count[topic] = 0

        topic_count[topic] += 1

    return render_template(
        "topics.html",
        topic_count=topic_count
    )


@app.route("/topic/<topic_name>")
def topic(topic_name):

    topics = get_topics()

    files = []

    combined_text = ""

    for filename, topic in topics.items():

        if topic == topic_name:

            files.append(filename)

            combined_text += "\n"

            combined_text += get_index_text(filename)

    combined_text = clean_combined_text(combined_text)

    summary = generate_master_summary(combined_text)

    phrase_data = extract_phrase_concepts(combined_text)

    concepts = phrase_data[:5]

    keywords = phrase_data

    questions = generate_revision_questions(combined_text)

    return render_template(
        "revision.html",
        title=f"📂 {topic_name}",
        back_url="/topics",
        back_text="⬅ Back to Topics",
        files=files,
        summary=summary,
        concepts=concepts,
        keywords=keywords,
        questions=questions
    )



@app.route("/time")
def time_revision():

    return render_template("time.html")




@app.route("/time/today")
def today_revision():

    today = datetime.now().strftime("%Y-%m-%d")

    data = generate_time_revision(today, today)

    return render_template(
        "revision.html",
        title="📅 Today's Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


@app.route("/time/yesterday")
def yesterday_revision():

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    data = generate_time_revision(yesterday, yesterday)

    return render_template(
        "revision.html",
        title="📅 Yesterday's Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


@app.route("/time/week")
def last_week_revision():

    today = datetime.now().strftime("%Y-%m-%d")

    last_week = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")

    data = generate_time_revision(last_week, today)

    return render_template(
        "revision.html",
        title="📅 Last 7 Days Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


@app.route("/time/month")
def last_month_revision():

    today = datetime.now().strftime("%Y-%m-%d")

    last_month = (datetime.now() - timedelta(days=29)).strftime("%Y-%m-%d")

    data = generate_time_revision(last_month, today)

    return render_template(
        "revision.html",
        title="📅 Last 30 Days Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


@app.route("/time/custom", methods=["POST"])
def custom_revision():

    start_date = request.form["start_date"]

    end_date = request.form["end_date"]

    data = generate_time_revision(start_date, end_date)

    return render_template(
        "revision.html",
        title=f"📅 Revision ({start_date} → {end_date})",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


if __name__ == "__main__":

    migrate_topics_to_metadata()

    app.run(debug=True)