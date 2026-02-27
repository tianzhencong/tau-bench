# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddLoyaltyPoints(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str, points: int) -> str:
        clients = data["clients"]
        if client_id not in clients:
            return "Error: client not found"

        client = clients[client_id]
        client["loyalty_points"] = client.get("loyalty_points", 0) + points

        return json.dumps(
            {
                "client_id": client_id,
                "points_added": points,
                "new_balance": client["loyalty_points"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_loyalty_points",
                "description": "Add loyalty points to a client's account. Returns the updated points balance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {
                            "type": "string",
                            "description": "The client id, such as 'C1001'.",
                        },
                        "points": {
                            "type": "integer",
                            "description": "The number of loyalty points to add.",
                        },
                    },
                    "required": ["client_id", "points"],
                },
            },
        }
