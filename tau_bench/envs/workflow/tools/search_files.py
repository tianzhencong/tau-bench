# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class SearchFiles(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        department: str = "",
        file_type: str = "",
        keyword: str = "",
    ) -> str:
        files = data["files"]
        results = []
        for file_id, f in files.items():
            if department and f["department"].lower() != department.lower():
                continue
            if file_type and f["type"].lower() != file_type.lower():
                continue
            if keyword:
                kw = keyword.lower()
                if (
                    kw not in f["name"].lower()
                    and kw not in f.get("content_preview", "").lower()
                ):
                    continue
            results.append(f)
        if not results:
            return "No matching files found."
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_files",
                "description": "Search for files by department, file type, and/or keyword in the file name or content preview.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "description": "Filter by department name. Leave empty for all departments.",
                        },
                        "file_type": {
                            "type": "string",
                            "description": "Filter by file type, e.g. 'pdf', 'xlsx', 'docx'. Leave empty for all types.",
                        },
                        "keyword": {
                            "type": "string",
                            "description": "Search keyword to match against file name or content preview. Leave empty for no keyword filter.",
                        },
                    },
                    "required": [],
                },
            },
        }
