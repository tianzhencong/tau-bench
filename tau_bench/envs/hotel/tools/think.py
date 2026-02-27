# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class Think(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], thought: str) -> str:
        return "OK"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "think",
                "description": "Use this tool to think about something. It will not obtain new information or change the database, but just append the thought to the agent's message history. Use this when complex reasoning is needed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "thought": {
                            "type": "string",
                            "description": "The thought to think about.",
                        },
                    },
                    "required": ["thought"],
                },
            },
        }
