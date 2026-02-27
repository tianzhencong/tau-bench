# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CancelAppointment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], appointment_id: str, reason: str) -> str:
        appointments = data["appointments"]
        if appointment_id not in appointments:
            return "Error: appointment not found"

        appointment = appointments[appointment_id]
        appointment["status"] = "cancelled"

        return json.dumps(
            {
                "appointment_id": appointment_id,
                "status": "cancelled",
                "reason": reason,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_appointment",
                "description": (
                    "Cancel a scheduled appointment. Only appointments with 'scheduled' status can be cancelled. "
                    "The agent must verify cancellation fee policies before calling this tool. "
                    "This tool does NOT enforce cancellation fee rules."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "string",
                            "description": "The appointment id, such as 'APT00001'.",
                        },
                        "reason": {
                            "type": "string",
                            "description": "The reason for cancellation.",
                        },
                    },
                    "required": ["appointment_id", "reason"],
                },
            },
        }
