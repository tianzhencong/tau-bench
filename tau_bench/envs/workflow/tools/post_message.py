# Copyright Sierra

import hashlib
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class PostMessage(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], from_id: str, to_id: str, content: str
    ) -> str:
        msg_id = "MSG_" + hashlib.md5(
            f"{from_id}_{to_id}_{content}".encode()
        ).hexdigest()[:10]
        message = {
            "message_id": msg_id,
            "from": from_id,
            "to": to_id,
            "subject": content[:50],
            "date": "2024-11-15",
            "read": False,
        }
        data["messages"].append(message)
        return json.dumps(
            {"message_id": msg_id, "status": "sent", "to": to_id}
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "post_message",
                "description": "Post an internal message from one employee to another.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_id": {
                            "type": "string",
                            "description": "The employee ID of the sender.",
                        },
                        "to_id": {
                            "type": "string",
                            "description": "The employee ID of the recipient.",
                        },
                        "content": {
                            "type": "string",
                            "description": "The message content.",
                        },
                    },
                    "required": ["from_id", "to_id", "content"],
                },
            },
        }
