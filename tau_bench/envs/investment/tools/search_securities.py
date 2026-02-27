# Copyright Sierra

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SearchSecurities(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        type: Optional[str] = None,
        sector: Optional[str] = None,
    ) -> str:
        securities = data["securities"]
        results = []
        for security_id, security in securities.items():
            if security["status"] != "active":
                continue
            if type is not None and security["type"].lower() != type.lower():
                continue
            if sector is not None and security["sector"].lower() != sector.lower():
                continue
            results.append(
                {
                    "security_id": security_id,
                    "name": security["name"],
                    "type": security["type"],
                    "sector": security["sector"],
                    "current_price": security["current_price"],
                }
            )
        if not results:
            return "No securities found matching the criteria."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_securities",
                "description": "Search for active securities, optionally filtered by type and/or sector. Returns a list of matching securities with their current prices.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["stock", "etf", "bond", "mutual_fund"],
                            "description": "The type of security to filter by, such as 'stock' or 'etf'. If not provided, all types are included.",
                        },
                        "sector": {
                            "type": "string",
                            "description": "The sector to filter by, such as 'Technology' or 'Healthcare'. If not provided, all sectors are included.",
                        },
                    },
                    "required": [],
                },
            },
        }
