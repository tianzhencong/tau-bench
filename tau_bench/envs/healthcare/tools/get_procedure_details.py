# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetProcedureDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], procedure_id: str) -> str:
        procedures = data["procedures"]
        if procedure_id in procedures:
            return json.dumps(procedures[procedure_id])
        return "Error: procedure not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_procedure_details",
                "description": "Get the details of a procedure, including name, department, duration, base cost, and whether a referral is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "procedure_id": {
                            "type": "string",
                            "description": "The procedure id, such as 'PROC001'.",
                        },
                    },
                    "required": ["procedure_id"],
                },
            },
        }
