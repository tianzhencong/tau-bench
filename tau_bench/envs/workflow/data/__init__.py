# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "workspace_data.json")) as f:
        return json.load(f)
