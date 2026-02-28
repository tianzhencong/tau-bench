# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetEmployeeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str) -> str:
        employees = data["employees"]
        if employee_id in employees:
            return json.dumps(employees[employee_id])
        return "Error: employee not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_details",
                "description": "Get detailed information about an employee by their employee ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "string",
                            "description": "The employee ID, e.g. 'EMP001'.",
                        },
                    },
                    "required": ["employee_id"],
                },
            },
        }
