import json
import os



METADATA_FILE = "metadata.json"
TOPIC_FILE = "topics.json"


def load_metadata():

    if not os.path.exists(METADATA_FILE):
        return {}

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(data):

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_topic(filename):

    metadata = load_metadata()

    if filename in metadata:

        return metadata[filename].get("topic", "Unknown")
    return "Unknown"


def get_topics():

    metadata = load_metadata()

    topics = {}

    for filename, info in metadata.items():

        topics[filename] = info.get("topic", "Unknown")

    return topics


def migrate_topics_to_metadata():

    metadata = load_metadata()

    topics = get_topics()

    changed = False

    for filename, topic in topics.items():

        if filename not in metadata:

            metadata[filename] = {
                "topic": topic,
                "date": datetime.now().strftime("%Y-%m-%d")
            }

            changed = True

    if changed:
        save_metadata(metadata)