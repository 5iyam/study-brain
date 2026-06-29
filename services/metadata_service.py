import json
import os



METADATA_FILE = "metadata.json"
TOPIC_FILE = "topics.json"



def load_metadata():

    if not os.path.exists(METADATA_FILE):
        return {}

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)