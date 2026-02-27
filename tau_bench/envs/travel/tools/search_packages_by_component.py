# Copyright Sierra

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SearchPackagesByComponent(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        component_type: str,
        destination: Optional[str] = None,
    ) -> str:
        packages = data["packages"]
        results = []
        for package_id, package in packages.items():
            if destination is not None and package["destination"].lower() != destination.lower():
                continue
            has_component = any(
                c.get("type", "").lower() == component_type.lower()
                for c in package.get("components", [])
            )
            if has_component:
                results.append(
                    {
                        "package_id": package_id,
                        "destination": package["destination"],
                        "duration_nights": package["duration_nights"],
                        "base_price": package["base_price"],
                        "available": package.get("available", False),
                    }
                )
        if not results:
            return "No packages found matching the criteria."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_packages_by_component",
                "description": "Search for travel packages that include a specific component type (e.g., flight, hotel, car, activity), optionally filtered by destination.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "component_type": {
                            "type": "string",
                            "enum": ["flight", "hotel", "car", "activity"],
                            "description": "The type of component to search for.",
                        },
                        "destination": {
                            "type": "string",
                            "description": "The destination to filter by. If not provided, all destinations are included.",
                        },
                    },
                    "required": ["component_type"],
                },
            },
        }
