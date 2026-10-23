
import json
from pathlib import Path
from difflib import SequenceMatcher

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = PROJECT_ROOT / "data" / "generated_history.json"

def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []

def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2, ensure_ascii=False)

def get_item_text(item):
    return (
        item.get("question")
        or item.get("statement")
        or item.get("sentence")
        or item.get("prompt")
        or ""
    )

def save_item_to_history(item):
    history = load_history()
    history.append(item)
    save_history(history)

def get_previous_questions(sport=None, limit=25):
    history = load_history()

    if sport:
        history = [
            item for item in history
            if item.get("sport") == sport
        ]

    history = history[-limit:]

    questions = []

    for item in history:
        text = get_item_text(item)
        if text:
            questions.append(text)

    return "\n".join(f"- {q}" for q in questions)

def similarity_score(text1, text2):
    return SequenceMatcher(
        None,
        text1.lower().strip(),
        text2.lower().strip()
    ).ratio()

def is_duplicate_item(item, threshold=0.80):
    new_text = get_item_text(item)

    if not new_text:
        return False

    history = load_history()

    for old_item in history:
        old_text = get_item_text(old_item)

        if old_text and similarity_score(new_text, old_text) >= threshold:
            return True

    return False

def clear_history():
    save_history([])
