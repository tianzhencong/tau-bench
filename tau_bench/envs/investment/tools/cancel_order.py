# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CancelOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str, account_id: str) -> str:
        accounts = data["accounts"]
        securities = data["securities"]

        if account_id not in accounts:
            return "Error: account not found"
        account = accounts[account_id]

        order = None
        for o in account["pending_orders"]:
            if o["order_id"] == order_id:
                order = o
                break

        if order is None:
            return "Error: order not found in account"

        if order["status"] != "pending":
            return f"Error: order status is '{order['status']}', only pending orders can be cancelled"

        order["status"] = "cancelled"

        if order["order_type"] == "buy":
            refund = round(order["quantity"] * order["price"], 2)
            account["cash_balance"] = round(account["cash_balance"] + refund, 2)

        if order["order_type"] == "sell":
            holding = None
            for h in account["holdings"]:
                if h["security_id"] == order["security_id"]:
                    holding = h
                    break
            if holding is not None:
                holding["quantity"] += order["quantity"]
            else:
                security = securities[order["security_id"]]
                account["holdings"].append(
                    {
                        "holding_id": f"H_restored_{order_id}",
                        "security_id": order["security_id"],
                        "security_name": security["name"],
                        "quantity": order["quantity"],
                        "average_cost_basis": order["price"],
                        "purchase_date": "restored",
                    }
                )

        return json.dumps(
            {
                "order_id": order_id,
                "account_id": account_id,
                "status": "cancelled",
                "order_type": order["order_type"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_order",
                "description": (
                    "Cancel a pending order in an account. Only orders with 'pending' status can be cancelled. "
                    "For buy orders, the cash will be refunded. For sell orders, the holding quantity will be restored."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order id, such as 'ORD100001'.",
                        },
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                    },
                    "required": ["order_id", "account_id"],
                },
            },
        }
