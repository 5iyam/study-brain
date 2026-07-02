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
# Your home page currently has something like:

🏠 Home

📚 Notes

🔍 Search

🧠 Universal Revision

⏰ Timewise Revision
And I actually think these two features are what make Study Brain unique.

Right now
Most AI note apps focus on:

PDF

↓

Summary

↓

Flashcards
That's useful, but it's not what makes Study Brain special.

The real vision of Study Brain
I think your application has three major pillars.

Pillar 1 — Note Intelligence (what we're building now)
OCR

↓

Smart Note

↓

Summary

↓

Keywords

↓

Questions

↓

Flashcards

↓

Quiz

↓

Tutor
This is all about understanding one note.

Pillar 2 — Universal Revision ⭐
This is where Study Brain becomes different.

Imagine you've studied:

Chapter 1

Chapter 2

Chapter 3

Chapter 4

Chapter 5
Instead of reviewing each separately,

Universal Revision asks:

"What should I revise today from everything I've ever studied?"

Example:

Today's Revision

• Matrix

• Pythagorean Theorem

• Alice Chapter 1

• Newton's First Law

• Photosynthesis
Notice:

It doesn't care which note it came from.

It cares about your knowledge.

Pillar 3 — Timewise Revision ⭐⭐
This is even more powerful.

Imagine:

Monday

↓

Tuesday

↓

Wednesday

↓

Thursday
The app knows:

Studied yesterday

↓

Studied last week

↓

Studied last month
Then it schedules reviews automatically.

Example:

Today

Review:

Chapter 2

Algebra

Matrix

Rabbit Hole

English Vocabulary
This is essentially a built-in spaced repetition system.

Why I'm not rushing there
Those two features depend on something very important:

Good data.

If your Smart Note doesn't generate:

summaries

keywords

questions

then Universal Revision has almost nothing meaningful to work with.

So the dependency chain is:

OCR

↓

Smart Note

↓

Knowledge

↓

Universal Revision

↓

Timewise Revision
My proposed roadmap
Phase 1 (Current)
Finish Smart Note.

✅ Summary

🔄 Keywords

Questions

Flashcards

Quiz

Phase 2
Build a Knowledge Database.

Instead of just saving OCR text, store:

Note

↓

Summary

↓

Keywords

↓

Questions

↓

Date Studied

↓

Difficulty

↓

Subject
Now every note becomes a structured knowledge item.

Phase 3
Universal Revision.

Use all stored knowledge.

Phase 4
Timewise Revision.

Use study history + spaced repetition.

This is the exciting part
I think Universal Revision and Timewise Revision are what people will remember about Study Brain.

Lots of apps can summarize a PDF.

Very few can answer:

"Considering everything I've learned over the last six months, what should I revise today?"

That's the kind of feature that makes a study assistant feel genuinely intelligent.

So my recommendation is:

Don't forget those two features—they're central to your vision.

But build them after Smart Note is mature enough to generate reliable knowledge. That way, when we start Universal Revision, we'll already have high-quality summaries, keywords, and questions to work with instead of having to redesign the foundations later.

# Smart Note

    ↓

Keywords V2

    ↓

Questions V2

    ↓

Flashcards ⭐

    ↓

Quiz ⭐

    ↓

Knowledge Database ⭐⭐⭐

    ↓

Universal Revision ⭐⭐⭐⭐⭐

    ↓

Timewise Revision ⭐⭐⭐⭐⭐

    ↓

AI Tutor ⭐⭐⭐⭐⭐