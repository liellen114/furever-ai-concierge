import json
import os
from PIL import Image
from PIL.ExifTags import TAGS


DATA_DIR = "data"
MEDIA_DIR = os.path.join(DATA_DIR, "media")
TIMELINE_FILE = os.path.join(DATA_DIR, "timeline.json")
REVIEW_QUEUE_FILE = os.path.join(DATA_DIR, "review_queue.json")


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)

    if not os.path.exists(TIMELINE_FILE):
        save_json(TIMELINE_FILE, [])

    if not os.path.exists(REVIEW_QUEUE_FILE):
        save_json(REVIEW_QUEUE_FILE, [])


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

def save_uploaded_media(uploaded_file):
    """
    Saves an uploaded photo or video into the local data/media folder.
    Returns metadata that can be attached to a memory record.
    """
    ensure_data_files()

    if uploaded_file is None:
        return None

    safe_filename = uploaded_file.name.replace(" ", "_")
    file_path = os.path.join(MEDIA_DIR, safe_filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return {
        "filename": safe_filename,
        "file_path": file_path,
        "file_type": uploaded_file.type
    }

def extract_photo_date(uploaded_file):
    """
    Attempts to extract the original photo date from EXIF metadata.
    Returns a YYYY-MM-DD string if found.
    Does not extract GPS/location metadata.
    """
    if uploaded_file is None:
        return None

    if not uploaded_file.type.startswith("image"):
        return None

    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        exif_data = image.getexif()

        if not exif_data:
            uploaded_file.seek(0)
            return None

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)

            if tag_name in ["DateTimeOriginal", "DateTimeDigitized", "DateTime"]:
                # EXIF date format is usually: YYYY:MM:DD HH:MM:SS
                date_string = str(value)

                if len(date_string) >= 10:
                    year = date_string[0:4]
                    month = date_string[5:7]
                    day = date_string[8:10]

                    uploaded_file.seek(0)
                    return f"{year}-{month}-{day}"

        uploaded_file.seek(0)
        return None

    except Exception:
        uploaded_file.seek(0)
        return None