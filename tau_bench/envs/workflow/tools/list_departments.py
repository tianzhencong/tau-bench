# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListDepartments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        employees = data["employees"]
        departments = sorted(set(emp["department"] for emp in employees.values()))
        return json.dumps(departments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_departments",
                "description": "List all departments in the organization.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
