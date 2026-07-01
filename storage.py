import json
import os


DATA_DIR = "data"
TIMELINE_FILE = os.path.join(DATA_DIR, "timeline.json")
REVIEW_QUEUE_FILE = os.path.join(DATA_DIR, "review_queue.json")


def ensure_data_files():
    """
    Creates the data folder and JSON files if they do not already exist.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TIMELINE_FILE):
        with open(TIMELINE_FILE, "w") as file:
            json.dump([], file, indent=2)

    if not os.path.exists(REVIEW_QUEUE_FILE):
        with open(REVIEW_QUEUE_FILE, "w") as file:
            json.dump([], file, indent=2)


def load_json(filepath):
    """
    Loads a JSON list from a file.
    """
    ensure_data_files()

    with open(filepath, "r") as file:
        return json.load(file)


def save_json(filepath, data):
    """
    Saves data to a JSON file.
    """
    ensure_data_files()

    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)


def load_timeline():
    """
    Loads approved memories.
    """
    return load_json(TIMELINE_FILE)


def save_memory_to_timeline(memory):
    """
    Adds one approved memory to the timeline.
    """
    timeline = load_timeline()
    timeline.append(memory)
    save_json(TIMELINE_FILE, timeline)


def load_review_queue():
    """
    Loads memories waiting for human review.
    """
    return load_json(REVIEW_QUEUE_FILE)


def save_memory_to_review_queue(memory, evaluation):
    """
    Adds one memory and its evaluation to the human review queue.
    """
    review_queue = load_review_queue()

    review_item = {
        "review_id": f"review_{len(review_queue) + 1:03d}",
        "memory": memory,
        "evaluation": evaluation,
        "review_status": "pending",
        "reviewer_notes": ""
    }

    review_queue.append(review_item)
    save_json(REVIEW_QUEUE_FILE, review_queue)


def approve_review_item(review_id, edited_memory=None, reviewer_notes=""):
    """
    Approves a review item and moves its memory to the timeline.

    If edited_memory is provided, the human-edited version is saved instead
    of the original agent-generated memory.
    """
    review_queue = load_review_queue()
    timeline = load_timeline()

    updated_queue = []

    for item in review_queue:
        if item["review_id"] == review_id:
            memory = edited_memory if edited_memory is not None else item["memory"]
            memory["status"] = "approved_after_human_review"
            memory["reviewer_notes"] = reviewer_notes
            timeline.append(memory)
        else:
            updated_queue.append(item)

    save_json(TIMELINE_FILE, timeline)
    save_json(REVIEW_QUEUE_FILE, updated_queue)


def reject_review_item(review_id):
    """
    Rejects a review item and removes it from the review queue.
    """
    review_queue = load_review_queue()

    updated_queue = [
        item for item in review_queue
        if item["review_id"] != review_id
    ]

    save_json(REVIEW_QUEUE_FILE, updated_queue)

def reset_demo_data():
    """
    Clears timeline and review queue.
    """
    ensure_data_files()
    save_json(TIMELINE_FILE, [])
    save_json(REVIEW_QUEUE_FILE, [])


def load_demo_data():
    """
    Loads a clean demo timeline and one review item.
    """
    from sample_data import DEMO_SAFE_MEMORY, DEMO_SAFE_MEMORY_2, DEMO_REVIEW_ITEM

    ensure_data_files()
    save_json(TIMELINE_FILE, [DEMO_SAFE_MEMORY, DEMO_SAFE_MEMORY_2])
    save_json(REVIEW_QUEUE_FILE, [DEMO_REVIEW_ITEM])