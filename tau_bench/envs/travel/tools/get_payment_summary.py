# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetPaymentSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str) -> str:
        clients = data["clients"]
        if client_id not in clients:
            return "Error: client not found"

        client = clients[client_id]
        return json.dumps(
            {
                "client_id": client_id,
                "payment_methods": client.get("payment_methods", []),
                "loyalty_points": client.get("loyalty_points", 0),
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payment_summary",
                "description": "Get all payment methods and loyalty points balance for a client.",
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
