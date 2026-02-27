# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetTransactionHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str) -> str:
        accounts = data["accounts"]
        if account_id not in accounts:
            return "Error: account not found"

        account = accounts[account_id]
        history = [
            order
            for order in account["pending_orders"]
            if order["status"] in ("executed", "cancelled")
        ]

        if not history:
            return "No transaction history found for this account."
        return json.dumps(history)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_transaction_history",
                "description": "Get the transaction history for an account, including all executed and cancelled orders.",
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
