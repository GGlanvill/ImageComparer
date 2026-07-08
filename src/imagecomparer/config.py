from pathlib import Path

APP_FOLDER = Path.home() / ".imagecomparer"

APP_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

SETTINGS_FILE = APP_FOLDER / "settings.json"
