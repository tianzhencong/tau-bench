# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetHotelDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], hotel_id: str) -> str:
        hotels = data["hotels"]
        if hotel_id in hotels:
            return json.dumps(hotels[hotel_id])
        return "Error: hotel not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_hotel_details",
                "description": "Get the details of a hotel, including room types, prices, and amenities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {
                            "type": "string",
                            "description": "The hotel id.",
                        },
                    },
                    "required": ["hotel_id"],
                },
            },
        }
