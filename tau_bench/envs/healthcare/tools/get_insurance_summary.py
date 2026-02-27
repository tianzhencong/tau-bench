# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

INSURANCE_PLANS = {
    "basic": {
        "plan_name": "Basic",
        "coverage_percentage": 60,
        "copay_per_visit": 40,
        "annual_deductible": 2000,
    },
    "standard": {
        "plan_name": "Standard",
        "coverage_percentage": 80,
        "copay_per_visit": 25,
        "annual_deductible": 1000,
    },
    "premium": {
        "plan_name": "Premium",
        "coverage_percentage": 90,
        "copay_per_visit": 10,
        "annual_deductible": 500,
    },
}


class GetInsuranceSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], patient_id: str) -> str:
        patients = data["patients"]
        if patient_id not in patients:
            return "Error: patient not found"

        patient = patients[patient_id]
        plan_key = patient["insurance_plan"].lower()
        if plan_key not in INSURANCE_PLANS:
            return "Error: unknown insurance plan"

        plan = INSURANCE_PLANS[plan_key]
        deductible_met = patient.get("deductible_met_this_year", 0)
        remaining_deductible = max(0, plan["annual_deductible"] - deductible_met)

        return json.dumps(
            {
                "patient_id": patient_id,
                "insurance_plan": plan["plan_name"],
                "coverage_percentage": plan["coverage_percentage"],
                "copay_per_visit": plan["copay_per_visit"],
                "annual_deductible": plan["annual_deductible"],
                "deductible_met_this_year": deductible_met,
                "remaining_deductible": remaining_deductible,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_insurance_summary",
                "description": "Get the insurance summary for a patient, including plan details, coverage percentage, copay per visit, annual deductible, amount met this year, and remaining deductible.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "The patient id, such as 'P10001'.",
                        },
                    },
                    "required": ["patient_id"],
                },
            },
        }
