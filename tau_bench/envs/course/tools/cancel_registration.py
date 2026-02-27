# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CancelRegistration(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], registration_id: str, reason: str) -> str:
        registrations = data["registrations"]
        if registration_id not in registrations:
            return "Error: registration not found"

        registration = registrations[registration_id]
        registration["status"] = "cancelled"
        registration["cancel_reason"] = reason

        return json.dumps(
            {
                "registration_id": registration_id,
                "status": "cancelled",
                "total_tuition": registration["total_tuition"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_registration",
                "description": (
                    "Cancel a course registration. Note: the API does not verify refund policy rules "
                    "(refund eligibility, timing restrictions). The agent must verify these before calling. "
                    "The agent needs to explain the cancellation detail and ask for explicit user confirmation "
                    "(yes/no) to proceed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "registration_id": {
                            "type": "string",
                            "description": "The registration id to cancel, such as 'REGGV6TOLA'.",
                        },
                        "reason": {
                            "type": "string",
                            "description": "The reason for cancellation.",
                        },
                    },
                    "required": ["registration_id", "reason"],
                },
            },
        }
