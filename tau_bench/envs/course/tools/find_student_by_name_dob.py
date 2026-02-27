# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindStudentByNameDob(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], first_name: str, last_name: str, dob: str
    ) -> str:
        students = data["students"]
        for student_id, profile in students.items():
            if (
                profile["name"]["first_name"].lower() == first_name.lower()
                and profile["name"]["last_name"].lower() == last_name.lower()
                and profile["dob"] == dob
            ):
                return student_id
        return "Error: student not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_student_by_name_dob",
                "description": (
                    "Find student id by first name, last name, and date of birth. If the student is not found, "
                    "the function will return an error message. By default, find student id by email, and only "
                    "call this function if the student cannot be found by email or does not remember their email."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {
                            "type": "string",
                            "description": "The first name of the student, such as 'John'.",
                        },
                        "last_name": {
                            "type": "string",
                            "description": "The last name of the student, such as 'Doe'.",
                        },
                        "dob": {
                            "type": "string",
                            "description": "The date of birth of the student in the format 'YYYY-MM-DD', such as '2000-01-15'.",
                        },
                    },
                    "required": ["first_name", "last_name", "dob"],
                },
            },
        }
