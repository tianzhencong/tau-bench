# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AggregateData(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        data_ref: str,
        group_by: str,
        metric: str,
        operation: str,
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

        groups: Dict[str, list] = {}
        for record in source:
            key = str(record.get(group_by, "unknown"))
            groups.setdefault(key, []).append(record)

        result = {}
        for key, records in groups.items():
            values = []
            for r in records:
                val = r.get(metric)
                if val is not None:
                    try:
                        values.append(float(val))
                    except (ValueError, TypeError):
                        pass
            if not values:
                result[key] = None
                continue
            if operation == "sum":
                result[key] = round(sum(values), 2)
            elif operation == "avg":
                result[key] = round(sum(values) / len(values), 2)
            elif operation == "count":
                result[key] = len(values)
            elif operation == "max":
                result[key] = round(max(values), 2)
            elif operation == "min":
                result[key] = round(min(values), 2)
            else:
                return f"Error: unsupported operation '{operation}'. Use sum, avg, count, max, or min."

        ref_key = hashlib.md5(
            f"agg_{data_ref}_{group_by}_{metric}_{operation}".encode()
        ).hexdigest()[:12]
        if "_intermediate_results" not in data:
            data["_intermediate_results"] = {}
        aggregated_list = [
            {group_by: k, f"{operation}_{metric}": v} for k, v in result.items()
        ]
        data["_intermediate_results"][ref_key] = aggregated_list
        return json.dumps({"data_ref": ref_key, "result": aggregated_list})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "aggregate_data",
                "description": "Aggregate data from a previous query or processing step. Groups records by a field and applies an operation (sum, avg, count, max, min) on a metric. The result is stored and a new data_ref key is returned for downstream tools.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_ref": {
                            "type": "string",
                            "description": "Reference key to the data to aggregate. Use 'latest_query' for the most recent QuerySalesData result, or a data_ref key from a previous processing step.",
                        },
                        "group_by": {
                            "type": "string",
                            "description": "The field name to group records by, e.g. 'region', 'product'.",
                        },
                        "metric": {
                            "type": "string",
                            "description": "The numeric field to aggregate, e.g. 'amount', 'quantity'.",
                        },
                        "operation": {
                            "type": "string",
                            "description": "The aggregation operation: 'sum', 'avg', 'count', 'max', or 'min'.",
                        },
                    },
                    "required": ["data_ref", "group_by", "metric", "operation"],
                },
            },
        }
