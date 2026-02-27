# Copyright Sierra

import json
import random
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class PlaceSellOrder(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], account_id: str, holding_id: str, quantity: int
    ) -> str:
        accounts = data["accounts"]
        securities = data["securities"]

        if account_id not in accounts:
            return "Error: account not found"
        account = accounts[account_id]

        holding = None
        holding_index = None
        for i, h in enumerate(account["holdings"]):
            if h["holding_id"] == holding_id:
                holding = h
                holding_index = i
                break

        if holding is None:
            return "Error: holding not found in account"

        if quantity > holding["quantity"]:
            return "Error: insufficient holding quantity"

        security_id = holding["security_id"]
        current_price = securities[security_id]["current_price"]
        proceeds = round(quantity * current_price, 2)

        account["cash_balance"] = round(account["cash_balance"] + proceeds, 2)

        holding["quantity"] -= quantity
        if holding["quantity"] == 0:
            account["holdings"].pop(holding_index)

        order_id = f"ORD{random.randint(100000, 999999)}"
        order = {
            "order_id": order_id,
            "account_id": account_id,
            "security_id": security_id,
            "order_type": "sell",
            "quantity": quantity,
            "price": current_price,
            "status": "executed",
            "created_at": "2026-02-27",
        }
        account["pending_orders"].append(order)

        return json.dumps(
            {
                "order_id": order_id,
                "account_id": account_id,
                "holding_id": holding_id,
                "security_id": security_id,
                "security_name": holding["security_name"] if holding["quantity"] > 0 else securities[security_id]["name"],
                "quantity": quantity,
                "price_per_unit": current_price,
                "proceeds": proceeds,
                "status": "executed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "place_sell_order",
                "description": (
                    "Place a sell order for a holding in a given account. "
                    "The order will be executed immediately at the current market price. "
                    "The agent must verify that the holding belongs to the correct account before calling this function."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                        "holding_id": {
                            "type": "string",
                            "description": "The holding id, such as 'H1001'.",
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "The number of units to sell.",
                        },
                    },
                    "required": ["account_id", "holding_id", "quantity"],
                },
            },
        }
