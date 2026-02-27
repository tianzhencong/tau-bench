# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class TransferFunds(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        from_account_id: str,
        to_account_id: str,
        amount: float,
    ) -> str:
        accounts = data["accounts"]

        if from_account_id not in accounts:
            return "Error: source account not found"
        if to_account_id not in accounts:
            return "Error: destination account not found"

        from_account = accounts[from_account_id]
        to_account = accounts[to_account_id]

        if amount > from_account["cash_balance"]:
            return "Error: insufficient cash balance in source account"

        from_account["cash_balance"] = round(
            from_account["cash_balance"] - amount, 2
        )
        to_account["cash_balance"] = round(
            to_account["cash_balance"] + amount, 2
        )

        return json.dumps(
            {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "amount": amount,
                "from_new_balance": from_account["cash_balance"],
                "to_new_balance": to_account["cash_balance"],
                "status": "completed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_funds",
                "description": (
                    "Transfer cash between two accounts. "
                    "The agent must verify IRA contribution limits and withdrawal penalties before calling this function."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_account_id": {
                            "type": "string",
                            "description": "The source account id, such as 'A5001'.",
                        },
                        "to_account_id": {
                            "type": "string",
                            "description": "The destination account id, such as 'A5002'.",
                        },
                        "amount": {
                            "type": "number",
                            "description": "The amount to transfer.",
                        },
                    },
                    "required": ["from_account_id", "to_account_id", "amount"],
                },
            },
        }
