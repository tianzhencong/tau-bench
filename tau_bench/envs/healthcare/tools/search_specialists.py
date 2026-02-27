# Copyright Sierra

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class SearchSpecialists(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        department: Optional[str] = None,
        procedure_id: Optional[str] = None,
        date: Optional[str] = None,
    ) -> str:
        specialists = data["specialists"]
        results = []
        for specialist_id, specialist in specialists.items():
            if department is not None and specialist["department"].lower() != department.lower():
                continue
            if procedure_id is not None and procedure_id not in specialist["procedures"]:
                continue
            if date is not None:
                available_slots = [
                    slot
                    for slot in specialist["available_slots"]
                    if slot["date"] == date and slot["available"]
                ]
                if not available_slots:
                    continue
                results.append(
                    {
                        "specialist_id": specialist_id,
                        "name": specialist["name"],
                        "department": specialist["department"],
                        "procedures": specialist["procedures"],
                        "available_slots": available_slots,
                    }
                )
            else:
                results.append(
                    {
                        "specialist_id": specialist_id,
                        "name": specialist["name"],
                        "department": specialist["department"],
                        "procedures": specialist["procedures"],
                    }
                )
        if not results:
            return "No specialists found matching the criteria."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_specialists",
                "description": "Search for specialists, optionally filtered by department, procedure they perform, and/or date availability. When a date is provided, only specialists with available slots on that date are returned, along with their available slots.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "description": "The department to filter by, such as 'Cardiology'. If not provided, all departments are included.",
                        },
                        "procedure_id": {
                            "type": "string",
                            "description": "The procedure id to filter by, such as 'PROC003'. Only returns specialists who perform this procedure.",
                        },
                        "date": {
                            "type": "string",
                            "description": "The date to filter by in 'YYYY-MM-DD' format. Only returns specialists with available slots on this date.",
                        },
                    },
                    "required": [],
                },
            },
        }
