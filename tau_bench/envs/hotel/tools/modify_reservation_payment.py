# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyReservationPayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        new_payment_methods: List[Dict[str, Any]],
    ) -> str:
        reservations = data["reservations"]
        users = data["users"]

        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', only confirmed reservations can be modified"

        user = users.get(res["user_id"], {})
        user_payments = {
            p["payment_id"]: p for p in user.get("payment_methods", [])
        }

        credit_cards = 0
        gift_cards = 0
        total_paid = 0
        for pm in new_payment_methods:
            pid = pm["payment_id"]
            amt = pm["amount"]
            if pid not in user_payments:
                return f"Error: payment method {pid} not found in user profile"
            ptype = user_payments[pid]["type"]
            if ptype == "credit_card":
                credit_cards += 1
            elif ptype == "gift_card":
                gift_cards += 1
                if user_payments[pid]["balance"] < amt:
                    return f"Error: gift card {pid} balance ({user_payments[pid]['balance']}) is not enough"
            if credit_cards > 1:
                return "Error: at most one credit card per reservation"
            if gift_cards > 2:
                return "Error: at most two gift cards per reservation"
            total_paid += amt

        if total_paid != res["total_price"]:
            return f"Error: payment amount {total_paid} does not match reservation total {res['total_price']}"

        res["payment_methods"] = new_payment_methods

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "new_payment_methods": new_payment_methods,
                "total": res["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_reservation_payment",
                "description": "Change the payment method(s) for a reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id.",
                        },
                        "new_payment_methods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "payment_id": {"type": "string"},
                                    "amount": {"type": "number"},
                                },
                                "required": ["payment_id", "amount"],
                            },
                            "description": "New list of payment methods and amounts.",
                        },
                    },
                    "required": ["reservation_id", "new_payment_methods"],
                },
            },
        }
