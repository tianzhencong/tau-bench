# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddHsaCredit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], patient_id: str, amount: float) -> str:
        patients = data["patients"]
        if patient_id not in patients:
            return "Error: patient not found"

        patient = patients[patient_id]
        hsa_account = None
        for pm in patient["payment_methods"]:
            if pm["type"] == "hsa":
                hsa_account = pm
                break

        if hsa_account is None:
            return "Error: patient does not have an HSA account"

        hsa_account["balance"] = round(hsa_account["balance"] + amount, 2)

        return json.dumps(
            {
                "patient_id": patient_id,
                "credit_amount": amount,
                "new_hsa_balance": hsa_account["balance"],
                "status": "success",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_hsa_credit",
                "description": "Add a credit (compensation) to a patient's HSA account balance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "The patient id, such as 'P10001'.",
                        },
                        "amount": {
                            "type": "number",
                            "description": "The credit amount in dollars to add to the HSA account.",
                        },
                    },
                    "required": ["patient_id", "amount"],
                },
            },
        }
