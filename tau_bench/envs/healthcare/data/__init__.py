# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "procedures.json")) as f:
        procedures = json.load(f)
    with open(os.path.join(FOLDER_PATH, "specialists.json")) as f:
        specialists = json.load(f)
    with open(os.path.join(FOLDER_PATH, "patients.json")) as f:
        patients = json.load(f)
    with open(os.path.join(FOLDER_PATH, "appointments.json")) as f:
        appointments = json.load(f)
    return {
        "procedures": procedures,
        "specialists": specialists,
        "patients": patients,
        "appointments": appointments,
    }
