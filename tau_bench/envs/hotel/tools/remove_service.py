# Copyright Sierra

import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool

CURRENT_TIME = datetime(2024, 5, 15, 15, 0, 0)


class RemoveService(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        service: str,
        payment_id: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', can only remove services from confirmed reservations"

        if service not in res["services"]:
            return f"Error: service '{service}' is not on this reservation"

        if service in ("late_checkout", "early_checkin"):
            return f"Error: {service} cannot be removed once added"

        ci = datetime.strptime(res["check_in_date"], "%Y-%m-%d")
        hours_until = (ci - CURRENT_TIME).total_seconds() / 3600
        if hours_until < 24:
            return "Error: services can only be removed if check-in is more than 24 hours away"

        co = datetime.strptime(res["check_out_date"], "%Y-%m-%d")
        nights = (co - ci).days
        num_guests = len(res["guests"])

        refund = 0
        if service == "breakfast":
            refund = 25 * nights * num_guests
        elif service == "parking":
            refund = 20 * nights
        elif service == "spa":
            refund = 50 * num_guests

        res["services"].remove(service)
        res["service_cost"] -= refund
        res["total_price"] -= refund

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "service_removed": service,
                "refund_amount": refund,
                "new_total": res["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_service",
                "description": "Remove a service from a confirmed reservation. Note: early_checkin and late_checkout cannot be removed. Services can only be removed if check-in is more than 24 hours away.",
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
                            "description": "The service to remove.",
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment method id for the refund.",
                        },
                    },
                    "required": ["reservation_id", "service", "payment_id"],
                },
            },
        }
