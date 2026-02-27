# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CancelBooking(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], booking_id: str, reason: str) -> str:
        bookings = data["bookings"]
        if booking_id not in bookings:
            return "Error: booking not found"

        booking = bookings[booking_id]
        booking["status"] = "cancelled"
        booking["cancellation_reason"] = reason

        return json.dumps(
            {
                "booking_id": booking_id,
                "status": "cancelled",
                "total_price": booking["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_booking",
                "description": "Cancel a travel booking. Note: the API does not check refund rules or cancellation policies. The agent must verify these before calling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "The booking id to cancel.",
                        },
                        "reason": {
                            "type": "string",
                            "description": "The reason for cancellation.",
                        },
                    },
                    "required": ["booking_id", "reason"],
                },
            },
        }
