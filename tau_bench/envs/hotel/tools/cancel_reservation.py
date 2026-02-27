# Copyright Sierra

import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool

CURRENT_TIME = datetime(2024, 5, 15, 15, 0, 0)


class CancelReservation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reservation_id: str, reason: str) -> str:
        reservations = data["reservations"]
        if reservation_id not in reservations:
            return "Error: reservation not found"

        res = reservations[reservation_id]
        if res["status"] != "confirmed":
            return f"Error: reservation status is '{res['status']}', only confirmed reservations can be cancelled"

        res["status"] = "cancelled"
        res["cancellation_reason"] = reason

        return json.dumps(
            {
                "reservation_id": reservation_id,
                "status": "cancelled",
                "total_price": res["total_price"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_reservation",
                "description": "Cancel a hotel reservation. Note: the API does not verify cancellation policy rules (refund eligibility, timing restrictions). The agent must verify these before calling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id to cancel.",
                        },
                        "reason": {
                            "type": "string",
                            "description": "The reason for cancellation.",
                        },
                    },
                    "required": ["reservation_id", "reason"],
                },
            },
        }
