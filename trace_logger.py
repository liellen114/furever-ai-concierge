import json
import os
from datetime import datetime


DATA_DIR = "data"
TRACE_FILE = os.path.join(DATA_DIR, "trace_log.json")


def ensure_trace_file():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TRACE_FILE):
        with open(TRACE_FILE, "w") as file:
            json.dump([], file, indent=2)


def log_trace(step, status, details=None):
    """
    Adds one trace event to the local trace log.
    """
    ensure_trace_file()

    with open(TRACE_FILE, "r") as file:
        traces = json.load(file)

    event = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "step": step,
        "status": status,
        "details": details or {}
    }

    traces.append(event)

    with open(TRACE_FILE, "w") as file:
        json.dump(traces, file, indent=2)


def load_traces():
    ensure_trace_file()

    with open(TRACE_FILE, "r") as file:
        return json.load(file)


def clear_traces():
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(TRACE_FILE, "w") as file:
        json.dump([], file, indent=2)