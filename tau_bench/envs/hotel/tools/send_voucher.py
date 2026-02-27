# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class SendVoucher(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, amount: int) -> str:
        users = data["users"]
        if user_id not in users:
            return "Error: user not found"
        if amount <= 0:
            return "Error: amount must be positive"

        voucher_id = f"voucher_{hash(user_id + str(amount)) % 10000000:07d}"
        users[user_id]["payment_methods"].append(
            {
                "payment_id": voucher_id,
                "type": "gift_card",
                "balance": amount,
            }
        )
        return json.dumps(
            {
                "voucher_id": voucher_id,
                "amount": amount,
                "user_id": user_id,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_voucher",
                "description": "Send a compensation voucher (gift card) to a user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id.",
                        },
                        "amount": {
                            "type": "integer",
                            "description": "The voucher amount in dollars.",
                        },
                    },
                    "required": ["user_id", "amount"],
                },
            },
        }
