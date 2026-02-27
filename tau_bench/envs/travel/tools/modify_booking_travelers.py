# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyBookingTravelers(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        booking_id: str,
        travelers: List[Dict[str, str]],
    ) -> str:
        bookings = data["bookings"]

        if booking_id not in bookings:
            return "Error: booking not found"

        booking = bookings[booking_id]
        if booking["status"] != "confirmed":
            return f"Error: booking status is '{booking['status']}', only confirmed bookings can be modified"

        if len(travelers) != len(booking["travelers"]):
            return f"Error: number of travelers must remain the same (original: {len(booking['travelers'])}, provided: {len(travelers)})"

        booking["travelers"] = travelers

        return json.dumps(
            {
                "booking_id": booking_id,
                "num_travelers": len(travelers),
                "travelers": travelers,
                "status": "confirmed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_booking_travelers",
                "description": "Modify the traveler list of a confirmed booking. The number of travelers must remain the same as the original booking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "The booking id.",
                        },
                        "travelers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "dob": {
                                        "type": "string",
                                        "description": "Date of birth in YYYY-MM-DD format.",
                                    },
                                },
                                "required": ["first_name", "last_name", "dob"],
                            },
                            "description": "Updated list of travelers. Must have the same number as the original booking.",
                        },
                    },
                    "required": ["booking_id", "travelers"],
                },
            },
        }
