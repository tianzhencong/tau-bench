# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class BookAppointment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        patient_id: str,
        procedure_id: str,
        specialist_id: str,
        date: str,
        start_time: str,
        payment_method: str,
    ) -> str:
        patients = data["patients"]
        procedures = data["procedures"]
        specialists = data["specialists"]
        appointments = data["appointments"]

        if patient_id not in patients:
            return "Error: patient not found"
        if procedure_id not in procedures:
            return "Error: procedure not found"
        if specialist_id not in specialists:
            return "Error: specialist not found"

        specialist = specialists[specialist_id]
        procedure = procedures[procedure_id]

        hours, minutes = map(int, start_time.split(":"))
        total_minutes = hours * 60 + minutes + procedure["duration_minutes"]
        end_time = f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

        appointment_id = "APT" + hashlib.md5(
            f"{patient_id}_{procedure_id}_{date}_{start_time}".encode()
        ).hexdigest()[:8]

        appointment = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "procedure_id": procedure_id,
            "procedure_name": procedure["name"],
            "specialist_id": specialist_id,
            "specialist_name": specialist["name"],
            "department": procedure["department"],
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "status": "scheduled",
            "copay_amount": 0,
            "insurance_covered": 0,
            "total_cost": procedure["base_cost"],
            "payment_method": payment_method,
            "referral_id": None,
            "created_at": "2024-09-15T10:00:00",
        }

        for s in specialist["available_slots"]:
            if s["date"] == date and s["start_time"] == start_time:
                s["available"] = False
                break

        appointments[appointment_id] = appointment
        patients[patient_id]["appointments"].append(appointment_id)

        return json.dumps(appointment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "book_appointment",
                "description": (
                    "Book a new appointment for a patient. The agent must verify referral requirements, "
                    "time conflicts, and insurance calculations before calling this tool. "
                    "This tool does NOT check referrals, time conflicts, or calculate insurance."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "The patient id, such as 'P10001'.",
                        },
                        "procedure_id": {
                            "type": "string",
                            "description": "The procedure id, such as 'PROC001'.",
                        },
                        "specialist_id": {
                            "type": "string",
                            "description": "The specialist id, such as 'DR001'.",
                        },
                        "date": {
                            "type": "string",
                            "description": "The appointment date in 'YYYY-MM-DD' format.",
                        },
                        "start_time": {
                            "type": "string",
                            "description": "The start time in 'HH:MM' format, such as '09:00'.",
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "The payment method id from the patient's profile, such as 'cc_P10001_1234' or 'hsa_P10001'.",
                        },
                    },
                    "required": [
                        "patient_id",
                        "procedure_id",
                        "specialist_id",
                        "date",
                        "start_time",
                        "payment_method",
                    ],
                },
            },
        }
