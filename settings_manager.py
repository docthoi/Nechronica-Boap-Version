# settings_manager.py

import json
import os

SETTINGS_FILE = "config.json"

def save_settings(settings):
    """
    Saves a dictionary of settings to a JSON file.

    Args:
        settings (dict): A dictionary containing the settings to save.
    """
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        print("Settings saved successfully.")
    except IOError as e:
        print(f"Error saving settings: {e}")

def load_settings():
    """
    Loads settings from a JSON file.

    Returns:
        dict: A dictionary of loaded settings, or a default dictionary
              if the file does not exist or an error occurs.
    """
    default_settings = {
        "resolution": "800x600",
        "mode": "Windowed"
    }
    
    if not os.path.exists(SETTINGS_FILE):
        print("Settings file not found. Using default settings.")
        return default_settings

    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        print("Settings loaded successfully.")
        return settings
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading settings file: {e}. Using default settings.")
        return default_settings

