# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindClientByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        clients = data["clients"]
        for client_id, profile in clients.items():
            if profile["email"].lower() == email.lower():
                return client_id
        return "Error: client not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_client_by_email",
                "description": "Find client id by email address. If the client is not found, the function will return an error message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email of the client, such as 'john.doe@example.com'.",
                        },
                    },
                    "required": ["email"],
                },
            },
        }
