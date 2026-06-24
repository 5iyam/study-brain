from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

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
    with open(os.path.join(UPLOAD_FOLDER, filename), "r") as f:
        content = f.read()

    return f"""
    <h1>{filename}</h1>
    <pre>{content}</pre>
    <br>
    <a href="/">Back to Home</a>
    """

if __name__ == "__main__":
    app.run(debug=True)