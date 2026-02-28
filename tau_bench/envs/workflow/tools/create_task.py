# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateTask(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        project_id: str,
        title: str,
        assignee: str,
        priority: str,
        due_date: str,
        description: str,
    ) -> str:
        projects = data["projects"]
        if project_id not in projects:
            return "Error: project not found"

        task_id = project_id + "_T" + hashlib.md5(
            f"{project_id}_{title}_{assignee}".encode()
        ).hexdigest()[:6]

        task = {
            "task_id": task_id,
            "title": title,
            "assignee": assignee,
            "status": "open",
            "priority": priority,
            "due_date": due_date,
            "description": description,
            "hours_logged": 0,
        }
        projects[project_id]["tasks"].append(task)
        data["created_tasks"].append(task)
        return json.dumps(task)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a new task in a project. The task is added to the project's task list and tracked in created_tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "The project ID to add the task to, e.g. 'PRJ001'.",
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task.",
                        },
                        "assignee": {
                            "type": "string",
                            "description": "The employee ID of the person assigned to the task.",
                        },
                        "priority": {
                            "type": "string",
                            "description": "Task priority: 'low', 'medium', 'high', or 'critical'.",
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Due date in YYYY-MM-DD format.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the task.",
                        },
                    },
                    "required": [
                        "project_id",
                        "title",
                        "assignee",
                        "priority",
                        "due_date",
                        "description",
                    ],
                },
            },
        }
