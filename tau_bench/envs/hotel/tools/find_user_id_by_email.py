# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindUserIdByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data["users"]
        for user_id, user in users.items():
            if user.get("email", "").lower() == email.lower():
                return json.dumps({"user_id": user_id})
        return "Error: user not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_user_id_by_email",
                "description": "Find user id by email address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email address of the user.",
                        },
                    },
                    "required": ["email"],
                },
            },
        }
