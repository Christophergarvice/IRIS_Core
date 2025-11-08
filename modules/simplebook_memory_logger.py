import json
import os
from datetime import datetime

# Path for the memory log file
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "SimpleBook_ExperienceMemory.json")

def log_event(module, action, result, notes=""):
    """Record an experience event to JSON memory."""
    event = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "module": module,
        "action": action,
        "result": result,
        "notes": notes
    }

    # Load existing log or start a new one
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Append the new event
    data.append(event)

    # Save updated log
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_summary():
    """Return a summary of success and failure counts."""
    if not os.path.exists(MEMORY_FILE):
        return {"success": 0, "fail": 0}

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    success = sum(1 for e in data if e["result"] == "success")
    fail = sum(1 for e in data if e["result"] == "fail")
    return {"success": success, "fail": fail}

if __name__ == "__main__":
    log_event("Module1", "parse_deposits", "success", "Deposits parsed correctly.")
    log_event("Module2", "parse_credits", "fail", "Formatting issue detected.")
    print(get_summary())