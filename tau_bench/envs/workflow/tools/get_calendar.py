# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetCalendar(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, date: str = "") -> str:
        events = data["calendar_events"]
        results = []
        for event in events:
            if employee_id in event.get("attendees", []) or event.get("organizer") == employee_id:
                if date and event["date"] != date:
                    continue
                results.append(event)
        if not results:
            return "No calendar events found."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_calendar",
                "description": "Get calendar events for an employee. Optionally filter by a specific date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "string",
                            "description": "The employee ID, e.g. 'EMP001'.",
                        },
                        "date": {
                            "type": "string",
                            "description": "Optional date filter in YYYY-MM-DD format. Leave empty for all upcoming events.",
                        },
                    },
                    "required": ["employee_id"],
                },
            },
        }
