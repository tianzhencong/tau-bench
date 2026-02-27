# Copyright Sierra

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SearchProcedures(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        department: Optional[str] = None,
        name_contains: Optional[str] = None,
    ) -> str:
        procedures = data["procedures"]
        results = []
        for procedure_id, procedure in procedures.items():
            if department is not None and procedure["department"].lower() != department.lower():
                continue
            if name_contains is not None and name_contains.lower() not in procedure["name"].lower():
                continue
            results.append(
                {
                    "procedure_id": procedure_id,
                    "name": procedure["name"],
                    "department": procedure["department"],
                    "base_cost": procedure["base_cost"],
                    "requires_referral": procedure["requires_referral"],
                }
            )
        if not results:
            return "No procedures found matching the criteria."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_procedures",
                "description": "Search for procedures in the catalog, optionally filtered by department and/or name. Returns a list of matching procedures with their details.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "description": "The department to filter by, such as 'Cardiology' or 'Orthopedics'. If not provided, all departments are included.",
                        },
                        "name_contains": {
                            "type": "string",
                            "description": "A substring to search for in the procedure name, such as 'MRI' or 'consultation'. Case-insensitive.",
                        },
                    },
                    "required": [],
                },
            },
        }
