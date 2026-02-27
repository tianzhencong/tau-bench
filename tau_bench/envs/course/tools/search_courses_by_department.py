# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class SearchCoursesByDepartment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department: str) -> str:
        courses = data["courses"]
        results = []
        for course_id, course in courses.items():
            if course["department"].lower() == department.lower():
                results.append(
                    {
                        "course_id": course_id,
                        "name": course["name"],
                        "department": course["department"],
                        "credits": course["credits"],
                    }
                )
        if not results:
            return "No courses found"
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_courses_by_department",
                "description": "Search for courses offered by a specific department. Returns a list of matching courses with their basic information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "description": "The department name to search for, such as 'Computer Science' or 'Engineering'.",
                        },
                    },
                    "required": ["department"],
                },
            },
        }
