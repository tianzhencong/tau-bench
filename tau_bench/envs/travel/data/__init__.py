# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "packages.json")) as f:
        packages = json.load(f)
    with open(os.path.join(FOLDER_PATH, "clients.json")) as f:
        clients = json.load(f)
    with open(os.path.join(FOLDER_PATH, "bookings.json")) as f:
        bookings = json.load(f)
    return {
        "packages": packages,
        "clients": clients,
        "bookings": bookings,
    }
