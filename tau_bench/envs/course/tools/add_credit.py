# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddCredit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], student_id: str, amount: int) -> str:
        students = data["students"]
        if student_id not in students:
            return "Error: student not found"

        student = students[student_id]
        for pm in student["payment_methods"]:
            if pm["type"] == "student_account":
                pm["balance"] += amount
                return json.dumps(
                    {
                        "student_id": student_id,
                        "payment_id": pm["payment_id"],
                        "new_balance": pm["balance"],
                    }
                )
        return "Error: student account not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_credit",
                "description": "Add a credit (compensation) to a student's student account balance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "student_id": {
                            "type": "string",
                            "description": "The student id, such as 'S10000'.",
                        },
                        "amount": {
                            "type": "integer",
                            "description": "The credit amount in dollars to add to the student account.",
                        },
                    },
                    "required": ["student_id", "amount"],
                },
            },
        }
