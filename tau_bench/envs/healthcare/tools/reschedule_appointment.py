# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class RescheduleAppointment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        appointment_id: str,
        new_specialist_id: str,
        new_date: str,
        new_start_time: str,
    ) -> str:
        appointments = data["appointments"]
        specialists = data["specialists"]
        procedures = data["procedures"]

        if appointment_id not in appointments:
            return "Error: appointment not found"

        appointment = appointments[appointment_id]
        if appointment["status"] != "scheduled":
            return f"Error: appointment status is '{appointment['status']}', only scheduled appointments can be rescheduled"

        if new_specialist_id not in specialists:
            return "Error: specialist not found"

        new_specialist = specialists[new_specialist_id]
        procedure = procedures[appointment["procedure_id"]]

        hours, minutes = map(int, new_start_time.split(":"))
        total_minutes = hours * 60 + minutes + procedure["duration_minutes"]
        new_end_time = f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

        old_specialist = specialists[appointment["specialist_id"]]
        for s in old_specialist["available_slots"]:
            if s["date"] == appointment["date"] and s["start_time"] == appointment["start_time"]:
                s["available"] = True
                break

        for s in new_specialist["available_slots"]:
            if s["date"] == new_date and s["start_time"] == new_start_time:
                s["available"] = False
                break

        appointment["specialist_id"] = new_specialist_id
        appointment["specialist_name"] = new_specialist["name"]
        appointment["date"] = new_date
        appointment["start_time"] = new_start_time
        appointment["end_time"] = new_end_time

        return json.dumps(appointment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "reschedule_appointment",
                "description": (
                    "Reschedule an existing appointment to a new date/time with a (possibly different) specialist. "
                    "Only scheduled appointments can be rescheduled. The agent must check for time conflicts. "
                    "This tool does NOT check time conflicts."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "string",
                            "description": "The appointment id, such as 'APT00001'.",
                        },
                        "new_specialist_id": {
                            "type": "string",
                            "description": "The specialist id for the rescheduled appointment, such as 'DR001'.",
                        },
                        "new_date": {
                            "type": "string",
                            "description": "The new date in 'YYYY-MM-DD' format.",
                        },
                        "new_start_time": {
                            "type": "string",
                            "description": "The new start time in 'HH:MM' format, such as '09:00'.",
                        },
                    },
                    "required": ["appointment_id", "new_specialist_id", "new_date", "new_start_time"],
                },
            },
        }
