# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetAccountDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str) -> str:
        accounts = data["accounts"]
        if account_id in accounts:
            return json.dumps(accounts[account_id])
        return "Error: account not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_account_details",
                "description": "Get the full details of an account, including holdings, pending orders, settings, and cash balance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                    },
                    "required": ["account_id"],
                },
            },
        }
