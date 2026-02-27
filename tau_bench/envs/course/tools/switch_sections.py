# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class SwitchSections(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        registration_id: str,
        switches: List[Dict[str, str]],
    ) -> str:
        registrations = data["registrations"]
        courses = data["courses"]

        if registration_id not in registrations:
            return "Error: registration not found"

        registration = registrations[registration_id]
        if registration["status"] not in ("confirmed", "pending"):
            return f"Error: registration status is '{registration['status']}', only confirmed or pending registrations can have sections switched"

        registered_course_ids = {c["course_id"]: c for c in registration["courses"]}

        changes = []
        for switch in switches:
            course_id = switch["course_id"]
            new_section_id = switch["new_section_id"]

            if course_id not in registered_course_ids:
                return f"Error: course {course_id} not found in registration"

            if course_id not in courses:
                return f"Error: course {course_id} not found in catalog"

            course_catalog = courses[course_id]
            if new_section_id not in course_catalog["sections"]:
                return f"Error: section {new_section_id} not found for course {course_id}"

            new_section = course_catalog["sections"][new_section_id]
            if not new_section["available"]:
                return f"Error: section {new_section_id} has no available seats"

            reg_course = registered_course_ids[course_id]
            old_section_id = reg_course["section_id"]

            reg_course["section_id"] = new_section_id
            reg_course["instructor"] = new_section["instructor"]
            reg_course["days"] = new_section["days"]
            reg_course["start_time"] = new_section["start_time"]
            reg_course["end_time"] = new_section["end_time"]
            reg_course["room"] = new_section["room"]
            reg_course["tuition"] = new_section["tuition_per_credit"] * reg_course["credits"]

            changes.append(
                {
                    "course_id": course_id,
                    "old_section_id": old_section_id,
                    "new_section_id": new_section_id,
                    "new_instructor": new_section["instructor"],
                    "new_days": new_section["days"],
                    "new_start_time": new_section["start_time"],
                    "new_end_time": new_section["end_time"],
                }
            )

        registration["total_tuition"] = sum(
            c["tuition"] for c in registration["courses"]
        )

        return json.dumps(
            {
                "registration_id": registration_id,
                "changes": changes,
                "new_total_tuition": registration["total_tuition"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "switch_sections",
                "description": (
                    "Switch sections for one or more courses in a registration. Note: the API does not check "
                    "for schedule conflicts. The agent must verify there are no time conflicts before calling. "
                    "The agent needs to explain the section switch detail and ask for explicit user confirmation "
                    "(yes/no) to proceed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "registration_id": {
                            "type": "string",
                            "description": "The registration id, such as 'REGGV6TOLA'.",
                        },
                        "switches": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "course_id": {
                                        "type": "string",
                                        "description": "The course id to switch sections for, such as 'CS120'.",
                                    },
                                    "new_section_id": {
                                        "type": "string",
                                        "description": "The new section id, such as 'CS120-002'.",
                                    },
                                },
                                "required": ["course_id", "new_section_id"],
                            },
                            "description": "List of section switches to make.",
                        },
                    },
                    "required": ["registration_id", "switches"],
                },
            },
        }
