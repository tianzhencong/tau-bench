# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListDepartments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        courses = data["courses"]
        departments = sorted(
            set(course["department"] for course in courses.values())
        )
        return json.dumps(departments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_departments",
                "description": "List all academic departments that offer courses.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
