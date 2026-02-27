# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetBookingDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], booking_id: str) -> str:
        bookings = data["bookings"]
        if booking_id in bookings:
            return json.dumps(bookings[booking_id])
        return "Error: booking not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_booking_details",
                "description": "Get the full details of a booking, including destination, duration, selected options, travelers, total price, payment methods, status, and trip protection.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "The booking id, such as 'BK12345678'.",
                        },
                    },
                    "required": ["booking_id"],
                },
            },
        }
