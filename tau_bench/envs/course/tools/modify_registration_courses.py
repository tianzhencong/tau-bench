# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyRegistrationCourses(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        registration_id: str,
        new_courses: List[Dict[str, str]],
    ) -> str:
        registrations = data["registrations"]
        courses = data["courses"]

        if registration_id not in registrations:
            return "Error: registration not found"

        registration = registrations[registration_id]
        if registration["status"] != "pending":
            return f"Error: registration status is '{registration['status']}', only pending registrations can have courses replaced"

        built_courses = []
        for nc in new_courses:
            course_id = nc["course_id"]
            section_id = nc["section_id"]

            if course_id not in courses:
                return f"Error: course {course_id} not found in catalog"

            course_catalog = courses[course_id]
            if section_id not in course_catalog["sections"]:
                return f"Error: section {section_id} not found for course {course_id}"

            section = course_catalog["sections"][section_id]
            built_courses.append(
                {
                    "course_id": course_id,
                    "course_name": course_catalog["name"],
                    "section_id": section_id,
                    "credits": course_catalog["credits"],
                    "tuition": section["tuition_per_credit"] * course_catalog["credits"],
                    "instructor": section["instructor"],
                    "days": section["days"],
                    "start_time": section["start_time"],
                    "end_time": section["end_time"],
                    "room": section["room"],
                }
            )

        registration["courses"] = built_courses
        registration["total_credits"] = sum(c["credits"] for c in built_courses)
        registration["total_tuition"] = sum(c["tuition"] for c in built_courses)
        registration["status"] = "pending (modified)"

        return json.dumps(registration)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_registration_courses",
                "description": (
                    "Replace all courses in a pending registration with a new set of courses. "
                    "Note: the API does not check prerequisites, credit limits, or schedule conflicts. "
                    "The agent must verify these before calling. The agent needs to explain the modification "
                    "detail and ask for explicit user confirmation (yes/no) to proceed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "registration_id": {
                            "type": "string",
                            "description": "The registration id, such as 'REGGV6TOLA'.",
                        },
                        "new_courses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "course_id": {
                                        "type": "string",
                                        "description": "The course id, such as 'CS120'.",
                                    },
                                    "section_id": {
                                        "type": "string",
                                        "description": "The section id, such as 'CS120-001'.",
                                    },
                                },
                                "required": ["course_id", "section_id"],
                            },
                            "description": "The new list of courses and sections for the registration.",
                        },
                    },
                    "required": ["registration_id", "new_courses"],
                },
            },
        }
