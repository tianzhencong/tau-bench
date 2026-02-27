# Copyright Sierra

import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class SearchAvailableRooms(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        city: str,
        check_in_date: str,
        check_out_date: str,
        room_type: str = "any",
    ) -> str:
        hotels = data["hotels"]
        try:
            ci = datetime.strptime(check_in_date, "%Y-%m-%d")
            co = datetime.strptime(check_out_date, "%Y-%m-%d")
        except ValueError:
            return "Error: invalid date format, use YYYY-MM-DD"
        if co <= ci:
            return "Error: check-out date must be after check-in date"

        nights = (co - ci).days
        results = []
        for hotel_id, hotel in hotels.items():
            if hotel["city"].lower() != city.lower():
                continue
            for rt, info in hotel["rooms"].items():
                if room_type != "any" and rt != room_type:
                    continue
                avail = info.get("available", 0)
                if avail > 0:
                    results.append(
                        {
                            "hotel_id": hotel_id,
                            "hotel_name": hotel["name"],
                            "city": hotel["city"],
                            "star_rating": hotel["star_rating"],
                            "room_type": rt,
                            "nightly_rate": info["nightly_rate"],
                            "total_price": info["nightly_rate"] * nights,
                            "max_occupancy": info["max_occupancy"],
                            "available_rooms": avail,
                            "amenities": info.get("amenities", []),
                        }
                    )
        if not results:
            return "No available rooms found matching the criteria."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_available_rooms",
                "description": "Search for available hotel rooms in a city for given dates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city to search in, such as 'New York'.",
                        },
                        "check_in_date": {
                            "type": "string",
                            "description": "Check-in date in YYYY-MM-DD format.",
                        },
                        "check_out_date": {
                            "type": "string",
                            "description": "Check-out date in YYYY-MM-DD format.",
                        },
                        "room_type": {
                            "type": "string",
                            "enum": [
                                "any",
                                "standard",
                                "deluxe",
                                "suite",
                                "presidential_suite",
                            ],
                            "description": "The desired room type. Use 'any' to search all types.",
                        },
                    },
                    "required": ["city", "check_in_date", "check_out_date"],
                },
            },
        }
