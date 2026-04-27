import json

DB_CONFIG = {
    "dbname": "snake_db",
    "user": "robloxgod",
    "host": "", 
    "password": ""
}

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"snake_color": (0, 255, 0), "grid": True, "sound": True}

def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)