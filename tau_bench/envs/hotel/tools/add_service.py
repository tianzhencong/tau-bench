# Copyright Sierra

import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddService(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        service: str,
        payment_id: str,
    ) -> str:
        reservations = data["reservations"]
        users = data["users"]

        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', can only add services to confirmed reservations"

        if service in res["services"]:
            return f"Error: service '{service}' is already added to this reservation"

        valid_services = ["breakfast", "parking", "spa", "late_checkout", "early_checkin"]
        if service not in valid_services:
            return f"Error: unknown service '{service}'"

        ci = datetime.strptime(res["check_in_date"], "%Y-%m-%d")
        co = datetime.strptime(res["check_out_date"], "%Y-%m-%d")
        nights = (co - ci).days
        num_guests = len(res["guests"])

        if service == "early_checkin":
            user = users.get(res["user_id"], {})
            membership = user.get("membership", "regular")
            if membership not in ["silver", "gold", "platinum"]:
                return "Error: early check-in is only available for silver members and above"

        cost = 0
        if service == "breakfast":
            cost = 25 * nights * num_guests
        elif service == "parking":
            cost = 20 * nights
        elif service == "spa":
            cost = 50 * num_guests
        elif service in ("late_checkout", "early_checkin"):
            cost = 30

        res["services"].append(service)
        res["service_cost"] += cost
        res["total_price"] += cost

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "service_added": service,
                "service_cost": cost,
                "new_total": res["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_service",
                "description": "Add a service to a confirmed reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id.",
                        },
                        "service": {
                            "type": "string",
                            "enum": [
                                "breakfast",
                                "parking",
                                "spa",
                                "late_checkout",
                                "early_checkin",
                            ],
                            "description": "The service to add.",
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment method id for the service charge.",
                        },
                    },
                    "required": ["reservation_id", "service", "payment_id"],
                },
            },
        }
