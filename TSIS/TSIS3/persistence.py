import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "medium"
}


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []


def save_leaderboard(entries):
    # Sort by score descending and keep top 10
    entries.sort(key=lambda x: x["score"], reverse=True)
    top10 = entries[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(top10, f, indent=2)
    return top10


def add_to_leaderboard(name, score, distance):
    entries = load_leaderboard()
    entries.append({"name": name, "score": score, "distance": int(distance)})
    return save_leaderboard(entries)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            # Fill in missing keys
            for key, val in DEFAULT_SETTINGS.items():
                if key not in data:
                    data[key] = val
            return data
    except:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)