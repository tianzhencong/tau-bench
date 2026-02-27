# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetPortfolioSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str) -> str:
        accounts = data["accounts"]
        securities = data["securities"]

        if account_id not in accounts:
            return "Error: account not found"

        account = accounts[account_id]
        holdings_summary = []
        total_holdings_value = 0.0

        for holding in account["holdings"]:
            security_id = holding["security_id"]
            current_price = securities[security_id]["current_price"]
            quantity = holding["quantity"]
            market_value = quantity * current_price
            unrealized_gain = (current_price - holding["average_cost_basis"]) * quantity
            total_holdings_value += market_value
            holdings_summary.append(
                {
                    "holding_id": holding["holding_id"],
                    "security_id": security_id,
                    "security_name": holding["security_name"],
                    "quantity": quantity,
                    "average_cost_basis": holding["average_cost_basis"],
                    "current_price": current_price,
                    "market_value": round(market_value, 2),
                    "unrealized_gain": round(unrealized_gain, 2),
                }
            )

        total_holdings_value = round(total_holdings_value, 2)
        cash_balance = account["cash_balance"]
        total_portfolio_value = round(total_holdings_value + cash_balance, 2)

        return json.dumps(
            {
                "account_id": account_id,
                "holdings": holdings_summary,
                "total_holdings_value": total_holdings_value,
                "cash_balance": cash_balance,
                "total_portfolio_value": total_portfolio_value,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_summary",
                "description": (
                    "Get a portfolio summary for an account, including total holdings value, "
                    "cash balance, total portfolio value, and unrealized gain/loss per holding."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id, such as 'A5001'.",
                        },
                    },
                    "required": ["account_id"],
                },
            },
        }
