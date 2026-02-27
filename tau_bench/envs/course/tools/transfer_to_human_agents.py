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
                "description": (
                    "Transfer the student to a human academic advisor, with a summary of the student's issue. "
                    "Only transfer if the student explicitly asks for a human advisor, or if the student's issue "
                    "cannot be resolved by the agent with the available tools."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A summary of the student's issue.",
                        },
                    },
                    "required": ["summary"],
                },
            },
        }
