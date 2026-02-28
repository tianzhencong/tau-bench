# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GenerateReport(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        data_ref: str,
        format: str,
        author_id: str,
    ) -> str:
        intermediate = data.get("_intermediate_results", {})
        if data_ref == "latest_query":
            source = data.get("_latest_query_result")
        else:
            source = intermediate.get(data_ref)
        if source is None:
            return f"Error: data reference '{data_ref}' not found"

        report_id = "RPT_" + hashlib.md5(
            f"{title}_{data_ref}_{format}_{author_id}".encode()
        ).hexdigest()[:10]

        record_count = len(source) if isinstance(source, list) else 1
        report = {
            "report_id": report_id,
            "title": title,
            "format": format,
            "author_id": author_id,
            "data_ref": data_ref,
            "record_count": record_count,
            "data": source,
        }
        data["generated_reports"][report_id] = report
        return json.dumps(
            {
                "report_id": report_id,
                "title": title,
                "format": format,
                "record_count": record_count,
                "status": "generated",
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate a report from processed data. The report is stored and can be referenced by its report_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the report.",
                        },
                        "data_ref": {
                            "type": "string",
                            "description": "Reference key to the data to include in the report. Use 'latest_query' for the most recent QuerySalesData result, or a data_ref from a previous processing step.",
                        },
                        "format": {
                            "type": "string",
                            "description": "The format of the report, e.g. 'pdf', 'csv', 'summary'.",
                        },
                        "author_id": {
                            "type": "string",
                            "description": "The employee ID of the report author.",
                        },
                    },
                    "required": ["title", "data_ref", "format", "author_id"],
                },
            },
        }
