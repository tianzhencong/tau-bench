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
                    "Transfer the patient to a human agent, with a summary of the patient's issue. "
                    "Only transfer if the patient explicitly asks for a human agent, or if the patient's issue "
                    "cannot be resolved by the agent with the available tools."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A summary of the patient's issue.",
                        },
                    },
                    "required": ["summary"],
                },
            },
        }
