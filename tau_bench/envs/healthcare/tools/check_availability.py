# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CheckAvailability(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], specialist_id: str, date: str) -> str:
        specialists = data["specialists"]
        if specialist_id not in specialists:
            return "Error: specialist not found"
        specialist = specialists[specialist_id]
        available_slots = [
            slot
            for slot in specialist["available_slots"]
            if slot["date"] == date and slot["available"]
        ]
        if not available_slots:
            return f"No available slots for {specialist['name']} on {date}."
        return json.dumps(available_slots)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_availability",
                "description": "Check available time slots for a specialist on a specific date. Returns a list of available slots.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "specialist_id": {
                            "type": "string",
                            "description": "The specialist id, such as 'DR001'.",
                        },
                        "date": {
                            "type": "string",
                            "description": "The date to check availability for, in the format 'YYYY-MM-DD', such as '2024-09-20'.",
                        },
                    },
                    "required": ["specialist_id", "date"],
                },
            },
        }
