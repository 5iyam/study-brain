from flask import Blueprint, render_template
import os

from services.metadata_service import get_topics

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    files = os.listdir("uploads")
    topics = get_topics()

    return render_template(
        "index.html",
        files=files,
        topics=topics
    )