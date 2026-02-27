# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListDestinations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        packages = data["packages"]
        destinations = sorted(
            set(package["destination"] for package in packages.values())
        )
        return json.dumps(destinations)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_destinations",
                "description": "List all unique travel destinations available across all packages.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
