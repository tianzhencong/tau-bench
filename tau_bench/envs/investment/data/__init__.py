# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "securities.json")) as f:
        securities = json.load(f)
    with open(os.path.join(FOLDER_PATH, "clients.json")) as f:
        clients = json.load(f)
    with open(os.path.join(FOLDER_PATH, "accounts.json")) as f:
        accounts = json.load(f)
    return {
        "securities": securities,
        "clients": clients,
        "accounts": accounts,
    }
