# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ModifyAccountSettings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str, settings: Dict[str, Any]) -> str:
        accounts = data["accounts"]
        if account_id not in accounts:
            return "Error: account not found"

        account = accounts[account_id]
        for key, value in settings.items():
            account["settings"][key] = value

        return json.dumps(
            {
                "account_id": account_id,
                "updated_settings": account["settings"],
                "status": "success",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_account_settings",
                "description": "Modify the settings of an account, such as dividend reinvestment or default order type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                        "settings": {
                            "type": "object",
                            "description": "A dictionary of settings to update, such as {'dividend_reinvestment': true, 'default_order_type': 'market'}.",
                        },
                    },
                    "required": ["account_id", "settings"],
                },
            },
        }
