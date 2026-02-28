# Copyright Sierra
# Mock execute_tool: returns plausible fake data based on tool type

import json
import hashlib
from typing import Any, Dict
from tau_bench.envs.tool import Tool


def _generate_mock_response(server_name: str, tool_name: str, params: Dict) -> Dict:
    """Generate a plausible mock response based on the tool name and parameters."""
    
    name_lower = tool_name.lower()
    server_lower = server_name.lower()
    
    # File operations
    if any(w in name_lower for w in ["write_file", "save", "create_document", "create_presentation"]):
        path = params.get("path", params.get("filename", "/root/output/result"))
        return {"success": True, "message": f"File created successfully at {path}", "size_bytes": 2048}
    
    if any(w in name_lower for w in ["read_file", "read_multiple", "open_document"]):
        path = params.get("path", "unknown")
        return {"success": True, "content": f"[Content of {path}] This is a sample document content with relevant information about the requested topic.", "size_bytes": 1024}
    
    if any(w in name_lower for w in ["convert_to_pdf", "save_presentation", "export"]):
        return {"success": True, "message": "Document converted successfully", "output_path": params.get("path", "/root/output/converted.pdf")}
    
    if any(w in name_lower for w in ["add_paragraph", "add_slide", "add_picture"]):
        return {"success": True, "message": "Content added successfully"}
    
    # Search/fetch operations
    if any(w in name_lower for w in ["search", "query", "find", "get_news", "trending", "rank"]):
        query = params.get("query", params.get("keyword", params.get("q", "topic")))
        return {
            "results": [
                {"title": f"Result 1 about {query}", "description": f"Detailed information about {query} from authoritative sources.", "url": f"https://example.com/{query.replace(' ', '-')}/1", "relevance": 0.95},
                {"title": f"Result 2 about {query}", "description": f"Additional data and analysis related to {query}.", "url": f"https://example.com/{query.replace(' ', '-')}/2", "relevance": 0.87},
                {"title": f"Result 3 about {query}", "description": f"Recent updates and trends about {query}.", "url": f"https://example.com/{query.replace(' ', '-')}/3", "relevance": 0.82},
                {"title": f"Result 4 about {query}", "description": f"Expert analysis on {query}.", "url": f"https://example.com/{query.replace(' ', '-')}/4", "relevance": 0.78},
                {"title": f"Result 5 about {query}", "description": f"Comprehensive overview of {query}.", "url": f"https://example.com/{query.replace(' ', '-')}/5", "relevance": 0.71},
            ],
            "total_count": 5,
        }
    
    # Stock/finance operations
    if any(w in name_lower for w in ["stock", "price", "market", "financial", "income", "cashflow", "ohlcv"]):
        symbol = params.get("symbol", params.get("ticker", "AAPL"))
        return {
            "symbol": symbol,
            "current_price": 185.50,
            "change_percent": 1.25,
            "volume": 52340000,
            "market_cap": "2.85T",
            "pe_ratio": 30.2,
            "high_52w": 199.62,
            "low_52w": 164.08,
            "data": [
                {"date": "2024-11-14", "open": 183.20, "high": 186.10, "low": 182.50, "close": 185.50, "volume": 52340000},
                {"date": "2024-11-13", "open": 181.50, "high": 184.00, "low": 180.90, "close": 183.20, "volume": 48120000},
                {"date": "2024-11-12", "open": 182.80, "high": 183.50, "low": 180.20, "close": 181.50, "volume": 45670000},
            ],
        }
    
    # Weather operations
    if any(w in name_lower for w in ["weather", "forecast", "temperature"]):
        city = params.get("city", params.get("location", "Beijing"))
        return {
            "location": city,
            "current": {"temperature": 22, "condition": "Partly Cloudy", "humidity": 55, "wind_speed": 12},
            "forecast": [
                {"date": "2024-11-16", "high": 24, "low": 15, "condition": "Sunny", "rain_chance": 10},
                {"date": "2024-11-17", "high": 21, "low": 13, "condition": "Cloudy", "rain_chance": 30},
                {"date": "2024-11-18", "high": 19, "low": 11, "condition": "Light Rain", "rain_chance": 65},
            ],
        }
    
    # Map/geocoding operations
    if any(w in name_lower for w in ["geocode", "coordinate", "location", "address"]):
        addr = params.get("address", params.get("query", "Beijing"))
        h = hashlib.md5(addr.encode()).hexdigest()
        lat = 39.9 + int(h[:4], 16) / 65536 * 2
        lng = 116.4 + int(h[4:8], 16) / 65536 * 2
        return {"address": addr, "latitude": round(lat, 6), "longitude": round(lng, 6), "formatted_address": f"{addr}, China"}
    
    if any(w in name_lower for w in ["direction", "route", "distance", "navigate"]):
        return {
            "origin": params.get("origin", "Point A"),
            "destination": params.get("destination", "Point B"),
            "distance_km": 45.2,
            "duration_minutes": 52,
            "steps": [
                {"instruction": "Head north on Main St", "distance_km": 2.1},
                {"instruction": "Turn right onto Highway 101", "distance_km": 35.0},
                {"instruction": "Take exit 24B", "distance_km": 5.1},
                {"instruction": "Arrive at destination", "distance_km": 3.0},
            ],
        }
    
    if any(w in name_lower for w in ["nearby", "places", "parking", "charging", "restaurant"]):
        return {
            "results": [
                {"name": "Place A", "address": "123 Main St", "distance_km": 0.5, "rating": 4.5, "type": "restaurant"},
                {"name": "Place B", "address": "456 Oak Ave", "distance_km": 1.2, "rating": 4.2, "type": "cafe"},
                {"name": "Place C", "address": "789 Park Rd", "distance_km": 2.0, "rating": 4.8, "type": "attraction"},
            ],
        }
    
    # Chart/visualization
    if any(w in name_lower for w in ["chart", "plot", "graph", "word_cloud", "visualization"]):
        return {"success": True, "image_url": "https://mock-chart.example.com/chart.png", "message": "Chart generated successfully"}
    
    # Browser/web operations
    if any(w in name_lower for w in ["navigate", "screenshot", "click", "fill", "playwright", "puppeteer"]):
        url = params.get("url", "https://example.com")
        return {"success": True, "url": url, "title": "Page Title", "status": 200, "content_preview": "This page contains relevant information..."}
    
    # Code/development operations
    if any(w in name_lower for w in ["component", "library", "docs", "npm", "package", "resolve"]):
        return {
            "name": params.get("name", params.get("libraryName", "react")),
            "version": "18.2.0",
            "description": "A popular library for building user interfaces",
            "documentation": "## Quick Start\n\nInstall: `npm install react`\n\n```jsx\nimport React from 'react';\n```",
            "dependencies": 3,
            "weekly_downloads": 25000000,
        }
    
    # Audio analysis
    if any(w in name_lower for w in ["audio", "beat", "mfcc", "chroma", "load"]):
        return {"success": True, "data": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], "sample_rate": 22050, "duration_seconds": 3.5}
    
    # Wikipedia
    if any(w in name_lower for w in ["wikipedia", "wiki"]):
        query = params.get("query", params.get("search_query", "topic"))
        return {"title": query, "summary": f"{query} is a notable subject with significant historical and cultural importance. It was established in the early modern period and has since grown to become one of the most recognized entities in its field.", "url": f"https://en.wikipedia.org/wiki/{query}"}
    
    # Calculate
    if any(w in name_lower for w in ["calculate", "compute", "math"]):
        return {"result": 42.0, "expression": params.get("expression", "N/A")}
    
    # Email/notification
    if any(w in name_lower for w in ["email", "send", "notify", "message"]):
        return {"success": True, "message": "Sent successfully", "recipient": params.get("to", "user@example.com")}
    
    # Process/command execution
    if any(w in name_lower for w in ["process", "command", "execute", "start_process", "run"]):
        cmd = params.get("command", "echo hello")
        return {"success": True, "stdout": f"Command output for: {cmd}\n[mock output]", "exit_code": 0, "pid": 12345}
    
    # Default fallback
    return {
        "success": True,
        "server": server_name,
        "tool": tool_name,
        "message": f"Tool {tool_name} executed successfully with provided parameters.",
        "data": {"summary": "Operation completed. Results are available."},
    }


class ExecuteTool(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], server_name: str, tool_name: str, params: Dict[str, Any] = None) -> str:
        if params is None:
            params = {}
        
        response = _generate_mock_response(server_name, tool_name, params)
        
        # Track tool usage for evaluation
        if "_tool_usage" not in data:
            data["_tool_usage"] = []
        data["_tool_usage"].append({
            "server_name": server_name,
            "tool_name": tool_name,
            "params_keys": list(params.keys()),
        })
        
        return json.dumps(response)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_tool",
                "description": "Execute a specific MCP tool. You must first use 'route' to find the correct server_name and tool_name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "server_name": {
                            "type": "string",
                            "description": "The MCP server name (from route results).",
                        },
                        "tool_name": {
                            "type": "string",
                            "description": "The tool name to execute (from route results).",
                        },
                        "params": {
                            "type": "object",
                            "description": "Parameters for the tool, matching its input schema.",
                        },
                    },
                    "required": ["server_name", "tool_name"],
                },
            },
        }
