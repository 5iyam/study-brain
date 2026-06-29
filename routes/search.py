from flask import Blueprint, request, render_template
import os

from services.search_service import search_index

search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["POST"])
def search():

    query = request.form["query"]

    results = search_index(query)

    indexed_notes = len(os.listdir("index"))

    return render_template(
        "search.html",
        query=query,
        results=results,
        indexed_notes=indexed_notes
    )