# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetSpecialistDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], specialist_id: str) -> str:
        specialists = data["specialists"]
        if specialist_id in specialists:
            return json.dumps(specialists[specialist_id])
        return "Error: specialist not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_specialist_details",
                "description": "Get the details of a specialist, including name, department, procedures they perform, and their available time slots.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "specialist_id": {
                            "type": "string",
                            "description": "The specialist id, such as 'DR001'.",
                        },
                    },
                    "required": ["specialist_id"],
                },
            },
        }
