# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class SendEmail(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        from_id: str,
        to_email: str,
        subject: str,
        body: str,
        attachment_ref: str = "",
    ) -> str:
        email_id = "EMAIL_" + hashlib.md5(
            f"{from_id}_{to_email}_{subject}".encode()
        ).hexdigest()[:10]

        email_record = {
            "email_id": email_id,
            "from_id": from_id,
            "to_email": to_email,
            "subject": subject,
            "body": body,
        }
        if attachment_ref:
            intermediate = data.get("_intermediate_results", {})
            report = data.get("generated_reports", {}).get(attachment_ref)
            inter_data = intermediate.get(attachment_ref)
            if report:
                email_record["attachment"] = attachment_ref
            elif inter_data:
                email_record["attachment"] = attachment_ref
            else:
                email_record["attachment"] = attachment_ref
        data["sent_emails"].append(email_record)
        return json.dumps({"email_id": email_id, "status": "sent", "to": to_email})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an email from an employee to a recipient. Optionally attach a report or data reference.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_id": {
                            "type": "string",
                            "description": "The employee ID of the sender.",
                        },
                        "to_email": {
                            "type": "string",
                            "description": "The recipient's email address.",
                        },
                        "subject": {
                            "type": "string",
                            "description": "The email subject line.",
                        },
                        "body": {
                            "type": "string",
                            "description": "The email body content.",
                        },
                        "attachment_ref": {
                            "type": "string",
                            "description": "Optional reference key for an attachment (report_id or data_ref). Leave empty for no attachment.",
                        },
                    },
                    "required": ["from_id", "to_email", "subject", "body"],
                },
            },
        }
