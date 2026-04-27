import json

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Настройки по умолчанию
        return {"sound": True, "car_color": "Red", "difficulty": "Medium"}

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": int(distance)})
    # Сортировка по очкам (от большего к меньшему) и топ-10
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    with open("leaderboard.json", "w") as f:
        json.dump(lb, f, indent=4)