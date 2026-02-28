# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FindEmployeeByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        employees = data["employees"]
        for emp_id, emp in employees.items():
            if emp["email"].lower() == email.lower():
                return emp_id
        return "Error: employee not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_employee_by_email",
                "description": "Find an employee's ID by their email address. Returns the employee_id if found.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email address of the employee, e.g. 'john.doe@company.com'.",
                        },
                    },
                    "required": ["email"],
                },
            },
        }
