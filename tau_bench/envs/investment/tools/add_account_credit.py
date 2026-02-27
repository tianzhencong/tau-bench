# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddAccountCredit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str, amount: float) -> str:
        accounts = data["accounts"]
        if account_id not in accounts:
            return "Error: account not found"

        account = accounts[account_id]
        account["cash_balance"] = round(account["cash_balance"] + amount, 2)

        return json.dumps(
            {
                "account_id": account_id,
                "credit_amount": amount,
                "new_cash_balance": account["cash_balance"],
                "status": "success",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_account_credit",
                "description": "Add a cash credit (compensation) to an account's cash balance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                        "amount": {
                            "type": "number",
                            "description": "The credit amount in dollars to add to the account.",
                        },
                    },
                    "required": ["account_id", "amount"],
                },
            },
        }
