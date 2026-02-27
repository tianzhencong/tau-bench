# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetClientDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str) -> str:
        clients = data["clients"]
        if client_id in clients:
            return json.dumps(clients[client_id])
        return "Error: client not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_client_details",
                "description": "Get the details of a client, including their name, email, date of birth, phone, tier, and account IDs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {
                            "type": "string",
                            "description": "The client id, such as 'C1001'.",
                        },
                    },
                    "required": ["client_id"],
                },
            },
        }
