# Copyright Sierra

import json
import hashlib
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class PlaceBuyOrder(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], account_id: str, security_id: str, quantity: int
    ) -> str:
        accounts = data["accounts"]
        securities = data["securities"]

        if account_id not in accounts:
            return "Error: account not found"
        account = accounts[account_id]

        if account["type"] == "savings":
            return "Error: cannot place orders on a savings account"

        if security_id not in securities:
            return "Error: security not found"
        security = securities[security_id]

        current_price = security["current_price"]
        total_cost = round(quantity * current_price, 2)

        det_seed = f"{account_id}_{security_id}_{quantity}"
        h = hashlib.md5(det_seed.encode()).hexdigest()
        holding_id = f"H{h[:8].upper()}"
        order_id = f"ORD{h[8:16].upper()}"

        account["cash_balance"] = round(account["cash_balance"] - total_cost, 2)

        account["holdings"].append(
            {
                "holding_id": holding_id,
                "security_id": security_id,
                "security_name": security["name"],
                "quantity": quantity,
                "average_cost_basis": current_price,
                "purchase_date": "2026-02-27",
            }
        )

        order = {
            "order_id": order_id,
            "account_id": account_id,
            "security_id": security_id,
            "order_type": "buy",
            "quantity": quantity,
            "price": current_price,
            "status": "executed",
            "created_at": "2026-02-27",
        }
        account["pending_orders"].append(order)

        return json.dumps(
            {
                "order_id": order_id,
                "holding_id": holding_id,
                "account_id": account_id,
                "security_id": security_id,
                "security_name": security["name"],
                "quantity": quantity,
                "price_per_unit": current_price,
                "total_cost": total_cost,
                "status": "executed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "place_buy_order",
                "description": (
                    "Place a buy order for a security in a given account. "
                    "The order will be executed immediately at the current market price. "
                    "The agent must verify that the security is active (not halted/delisted) and that "
                    "the account has sufficient cash balance before calling this function."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                        "security_id": {
                            "type": "string",
                            "description": "The security id, such as 'SEC1001'.",
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "The number of units to buy.",
                        },
                    },
                    "required": ["account_id", "security_id", "quantity"],
                },
            },
        }
