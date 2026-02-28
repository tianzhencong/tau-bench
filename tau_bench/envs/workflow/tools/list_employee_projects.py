# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListEmployeeProjects(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str) -> str:
        projects = data["projects"]
        employee_projects = []
        for proj_id, proj in projects.items():
            if proj["owner"] == employee_id or employee_id in proj.get("members", []):
                employee_projects.append(
                    {
                        "project_id": proj["project_id"],
                        "name": proj["name"],
                        "status": proj["status"],
                        "role": "owner" if proj["owner"] == employee_id else "member",
                    }
                )
        if not employee_projects:
            return "No projects found for this employee."
        return json.dumps(employee_projects)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_employee_projects",
                "description": "List all projects where the employee is an owner or a member.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "string",
                            "description": "The employee ID, e.g. 'EMP001'.",
                        },
                    },
                    "required": ["employee_id"],
                },
            },
        }
