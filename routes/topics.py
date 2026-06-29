from flask import Blueprint, render_template

from services.metadata_service import get_topics
from services.index_service import (
    get_index_text,
    clean_combined_text,
)
from services.revision_service import (
    generate_master_summary,
    extract_phrase_concepts,
    generate_revision_questions,
)

topics_bp = Blueprint("topics", __name__)


@topics_bp.route("/topics")
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


@topics_bp.route("/topic/<topic_name>")
def topic(topic_name):

    topics = get_topics()

    files = []

    combined_text = ""

    for filename, topic_name_in_file in topics.items():

        if topic_name_in_file == topic_name:

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