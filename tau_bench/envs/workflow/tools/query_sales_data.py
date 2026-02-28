# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class QuerySalesData(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        region: str = "",
        product: str = "",
        date_from: str = "",
        date_to: str = "",
    ) -> str:
        sales = data["sales_database"]
        results = []
        for record in sales:
            if region and record["region"].lower() != region.lower():
                continue
            if product and record["product"].lower() != product.lower():
                continue
            if date_from and record["date"] < date_from:
                continue
            if date_to and record["date"] > date_to:
                continue
            results.append(record)
        data["_latest_query_result"] = results
        if not results:
            return "No matching sales records found."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_sales_data",
                "description": "Query sales records with optional filters. Results are stored for use by downstream data processing tools (AggregateData, FilterData, etc.).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "region": {
                            "type": "string",
                            "description": "Filter by region, e.g. 'North', 'South', 'East', 'West'. Leave empty for all regions.",
                        },
                        "product": {
                            "type": "string",
                            "description": "Filter by product name, e.g. 'Basic Plan'. Leave empty for all products.",
                        },
                        "date_from": {
                            "type": "string",
                            "description": "Filter records on or after this date (YYYY-MM-DD). Leave empty for no lower bound.",
                        },
                        "date_to": {
                            "type": "string",
                            "description": "Filter records on or before this date (YYYY-MM-DD). Leave empty for no upper bound.",
                        },
                    },
                    "required": [],
                },
            },
        }
