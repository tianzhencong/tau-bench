# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FormatTable(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], data_ref: str, columns: List[str]) -> str:
        intermediate = data.get("_intermediate_results", {})
        if data_ref == "latest_query":
            source = data.get("_latest_query_result")
        else:
            source = intermediate.get(data_ref)
        if source is None:
            return f"Error: data reference '{data_ref}' not found"
        if not isinstance(source, list):
            return "Error: data reference does not point to a list of records"
        if not columns:
            return "Error: columns list cannot be empty"

        header = "| " + " | ".join(columns) + " |"
        separator = "| " + " | ".join(["---"] * len(columns)) + " |"
        rows = []
        for record in source:
            row_vals = [str(record.get(col, "")) for col in columns]
            rows.append("| " + " | ".join(row_vals) + " |")
        table = "\n".join([header, separator] + rows)
        return table

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "format_table",
                "description": "Format data from a previous processing step as a markdown table with specified columns.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_ref": {
                            "type": "string",
                            "description": "Reference key to the data to format. Use 'latest_query' for the most recent QuerySalesData result, or a data_ref from a previous processing step.",
                        },
                        "columns": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of column names to include in the table.",
                        },
                    },
                    "required": ["data_ref", "columns"],
                },
            },
        }
