# Study Brain
# keep building, keep learning, and keep looking for real problems worth solving.

# I won't allow my current skill or knowledge to stop me from solving real-world problems.I can learn the skills or knowledge along the way and I'll keep learning so I can build better solutions over time

An AI-assisted study tool built with Python and Flask.

## Features

- Upload notes and images
- OCR text extraction
- Automatic summaries
- Keyword extraction
- Local processing (no cloud required)

## Tech Stack

- Python
- Flask
- Tesseract OCR
- HTML

## Future Plans

- Revision questions
- Search notes
- Flashcards
- Local AI integration
## cd ~/Desktop/study-brain
## source venv/bin/activate
## python -m py_compile app.py
# Study Brain Roadmap

## ✅ v1.9 Stable
- Universal Revision
- Topic Revision
- Time Revision
- Metadata
- Smart Notes

## 🚧 v2.0
- Split app.py
- Create routes/
- Create services/
- Clean architecture

## v2.1
- Flashcards

## v2.2
- Quiz Mode

## v2.3
- Progress Tracking
## 28 june 2026
# Changelog

## v1.9 Stable

### Added
- Universal Revision
- Topic-wise Revision
- Time-wise Revision
- Custom Date Range
- Smart Notes
- Metadata Engine

### Improved
- Reusable Revision Template
- Reusable Time Engine

### Fixed
- Topic JSON migration
- Route organization
"""
Metadata Service

Handles all metadata operations.

Functions:
- load_metadata()
- save_metadata()
- get_topic()
- get_topics()
- migrate_topics_to_metadata()
"""

# ==================================================
# Imports
# ==================================================

import json
import os
from datetime import datetime


# ==================================================
# Constants
# ==================================================

METADATA_FILE = "metadata.json"
TOPIC_FILE = "topics.json"


# ==================================================
# Metadata Functions
# ==================================================

# load_metadata()

# save_metadata()

s# get_topic()

# get_topics()

# migrate_topics_to_metadata()
# You're starting at a remarkable time
You're entering university during one of the biggest technological transitions in history.

That doesn't guarantee success.

But it means you have opportunities that previous generations didn't.

You can learn:

Computer science

AI

Robotics

Biology

Psychology

Economics

...and combine them in ways that were impossible before.
Spend the next four years becoming someone who can solve difficult problems.

Learn:

mathematics

algorithms

programming

communication

product thinking

ethics

teamwork

Those skills remain valuable no matter how AI evolves.


✅ AI Brain architecture
✅ Online engine
✅ DeepSeek integration
✅ Replace Summary
✅ Replace Keywords
✅ Replace Questions

we are going to send this as a request 
You are an expert teacher.

Read the following study notes.

Create a revision summary.

Rules:

• Keep every important concept.
• Use bullet points.
• Correct OCR mistakes when obvious.
• Don't invent facts.
• Organize information logically.
• Use clear educational language.
# promt engineering 
You are Study Brain.

You are an expert teacher, educator and learning scientist.

Your mission is NOT to summarize text.

Your mission is to help students understand, remember and revise.

You always think like an experienced teacher preparing revision notes before an exam.

You never invent facts.

You only use information provided by the student.

If OCR contains obvious mistakes, silently correct them.

Your notes must be structured, clean and visually easy to revise.

Every response should reduce cognitive load.

Always organize information from general concepts to details.

Brain

│

├── Teacher

├── Summarizer

├── Keyword Extractor

├── Flashcard Generator

├── Question Generator

├── Exam Coach

├── Memory Coach

├── Concept Mapper

└── Doubt Solver