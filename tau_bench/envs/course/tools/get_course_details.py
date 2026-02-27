# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetCourseDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], course_id: str) -> str:
        courses = data["courses"]
        if course_id in courses:
            return json.dumps(courses[course_id])
        return "Error: course not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_course_details",
                "description": "Get the catalog details of a course, including all available sections, prerequisites, and credit information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_id": {
                            "type": "string",
                            "description": "The course id, such as 'CS120'.",
                        },
                    },
                    "required": ["course_id"],
                },
            },
        }
