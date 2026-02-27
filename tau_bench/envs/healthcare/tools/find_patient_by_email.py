# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindPatientByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        patients = data["patients"]
        for patient_id, profile in patients.items():
            if profile["email"].lower() == email.lower():
                return patient_id
        return "Error: patient not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_patient_by_email",
                "description": "Find patient id by email address. If the patient is not found, the function will return an error message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email of the patient, such as 'john.doe@example.com'.",
                        },
                    },
                    "required": ["email"],
                },
            },
        }
