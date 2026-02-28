# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetProjectDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], project_id: str) -> str:
        projects = data["projects"]
        if project_id in projects:
            return json.dumps(projects[project_id])
        return "Error: project not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_project_details",
                "description": "Get detailed information about a project including all its tasks, members, budget, and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "The project ID, e.g. 'PRJ001'.",
                        },
                    },
                    "required": ["project_id"],
                },
            },
        }
