# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindClientByNameDob(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], first_name: str, last_name: str, dob: str
    ) -> str:
        clients = data["clients"]
        for client_id, profile in clients.items():
            if (
                profile["name"]["first_name"].lower() == first_name.lower()
                and profile["name"]["last_name"].lower() == last_name.lower()
                and profile["dob"] == dob
            ):
                return client_id
        return "Error: client not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_client_by_name_dob",
                "description": (
                    "Find client id by first name, last name, and date of birth. If the client is not found, "
                    "the function will return an error message. By default, find client id by email, and only "
                    "call this function if the client cannot be found by email or does not remember their email."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {
                            "type": "string",
                            "description": "The first name of the client, such as 'John'.",
                        },
                        "last_name": {
                            "type": "string",
                            "description": "The last name of the client, such as 'Doe'.",
                        },
                        "dob": {
                            "type": "string",
                            "description": "The date of birth of the client in the format 'YYYY-MM-DD', such as '1990-01-15'.",
                        },
                    },
                    "required": ["first_name", "last_name", "dob"],
                },
            },
        }
