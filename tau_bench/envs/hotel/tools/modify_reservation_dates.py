# Copyright Sierra

import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ModifyReservationDates(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        new_check_in_date: str,
        new_check_out_date: str,
        payment_id: str,
    ) -> str:
        reservations = data["reservations"]
        hotels = data["hotels"]

        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', only confirmed reservations can be modified"

        try:
            new_ci = datetime.strptime(new_check_in_date, "%Y-%m-%d")
            new_co = datetime.strptime(new_check_out_date, "%Y-%m-%d")
        except ValueError:
            return "Error: invalid date format, use YYYY-MM-DD"
        if new_co <= new_ci:
            return "Error: check-out date must be after check-in date"

        hotel = hotels[res["hotel_id"]]
        room_info = hotel["rooms"][res["room_type"]]
        new_nights = (new_co - new_ci).days
        new_room_cost = room_info["nightly_rate"] * new_nights

        num_guests = len(res["guests"])
        new_service_cost = 0
        for svc in res["services"]:
            if svc == "breakfast":
                new_service_cost += 25 * new_nights * num_guests
            elif svc == "parking":
                new_service_cost += 20 * new_nights
            elif svc == "spa":
                new_service_cost += 50 * num_guests
            elif svc in ("late_checkout", "early_checkin"):
                new_service_cost += 30

        new_total = new_room_cost + new_service_cost + res["insurance_cost"]
        price_diff = new_total - res["total_price"]

        res["check_in_date"] = new_check_in_date
        res["check_out_date"] = new_check_out_date
        res["room_cost"] = new_room_cost
        res["service_cost"] = new_service_cost
        res["total_price"] = new_total

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "new_check_in": new_check_in_date,
                "new_check_out": new_check_out_date,
                "new_total": new_total,
                "price_difference": price_diff,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_reservation_dates",
                "description": "Modify the check-in and check-out dates of a reservation. Note: the API does not verify rate type restrictions (non-refundable rates cannot be modified). The agent must check before calling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id.",
                        },
                        "new_check_in_date": {
                            "type": "string",
                            "description": "New check-in date in YYYY-MM-DD format.",
                        },
                        "new_check_out_date": {
                            "type": "string",
                            "description": "New check-out date in YYYY-MM-DD format.",
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment method id for additional charges or refund.",
                        },
                    },
                    "required": [
                        "reservation_id",
                        "new_check_in_date",
                        "new_check_out_date",
                        "payment_id",
                    ],
                },
            },
        }
