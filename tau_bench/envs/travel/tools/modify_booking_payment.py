# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyBookingPayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        booking_id: str,
        new_payment_methods: List[Dict[str, Any]],
        use_points: int = 0,
    ) -> str:
        bookings = data["bookings"]

        if booking_id not in bookings:
            return "Error: booking not found"

        booking = bookings[booking_id]
        if booking["status"] != "confirmed":
            return f"Error: booking status is '{booking['status']}', only confirmed bookings can be modified"

        booking["payment_methods"] = new_payment_methods

        return json.dumps(
            {
                "booking_id": booking_id,
                "new_payment_methods": new_payment_methods,
                "use_points": use_points,
                "total_price": booking["total_price"],
                "status": "confirmed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_booking_payment",
                "description": "Change the payment method(s) for a confirmed booking. Note: the API does not verify that payment amounts add up correctly. The agent must verify this before calling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "The booking id.",
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
                        "use_points": {
                            "type": "integer",
                            "description": "Number of loyalty points to apply to this booking.",
                        },
                    },
                    "required": ["booking_id", "new_payment_methods", "use_points"],
                },
            },
        }
