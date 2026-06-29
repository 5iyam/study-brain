from flask import Blueprint
from flask import request, redirect, url_for
import os
from datetime import datetime

from services.index_service import create_index
from services.metadata_service import (
    load_metadata,
    save_metadata,
)

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload():

    file = request.files["note"]
    topic = request.form["topic"].strip()

    if file and file.filename:

        file.save(
            os.path.join(
                "uploads",
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

    return redirect(url_for("home.home"))