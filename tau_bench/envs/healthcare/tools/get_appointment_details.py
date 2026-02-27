# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetAppointmentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], appointment_id: str) -> str:
        appointments = data["appointments"]
        if appointment_id in appointments:
            return json.dumps(appointments[appointment_id])
        return "Error: appointment not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_appointment_details",
                "description": "Get the details of an appointment, including patient, procedure, specialist, date/time, status, cost breakdown, and payment method.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "string",
                            "description": "The appointment id, such as 'APT00001'.",
                        },
                    },
                    "required": ["appointment_id"],
                },
            },
        }
