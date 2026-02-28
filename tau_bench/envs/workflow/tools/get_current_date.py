# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetCurrentDate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        return "2024-11-15"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Get the current date.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
