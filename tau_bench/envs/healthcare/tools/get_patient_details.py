# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetPatientDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], patient_id: str) -> str:
        patients = data["patients"]
        if patient_id in patients:
            return json.dumps(patients[patient_id])
        return "Error: patient not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_patient_details",
                "description": "Get the details of a patient, including their name, email, date of birth, phone, insurance plan, payment methods, deductible status, primary care doctor, medical history, referrals, dependents, and appointment IDs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "The patient id, such as 'P10001'.",
                        },
                    },
                    "required": ["patient_id"],
                },
            },
        }
