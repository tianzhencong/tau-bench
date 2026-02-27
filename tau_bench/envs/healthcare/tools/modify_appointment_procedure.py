# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ModifyAppointmentProcedure(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        appointment_id: str,
        new_procedure_id: str,
        payment_method: str,
    ) -> str:
        appointments = data["appointments"]
        procedures = data["procedures"]

        if appointment_id not in appointments:
            return "Error: appointment not found"

        appointment = appointments[appointment_id]
        if appointment["status"] != "scheduled":
            return f"Error: appointment status is '{appointment['status']}', only scheduled appointments can be modified"

        if new_procedure_id not in procedures:
            return "Error: procedure not found"

        new_procedure = procedures[new_procedure_id]

        appointment["procedure_id"] = new_procedure_id
        appointment["procedure_name"] = new_procedure["name"]
        appointment["department"] = new_procedure["department"]
        appointment["total_cost"] = new_procedure["base_cost"]
        appointment["payment_method"] = payment_method

        return json.dumps(appointment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_appointment_procedure",
                "description": (
                    "Change the procedure for an existing appointment. Updates costs based on the new procedure's base cost. "
                    "Only scheduled appointments can be modified. The agent must verify referral requirements. "
                    "This tool does NOT check referrals."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "string",
                            "description": "The appointment id, such as 'APT00001'.",
                        },
                        "new_procedure_id": {
                            "type": "string",
                            "description": "The new procedure id, such as 'PROC003'.",
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "The payment method id, such as 'cc_P10001_1234'.",
                        },
                    },
                    "required": ["appointment_id", "new_procedure_id", "payment_method"],
                },
            },
        }
