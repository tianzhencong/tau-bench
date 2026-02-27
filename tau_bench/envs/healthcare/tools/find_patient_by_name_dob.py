# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindPatientByNameDob(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], first_name: str, last_name: str, dob: str
    ) -> str:
        patients = data["patients"]
        for patient_id, profile in patients.items():
            if (
                profile["name"]["first_name"].lower() == first_name.lower()
                and profile["name"]["last_name"].lower() == last_name.lower()
                and profile["dob"] == dob
            ):
                return patient_id
        return "Error: patient not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_patient_by_name_dob",
                "description": (
                    "Find patient id by first name, last name, and date of birth. If the patient is not found, "
                    "the function will return an error message. By default, find patient id by email, and only "
                    "call this function if the patient cannot be found by email or does not remember their email."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {
                            "type": "string",
                            "description": "The first name of the patient, such as 'John'.",
                        },
                        "last_name": {
                            "type": "string",
                            "description": "The last name of the patient, such as 'Doe'.",
                        },
                        "dob": {
                            "type": "string",
                            "description": "The date of birth of the patient in the format 'YYYY-MM-DD', such as '1990-01-15'.",
                        },
                    },
                    "required": ["first_name", "last_name", "dob"],
                },
            },
        }
