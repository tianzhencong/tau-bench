# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class TransferToHumanAgents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], summary: str) -> str:
        return "Transfer successful"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_to_human_agents",
                "description": "Transfer the user to a human agent. Use this only when the request cannot be handled by the automated system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A summary of the user's request and the reason for transfer.",
                        },
                    },
                    "required": ["summary"],
                },
            },
        }
