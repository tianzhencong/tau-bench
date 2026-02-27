# Copyright Sierra

import json
import random
import string
from datetime import datetime
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class BookReservation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        hotel_id: str,
        room_type: str,
        check_in_date: str,
        check_out_date: str,
        guests: List[Dict[str, str]],
        payment_methods: List[Dict[str, Any]],
        services: List[str],
        cancellation_insurance: bool = False,
    ) -> str:
        users = data["users"]
        hotels = data["hotels"]
        reservations = data["reservations"]

        if user_id not in users:
            return "Error: user not found"
        if hotel_id not in hotels:
            return "Error: hotel not found"

        hotel = hotels[hotel_id]
        if room_type not in hotel["rooms"]:
            return f"Error: room type '{room_type}' not available at this hotel"

        room_info = hotel["rooms"][room_type]
        if room_info["available"] <= 0:
            return f"Error: no available {room_type} rooms"

        max_occ = room_info["max_occupancy"]
        if len(guests) > max_occ:
            return f"Error: {room_type} room allows maximum {max_occ} guests, but {len(guests)} provided"
        if len(guests) == 0:
            return "Error: at least one guest is required"
        if len(guests) > 4:
            return "Error: maximum 4 guests per reservation"

        try:
            ci = datetime.strptime(check_in_date, "%Y-%m-%d")
            co = datetime.strptime(check_out_date, "%Y-%m-%d")
        except ValueError:
            return "Error: invalid date format, use YYYY-MM-DD"
        if co <= ci:
            return "Error: check-out date must be after check-in date"

        nights = (co - ci).days
        room_cost = room_info["nightly_rate"] * nights

        service_cost = 0
        num_guests = len(guests)
        valid_services = [
            "breakfast",
            "parking",
            "spa",
            "late_checkout",
            "early_checkin",
        ]
        for svc in services:
            if svc not in valid_services:
                return f"Error: unknown service '{svc}'"
            if svc == "breakfast":
                service_cost += 25 * nights * num_guests
            elif svc == "parking":
                service_cost += 20 * nights
            elif svc == "spa":
                service_cost += 50 * num_guests
            elif svc == "late_checkout":
                service_cost += 30
            elif svc == "early_checkin":
                user_membership = users[user_id].get("membership", "regular")
                if user_membership not in ["silver", "gold", "platinum"]:
                    return "Error: early check-in is only available for silver members and above"
                service_cost += 30

        insurance_cost = 40 if cancellation_insurance else 0
        total = room_cost + service_cost + insurance_cost

        credit_cards = 0
        gift_cards = 0
        total_paid = 0
        user_payments = {
            p["payment_id"]: p for p in users[user_id].get("payment_methods", [])
        }
        for pm in payment_methods:
            pid = pm["payment_id"]
            amt = pm["amount"]
            if pid not in user_payments:
                return f"Error: payment method {pid} not found in user profile"
            ptype = user_payments[pid]["type"]
            if ptype == "credit_card":
                credit_cards += 1
            elif ptype == "gift_card":
                gift_cards += 1
                if user_payments[pid]["balance"] < amt:
                    return f"Error: gift card {pid} balance ({user_payments[pid]['balance']}) is not enough for amount {amt}"
            if credit_cards > 1:
                return "Error: at most one credit card per reservation"
            if gift_cards > 2:
                return "Error: at most two gift cards per reservation"
            total_paid += amt

        if total_paid != total:
            return f"Error: payment amount does not add up, total price is {total}, but paid {total_paid}"

        res_id = "RES" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while res_id in reservations:
            res_id = "RES" + "".join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )

        for pm in payment_methods:
            pid = pm["payment_id"]
            if user_payments[pid]["type"] == "gift_card":
                user_payments[pid]["balance"] -= pm["amount"]
                for p in users[user_id]["payment_methods"]:
                    if p["payment_id"] == pid:
                        p["balance"] = user_payments[pid]["balance"]

        reservations[res_id] = {
            "reservation_id": res_id,
            "user_id": user_id,
            "hotel_id": hotel_id,
            "room_type": room_type,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests,
            "payment_methods": payment_methods,
            "services": services,
            "cancellation_insurance": cancellation_insurance,
            "status": "confirmed",
            "created_at": "2024-05-15T15:00:00",
            "rate_type": "refundable",
            "room_cost": room_cost,
            "service_cost": service_cost,
            "insurance_cost": insurance_cost,
            "total_price": total,
        }

        users[user_id]["reservations"].append(res_id)
        hotel["rooms"][room_type]["available"] -= 1

        return json.dumps(
            {
                "reservation_id": res_id,
                "total_price": total,
                "status": "confirmed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "book_reservation",
                "description": "Book a hotel room reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id.",
                        },
                        "hotel_id": {
                            "type": "string",
                            "description": "The hotel id.",
                        },
                        "room_type": {
                            "type": "string",
                            "enum": [
                                "standard",
                                "deluxe",
                                "suite",
                                "presidential_suite",
                            ],
                            "description": "The room type to book.",
                        },
                        "check_in_date": {
                            "type": "string",
                            "description": "Check-in date in YYYY-MM-DD format.",
                        },
                        "check_out_date": {
                            "type": "string",
                            "description": "Check-out date in YYYY-MM-DD format.",
                        },
                        "guests": {
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
                            "description": "List of guests.",
                        },
                        "payment_methods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "payment_id": {"type": "string"},
                                    "amount": {"type": "number"},
                                },
                                "required": ["payment_id", "amount"],
                            },
                            "description": "List of payment methods and amounts.",
                        },
                        "services": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "breakfast",
                                    "parking",
                                    "spa",
                                    "late_checkout",
                                    "early_checkin",
                                ],
                            },
                            "description": "List of additional services to add.",
                        },
                        "cancellation_insurance": {
                            "type": "boolean",
                            "description": "Whether to add cancellation insurance ($40).",
                        },
                    },
                    "required": [
                        "user_id",
                        "hotel_id",
                        "room_type",
                        "check_in_date",
                        "check_out_date",
                        "guests",
                        "payment_methods",
                        "services",
                        "cancellation_insurance",
                    ],
                },
            },
        }
