# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetPackageDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], package_id: str) -> str:
        packages = data["packages"]
        if package_id in packages:
            return json.dumps(packages[package_id])
        return "Error: package not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_package_details",
                "description": "Get the full details of a travel package, including destination, duration, all components with their options, base price, and availability.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "package_id": {
                            "type": "string",
                            "description": "The package id, such as 'PKG001'.",
                        },
                    },
                    "required": ["package_id"],
                },
            },
        }
