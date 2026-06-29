"""
Revision Service

Handles summary generation, keyword extraction,
concept extraction and revision question generation.

Functions:
- generate_summary()
- generate_master_summary()
- extract_keywords()
- extract_main_concepts()
- extract_phrase_concepts()
- generate_revision_questions()
- generate_time_revision()
"""

# ==================================================
# Imports
# ==================================================

from collections import Counter
from services.metadata_service import load_metadata
from services.index_service import (
    get_index_text,
    clean_combined_text,
)

# ==================================================
# Constants
# ==================================================



# ==================================================
# Revision Functions
# ==================================================

def generate_summary(text):
    lines = text.split("\n")
    cleaned = []
    ignore_words = [
        "name", "roll", "date", "page", "class", "section"
    ]

    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        skip = False
        for word in ignore_words:
            if word in line.lower():
                skip = True
                break
        if not skip:
            cleaned.append(line)

    cleaned.sort(key=len, reverse=True)
    return cleaned[:5]

def generate_master_summary(text):

    lines = text.split("\n")

    summary = []

    seen = set()

    ignore_words = [
        "name",
        "roll",
        "date",
        "page",
        "class",
        "section"
    ]

    for line in lines:

        line = line.strip()

        if len(line) < 40:
            continue

        lower = line.lower()

        skip = False

        for word in ignore_words:

            if word in lower:
                skip = True
                break

        if skip:
            continue

        if lower in seen:
            continue

        seen.add(lower)

        summary.append(line)

    summary.sort(key=lambda x: len(x.split()), reverse=True)

    return summary[:10]


def extract_keywords(text):
    words = text.lower().split()
    stop_words = {
        "the", "is", "a", "an", "and", "or",
        "to", "of", "in", "on", "for",
        "with", "this", "that", "it",
        "are", "was", "were", "be",
        "as", "by", "at", "from"
    }
    cleaned = []

    for word in words:
        word = ''.join(c for c in word if c.isalnum())
        if len(word) < 4:
            continue
        if word in stop_words:
            continue
        cleaned.append(word)

    counter = Counter(cleaned)
    return counter.most_common(10)


def extract_phrase_concepts(text):

    words = text.split()

    stop_words = {
        "the", "is", "a", "an", "of", "to",
        "and", "or", "for", "in", "on",
        "with", "this", "that", "are"
    }

    phrases = []

    for i in range(len(words) - 1):

        first = ''.join(c for c in words[i] if c.isalnum())

        second = ''.join(c for c in words[i + 1] if c.isalnum())

        if len(first) < 3 or len(second) < 3:
            continue

        if first.lower() in stop_words:
            continue

        if second.lower() in stop_words:
            continue

        phrase = first.title() + " " + second.title()

        phrases.append(phrase)

    counter = Counter(phrases)

    return counter.most_common(15)


def generate_revision_questions(text):

    concepts = extract_phrase_concepts(text)

    templates = [
        "What is {}?",
        "Explain {}.",
        "How does {} work?",
        "Why is {} important?",
        "Write short notes on {}.",
        "What are the applications of {}?",
        "Describe {}.",
        "Discuss the advantages of {}."
    ]

    questions = []

    for i, (concept, count) in enumerate(concepts):

        template = templates[i % len(templates)]

        questions.append(template.format(concept))

    return questions


def generate_time_revision(start_date, end_date):

    metadata = load_metadata()

    files = []

    combined_text = ""

    for filename, info in metadata.items():

        note_date = info.get("date")

        if note_date is None:
            continue

        if start_date <= note_date <= end_date:

            files.append(filename)

            combined_text += "\n"

            combined_text += get_index_text(filename)

    combined_text = clean_combined_text(combined_text)

    summary = generate_master_summary(combined_text)

    phrase_data = extract_phrase_concepts(combined_text)

    concepts = phrase_data[:5]

    keywords = phrase_data

    questions = generate_revision_questions(combined_text)

    return {
        "files": files,
        "summary": summary,
        "concepts": concepts,
        "keywords": keywords,
        "questions": questions
    }