# Copyright Sierra

import hashlib
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class BookPackage(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        client_id: str,
        package_id: str,
        selected_options: Dict[str, str],
        travelers: List[Dict[str, str]],
        payment_methods: List[Dict[str, Any]],
        use_points: int = 0,
        trip_protection: bool = False,
    ) -> str:
        clients = data["clients"]
        packages = data["packages"]
        bookings = data["bookings"]

        if client_id not in clients:
            return "Error: client not found"
        if package_id not in packages:
            return "Error: package not found"

        package = packages[package_id]
        if not package.get("available", False):
            return "Error: package is not available"

        if len(travelers) == 0:
            return "Error: at least one traveler is required"
        if len(travelers) > 6:
            return "Error: maximum 6 travelers per booking"

        total = package["base_price"]

        component_map = {c["component_id"]: c for c in package.get("components", [])}
        for component_id, option_name in selected_options.items():
            if component_id not in component_map:
                return f"Error: component {component_id} not found in package"
            component = component_map[component_id]
            if option_name not in component.get("options", {}):
                return f"Error: option '{option_name}' not found for component {component_id}"
            total += component["options"][option_name].get("price_modifier", 0)

        if trip_protection:
            total += 50 * len(travelers)

        client = clients[client_id]
        if use_points > 0:
            if use_points > client.get("loyalty_points", 0):
                return f"Error: insufficient loyalty points, available: {client.get('loyalty_points', 0)}"
            client["loyalty_points"] -= use_points

        booking_id = "BK" + hashlib.md5(
            f"{client_id}_{package_id}_{len(travelers)}".encode()
        ).hexdigest()[:8].upper()

        bookings[booking_id] = {
            "booking_id": booking_id,
            "client_id": client_id,
            "package_id": package_id,
            "destination": package["destination"],
            "duration_nights": package["duration_nights"],
            "selected_options": selected_options,
            "travelers": travelers,
            "total_price": total,
            "payment_methods": payment_methods,
            "status": "confirmed",
            "trip_protection": trip_protection,
            "trip_start_date": "",
            "created_at": "2024-05-15T15:00:00",
        }

        package["available"] = False
        client.setdefault("bookings", []).append(booking_id)

        return json.dumps(
            {
                "booking_id": booking_id,
                "total_price": total,
                "status": "confirmed",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "book_package",
                "description": "Book a travel package for a client. The total price is calculated as base_price + sum of selected option price modifiers + trip protection (50 per traveler if enabled). Payment math is NOT validated by this tool; the agent must verify payment amounts before calling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {
                            "type": "string",
                            "description": "The client id, such as 'C1001'.",
                        },
                        "package_id": {
                            "type": "string",
                            "description": "The package id, such as 'PKG001'.",
                        },
                        "selected_options": {
                            "type": "object",
                            "description": "A mapping of component_id to the selected option name for each component.",
                            "additionalProperties": {"type": "string"},
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
                            "description": "List of travelers (maximum 6).",
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
                        "use_points": {
                            "type": "integer",
                            "description": "Number of loyalty points to use for this booking. Points are deducted from the client's balance.",
                        },
                        "trip_protection": {
                            "type": "boolean",
                            "description": "Whether to add trip protection ($50 per traveler).",
                        },
                    },
                    "required": [
                        "client_id",
                        "package_id",
                        "selected_options",
                        "travelers",
                        "payment_methods",
                        "use_points",
                        "trip_protection",
                    ],
                },
            },
        }
