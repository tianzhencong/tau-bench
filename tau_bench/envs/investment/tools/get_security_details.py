# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetSecurityDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], security_id: str) -> str:
        securities = data["securities"]
        if security_id in securities:
            return json.dumps(securities[security_id])
        return "Error: security not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_security_details",
                "description": "Get the details of a security, including its name, type, sector, current price, and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "security_id": {
                            "type": "string",
                            "description": "The security id, such as 'SEC1001'.",
                        },
                    },
                    "required": ["security_id"],
                },
            },
        }
