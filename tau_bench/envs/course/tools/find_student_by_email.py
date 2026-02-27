# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindStudentByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        students = data["students"]
        for student_id, profile in students.items():
            if profile["email"].lower() == email.lower():
                return student_id
        return "Error: student not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_student_by_email",
                "description": "Find student id by email address. If the student is not found, the function will return an error message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email of the student, such as 'john.doe@university.edu'.",
                        },
                    },
                    "required": ["email"],
                },
            },
        }
