# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FilterData(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        data_ref: str,
        field: str,
        operator: str,
        value: str,
    ) -> str:
        intermediate = data.get("_intermediate_results", {})
        if data_ref == "latest_query":
            source = data.get("_latest_query_result")
        else:
            source = intermediate.get(data_ref)
        if source is None:
            return f"Error: data reference '{data_ref}' not found"
        if not isinstance(source, list):
            return "Error: data reference does not point to a list of records"

        filtered = []
        for record in source:
            field_val = record.get(field)
            if field_val is None:
                continue
            if operator == "equals":
                if str(field_val).lower() == value.lower():
                    filtered.append(record)
            elif operator == "greater_than":
                try:
                    if float(field_val) > float(value):
                        filtered.append(record)
                except (ValueError, TypeError):
                    pass
            elif operator == "less_than":
                try:
                    if float(field_val) < float(value):
                        filtered.append(record)
                except (ValueError, TypeError):
                    pass
            elif operator == "contains":
                if value.lower() in str(field_val).lower():
                    filtered.append(record)
            else:
                return f"Error: unsupported operator '{operator}'. Use equals, greater_than, less_than, or contains."

        ref_key = hashlib.md5(
            f"filter_{data_ref}_{field}_{operator}_{value}".encode()
        ).hexdigest()[:12]
        if "_intermediate_results" not in data:
            data["_intermediate_results"] = {}
        data["_intermediate_results"][ref_key] = filtered
        return json.dumps({"data_ref": ref_key, "result": filtered})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "filter_data",
                "description": "Filter records from a previous query or processing step. Applies a condition on a field and returns matching records. The result is stored and a new data_ref key is returned for downstream tools.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_ref": {
                            "type": "string",
                            "description": "Reference key to the data to filter. Use 'latest_query' for the most recent QuerySalesData result, or a data_ref key from a previous processing step.",
                        },
                        "field": {
                            "type": "string",
                            "description": "The field name to filter on, e.g. 'region', 'amount'.",
                        },
                        "operator": {
                            "type": "string",
                            "description": "The filter operator: 'equals', 'greater_than', 'less_than', or 'contains'.",
                        },
                        "value": {
                            "type": "string",
                            "description": "The value to compare against.",
                        },
                    },
                    "required": ["data_ref", "field", "operator", "value"],
                },
            },
        }
