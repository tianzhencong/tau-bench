# Copyright Sierra

import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ModifyReservationRoom(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        new_room_type: str,
        payment_id: str,
    ) -> str:
        reservations = data["reservations"]
        hotels = data["hotels"]

        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', only confirmed reservations can be modified"

        hotel = hotels[res["hotel_id"]]
        if new_room_type not in hotel["rooms"]:
            return f"Error: room type '{new_room_type}' not available at this hotel"

        new_room_info = hotel["rooms"][new_room_type]
        if new_room_info["available"] <= 0:
            return f"Error: no available {new_room_type} rooms"

        num_guests = len(res["guests"])
        if num_guests > new_room_info["max_occupancy"]:
            return f"Error: {new_room_type} room max occupancy is {new_room_info['max_occupancy']}, but reservation has {num_guests} guests"

        ci = datetime.strptime(res["check_in_date"], "%Y-%m-%d")
        co = datetime.strptime(res["check_out_date"], "%Y-%m-%d")
        nights = (co - ci).days
        new_room_cost = new_room_info["nightly_rate"] * nights
        price_diff = new_room_cost - res["room_cost"]

        old_room_type = res["room_type"]
        hotel["rooms"][old_room_type]["available"] += 1
        hotel["rooms"][new_room_type]["available"] -= 1

        res["room_type"] = new_room_type
        res["room_cost"] = new_room_cost
        res["total_price"] = new_room_cost + res["service_cost"] + res["insurance_cost"]

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "old_room_type": old_room_type,
                "new_room_type": new_room_type,
                "price_difference": price_diff,
                "new_total": res["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_reservation_room",
                "description": "Change the room type of a reservation (upgrade or downgrade).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id.",
                        },
                        "new_room_type": {
                            "type": "string",
                            "enum": [
                                "standard",
                                "deluxe",
                                "suite",
                                "presidential_suite",
                            ],
                            "description": "The new room type.",
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment method id for price difference.",
                        },
                    },
                    "required": ["reservation_id", "new_room_type", "payment_id"],
                },
            },
        }
