# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyReservationGuests(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        guests: List[Dict[str, str]],
    ) -> str:
        reservations = data["reservations"]
        hotels = data["hotels"]

        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', only confirmed reservations can be modified"

        if len(guests) == 0:
            return "Error: at least one guest is required"

        hotel = hotels[res["hotel_id"]]
        room_info = hotel["rooms"][res["room_type"]]
        if len(guests) > room_info["max_occupancy"]:
            return f"Error: {res['room_type']} room max occupancy is {room_info['max_occupancy']}, but {len(guests)} guests provided"

        old_num = len(res["guests"])
        new_num = len(guests)
        from datetime import datetime

        ci = datetime.strptime(res["check_in_date"], "%Y-%m-%d")
        co = datetime.strptime(res["check_out_date"], "%Y-%m-%d")
        nights = (co - ci).days

        service_cost_diff = 0
        for svc in res["services"]:
            if svc == "breakfast":
                service_cost_diff += 25 * nights * (new_num - old_num)
            elif svc == "spa":
                service_cost_diff += 50 * (new_num - old_num)

        res["guests"] = guests
        res["service_cost"] += service_cost_diff
        res["total_price"] += service_cost_diff

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "num_guests": new_num,
                "service_cost_change": service_cost_diff,
                "new_total": res["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_reservation_guests",
                "description": "Modify the guest list of a reservation. The primary guest (first in list) cannot be changed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id.",
                        },
                        "guests": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "dob": {"type": "string"},
                                },
                                "required": ["first_name", "last_name", "dob"],
                            },
                            "description": "Updated list of guests.",
                        },
                    },
                    "required": ["reservation_id", "guests"],
                },
            },
        }
