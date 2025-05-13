import logging

from prompt_toolkit.styles import Style

logging.basicConfig(level=logging.INFO)

FACULTIES_URL = "https://vsu.by/studentam/raspisanie-zanyatij.html"
BASE_URL = "https://vsu.by{urn}"

DATA_FOLDER = "data"

STYLE = Style.from_dict(
    {
        "dialog": "bg:#000000 fg:#8d9ea5",
        "button": "bg:#8d9ea5",
        "button.focused": "bg:#316d92",
        "button.arrow": "fg:#316d92",
        "te" "checkbox": "fg:#8d9ea5",
        "checkbox-checked": "#316d92",
        "checkbox-list": "#8d9ea5",
        "radio": "fg:#8d9ea5",
        "radio-checked": "#316d92",
        "radio-list": "#8d9ea5",
        "dialog.body": "bg:#031019",
        "dialog shadow": "bg:#000000",
        "frame.label": "fg:#316d92",
        "dialog.body label": "fg:#316d92",
    }
)

try:
    from local_settings import *
except ImportError:
    pass
