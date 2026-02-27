# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DropCourses(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        registration_id: str,
        course_ids: List[str],
        payment_id: str,
    ) -> str:
        registrations = data["registrations"]
        if registration_id not in registrations:
            return "Error: registration not found"

        registration = registrations[registration_id]

        if registration["status"] != "confirmed":
            return f"Error: registration status is '{registration['status']}', only confirmed registrations can have courses dropped"

        registered_course_ids = [c["course_id"] for c in registration["courses"]]
        for cid in course_ids:
            if cid not in registered_course_ids:
                return f"Error: course {cid} not found in registration"

        remaining = [
            c for c in registration["courses"] if c["course_id"] not in course_ids
        ]
        if len(remaining) < 1:
            return "Error: cannot drop all courses, at least one course must remain. Use cancel_registration instead."

        dropped = [
            c for c in registration["courses"] if c["course_id"] in course_ids
        ]

        registration["courses"] = remaining
        registration["total_credits"] = sum(c["credits"] for c in remaining)
        registration["total_tuition"] = sum(c["tuition"] for c in remaining)

        return json.dumps(
            {
                "registration_id": registration_id,
                "dropped_courses": [
                    {"course_id": c["course_id"], "course_name": c["course_name"]}
                    for c in dropped
                ],
                "remaining_courses": len(remaining),
                "new_total_credits": registration["total_credits"],
                "new_total_tuition": registration["total_tuition"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "drop_courses",
                "description": (
                    "Drop specific courses from a confirmed registration. At least one course must remain "
                    "in the registration. Note: the API does not verify refund policy rules. The agent must "
                    "verify refund eligibility before calling. The agent needs to explain the drop detail "
                    "and ask for explicit user confirmation (yes/no) to proceed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "registration_id": {
                            "type": "string",
                            "description": "The registration id, such as 'REGGV6TOLA'.",
                        },
                        "course_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of course ids to drop, such as ['CS120', 'MATH101'].",
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "The payment method id for any refund, such as 'credit_card_9531021' or 'student_account_S10000'.",
                        },
                    },
                    "required": ["registration_id", "course_ids", "payment_id"],
                },
            },
        }
