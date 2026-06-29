from flask import Blueprint, render_template
import os

from services.index_service import (
    get_index_text,
    clean_combined_text,
)

from services.revision_service import (
    generate_master_summary,
    extract_phrase_concepts,
    generate_revision_questions,
)

universal_bp = Blueprint("universal", __name__)

@universal_bp.route("/universal")
def universal():

    all_text = ""

    files = os.listdir("index")

    for file in files:

        try:

            all_text += "\n\n"

            all_text += get_index_text(file)

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