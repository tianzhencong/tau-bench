# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyRegistrationPayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        registration_id: str,
        new_payment_methods: List[Dict[str, Any]],
    ) -> str:
        registrations = data["registrations"]

        if registration_id not in registrations:
            return "Error: registration not found"

        registration = registrations[registration_id]
        if registration["status"] not in ("pending", "confirmed"):
            return f"Error: registration status is '{registration['status']}', only pending or confirmed registrations can have payment modified"

        student_id = registration["student_id"]
        student = data["students"][student_id]
        student_payment_ids = {pm["payment_id"] for pm in student["payment_methods"]}

        total_payment = sum(pm["amount"] for pm in new_payment_methods)
        if round(total_payment, 2) != round(registration["total_tuition"], 2):
            return f"Error: payment amounts ({total_payment}) do not add up to total tuition ({registration['total_tuition']})"

        for pm in new_payment_methods:
            if pm["payment_id"] not in student_payment_ids:
                return f"Error: payment method {pm['payment_id']} not found in student profile"

        registration["payment_history"] = [
            {
                "transaction_type": "payment",
                "amount": pm["amount"],
                "payment_method_id": pm["payment_id"],
            }
            for pm in new_payment_methods
        ]

        return json.dumps(
            {
                "registration_id": registration_id,
                "total_tuition": registration["total_tuition"],
                "payment_history": registration["payment_history"],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_registration_payment",
                "description": (
                    "Change the payment method(s) for a registration. The total of all payment amounts "
                    "must equal the registration's total tuition. The agent needs to explain the payment "
                    "modification detail and ask for explicit user confirmation (yes/no) to proceed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "registration_id": {
                            "type": "string",
                            "description": "The registration id, such as 'REGGV6TOLA'.",
                        },
                        "new_payment_methods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "payment_id": {
                                        "type": "string",
                                        "description": "The payment method id, such as 'credit_card_9531021' or 'financial_aid_324597'.",
                                    },
                                    "amount": {
                                        "type": "number",
                                        "description": "The amount to charge to this payment method.",
                                    },
                                },
                                "required": ["payment_id", "amount"],
                            },
                            "description": "List of payment methods and amounts. The total must equal the registration's total tuition.",
                        },
                    },
                    "required": ["registration_id", "new_payment_methods"],
                },
            },
        }
