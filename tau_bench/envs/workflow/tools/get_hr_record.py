# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetHrRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str) -> str:
        hr_records = data["hr_records"]
        if employee_id in hr_records:
            return json.dumps(hr_records[employee_id])
        return "Error: HR record not found for this employee"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_hr_record",
                "description": "Get the HR record for an employee, including leave balance, performance rating, and salary band.",
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
