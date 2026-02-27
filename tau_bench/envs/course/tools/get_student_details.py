# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetStudentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], student_id: str) -> str:
        students = data["students"]
        if student_id in students:
            return json.dumps(students[student_id])
        return "Error: student not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_student_details",
                "description": "Get the details of a student, including their profile, payment methods, completed courses, and registration ids.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "student_id": {
                            "type": "string",
                            "description": "The student id, such as 'S10000'.",
                        },
                    },
                    "required": ["student_id"],
                },
            },
        }
