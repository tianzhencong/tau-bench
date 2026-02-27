# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListAccountTypes(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        return json.dumps(
            {
                "brokerage": "A standard taxable brokerage account for buying and selling securities.",
                "ira": "An Individual Retirement Account with tax advantages for retirement savings. Subject to annual contribution limits.",
                "savings": "A cash savings account that earns interest. Cannot be used for trading securities.",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_account_types",
                "description": "List all available account types with their descriptions.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
