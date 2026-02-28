# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateTaskStatus(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], project_id: str, task_id: str, new_status: str
    ) -> str:
        projects = data["projects"]
        if project_id not in projects:
            return "Error: project not found"
        tasks = projects[project_id]["tasks"]
        for task in tasks:
            if task["task_id"] == task_id:
                old_status = task["status"]
                task["status"] = new_status
                return json.dumps(
                    {
                        "task_id": task_id,
                        "old_status": old_status,
                        "new_status": new_status,
                        "status": "updated",
                    }
                )
        return f"Error: task '{task_id}' not found in project '{project_id}'"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_task_status",
                "description": "Update the status of a task in a project.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "The project ID containing the task, e.g. 'PRJ001'.",
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The task ID to update, e.g. 'PRJ001_T01'.",
                        },
                        "new_status": {
                            "type": "string",
                            "description": "The new status for the task, e.g. 'in_progress', 'done', 'blocked'.",
                        },
                    },
                    "required": ["project_id", "task_id", "new_status"],
                },
            },
        }
