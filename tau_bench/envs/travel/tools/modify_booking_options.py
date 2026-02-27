# Copyright Sierra

import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ModifyBookingOptions(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        booking_id: str,
        changes: List[Dict[str, str]],
        payment_id: str,
    ) -> str:
        bookings = data["bookings"]
        packages = data["packages"]

        if booking_id not in bookings:
            return "Error: booking not found"

        booking = bookings[booking_id]
        if booking["status"] != "confirmed":
            return f"Error: booking status is '{booking['status']}', only confirmed bookings can be modified"

        package_id = booking["package_id"]
        if package_id not in packages:
            return "Error: associated package not found"

        package = packages[package_id]
        component_map = {c["component_id"]: c for c in package.get("components", [])}

        price_diff = 0
        applied_changes = []
        for change in changes:
            component_id = change["component_id"]
            new_option = change["new_option"]

            if component_id not in component_map:
                return f"Error: component {component_id} not found in package"

            component = component_map[component_id]
            if new_option not in component.get("options", {}):
                return f"Error: option '{new_option}' not found for component {component_id}"

            old_option = booking["selected_options"].get(component_id)
            old_modifier = 0
            if old_option and old_option in component.get("options", {}):
                old_modifier = component["options"][old_option].get("price_modifier", 0)
            new_modifier = component["options"][new_option].get("price_modifier", 0)

            price_diff += new_modifier - old_modifier
            booking["selected_options"][component_id] = new_option
            applied_changes.append(
                {
                    "component_id": component_id,
                    "old_option": old_option,
                    "new_option": new_option,
                    "price_change": new_modifier - old_modifier,
                }
            )

        booking["total_price"] += price_diff

        return json.dumps(
            {
                "booking_id": booking_id,
                "changes": applied_changes,
                "price_difference": price_diff,
                "new_total_price": booking["total_price"],
                "payment_id": payment_id,
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_booking_options",
                "description": "Modify the selected options for components in a confirmed booking. Returns the changes made and updated total price.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "The booking id.",
                        },
                        "changes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "component_id": {
                                        "type": "string",
                                        "description": "The component id to change.",
                                    },
                                    "new_option": {
                                        "type": "string",
                                        "description": "The new option name to select.",
                                    },
                                },
                                "required": ["component_id", "new_option"],
                            },
                            "description": "List of option changes to apply.",
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "The payment method id to use for any price difference.",
                        },
                    },
                    "required": ["booking_id", "changes", "payment_id"],
                },
            },
        }
