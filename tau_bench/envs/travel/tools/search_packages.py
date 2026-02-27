# Copyright Sierra

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SearchPackages(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        destination: Optional[str] = None,
        min_duration: Optional[int] = None,
        max_price: Optional[float] = None,
    ) -> str:
        packages = data["packages"]
        results = []
        for package_id, package in packages.items():
            if not package.get("available", False):
                continue
            if destination is not None and package["destination"].lower() != destination.lower():
                continue
            if min_duration is not None and package["duration_nights"] < min_duration:
                continue
            if max_price is not None and package["base_price"] > max_price:
                continue
            results.append(
                {
                    "package_id": package_id,
                    "destination": package["destination"],
                    "duration_nights": package["duration_nights"],
                    "base_price": package["base_price"],
                    "num_components": len(package.get("components", [])),
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
                "name": "search_packages",
                "description": "Search for available travel packages, optionally filtered by destination, minimum duration, and maximum price. Returns a list of matching packages with basic information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": "The destination to filter by, such as 'Paris' or 'Tokyo'. If not provided, all destinations are included.",
                        },
                        "min_duration": {
                            "type": "integer",
                            "description": "The minimum number of nights for the package. If not provided, no minimum is applied.",
                        },
                        "max_price": {
                            "type": "number",
                            "description": "The maximum base price for the package. If not provided, no maximum is applied.",
                        },
                    },
                    "required": [],
                },
            },
        }
