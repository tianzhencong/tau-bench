# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "courses.json")) as f:
        course_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "registrations.json")) as f:
        registration_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "students.json")) as f:
        student_data = json.load(f)
    return {
        "courses": course_data,
        "registrations": registration_data,
        "students": student_data,
    }
