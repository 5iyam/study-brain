from flask import Flask, render_template, request, send_from_directory
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"


def generate_summary(text):
    sentences = text.replace("\n", " ").split(".")

    summary = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            summary.append(sentence)

        if len(summary) >= 5:
            break

    return summary


@app.route("/")
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["note"]

    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@app.route("/note/<filename>")
def note(filename):

    filename = filename
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

    <a href="/summary/{filename}">
        Generate Summary
    </a>

    <br><br>

    <a href="/">Back to Home</a>
    """


@app.route("/summary/<filename>")
def summary(filename):

    path = os.path.join(UPLOAD_FOLDER, filename)

    text = pytesseract.image_to_string(Image.open(path))

    summary_lines = generate_summary(text)

    html = f"""
    <h1>Summary</h1>

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


if __name__ == "__main__":
    app.run(debug=True)