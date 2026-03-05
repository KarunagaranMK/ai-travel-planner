import json
from pathlib import Path

DATA_FILE = Path("backend/data/trips.json")

def load_memory():
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text())

def save_memory(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=4))