# Copyright Sierra
# Mock route tool: keyword-based tool retrieval from 525 MCP tools

import json
import os
import re
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

_TOOLS_CACHE = None

def _load_tools():
    global _TOOLS_CACHE
    if _TOOLS_CACHE is not None:
        return _TOOLS_CACHE
    
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mcp_tools.json")
    with open(path) as f:
        servers = json.load(f)
    
    flat = []
    for server in servers:
        server_name_display = server.get("name", "")
        category = server.get("category", "")
        for srv_key, srv_data in server.get("tools", {}).items():
            if isinstance(srv_data, dict) and "tools" in srv_data:
                for tool_def in srv_data["tools"]:
                    flat.append({
                        "server_name": srv_key,
                        "server_display": server_name_display,
                        "category": category,
                        "tool_name": tool_def.get("name", ""),
                        "tool_description": tool_def.get("description", ""),
                        "input_schema": tool_def.get("inputSchema", {}),
                    })
    _TOOLS_CACHE = flat
    return flat


def _keyword_match(query: str, tools: List[Dict]) -> List[Dict]:
    query_lower = query.lower()
    query_words = set(re.findall(r'[a-z]+', query_lower))
    
    scored = []
    for t in tools:
        text = f"{t['server_display']} {t['tool_name']} {t['tool_description']} {t['category']}".lower()
        text_words = set(re.findall(r'[a-z]+', text))
        overlap = len(query_words & text_words)
        if overlap > 0:
            scored.append((overlap, t))
    
    scored.sort(key=lambda x: -x[0])
    return [s[1] for s in scored[:5]]


class Route(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], query: str) -> str:
        tools = _load_tools()
        matches = _keyword_match(query, tools)
        
        if not matches:
            return json.dumps({"success": False, "message": "No matching tools found"})
        
        results = []
        for m in matches:
            results.append({
                "server_name": m["server_name"],
                "tool_name": m["tool_name"],
                "tool_description": m["tool_description"][:200],
                "category": m["category"],
                "input_schema": m["input_schema"],
            })
        
        return json.dumps({"success": True, "matched_tools": results})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "route",
                "description": "Search the MCP tool catalog to find relevant tools for your task. Describe what kind of tool you need in natural language.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language description of the tool you need, e.g., 'search for stock price data' or 'create a PDF document'.",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
