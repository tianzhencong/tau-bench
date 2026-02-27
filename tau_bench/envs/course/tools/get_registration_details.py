# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetRegistrationDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], registration_id: str) -> str:
        registrations = data["registrations"]
        if registration_id in registrations:
            return json.dumps(registrations[registration_id])
        return "Error: registration not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_registration_details",
                "description": "Get the details of a course registration, including enrolled courses, schedule, payment history, and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "registration_id": {
                            "type": "string",
                            "description": "The registration id, such as 'REGGV6TOLA'.",
                        },
                    },
                    "required": ["registration_id"],
                },
            },
        }
