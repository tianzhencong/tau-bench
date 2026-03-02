# Copyright Sierra
# Improved execute_tool: returns diverse, parameterized mock data

import json
import hashlib
from typing import Any, Dict
from tau_bench.envs.tool import Tool


def _hash_seed(server_name: str, tool_name: str, params: Dict) -> int:
    """Generate a deterministic seed from inputs for varied but reproducible responses."""
    seed_str = f"{server_name}_{tool_name}_{json.dumps(params, sort_keys=True)}"
    return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)


def _generate_mock_response(server_name: str, tool_name: str, params: Dict) -> Dict:
    """Generate parameterized mock data that varies based on inputs."""
    
    seed = _hash_seed(server_name, tool_name, params)
    name_lower = tool_name.lower()
    
    # Use seed to generate varied numbers
    price = round(50 + (seed % 500) + (seed % 100) / 100, 2)
    count = 3 + seed % 8
    rating = round(3.0 + (seed % 20) / 10, 1)
    
    # File operations
    if any(w in name_lower for w in ["write_file", "save", "create_document", "create_presentation", "save_presentation"]):
        path = params.get("path", params.get("filename", f"/root/output/result_{seed % 1000}"))
        return {"success": True, "message": f"File created at {path}", "size_bytes": 1024 + seed % 5000}
    
    if any(w in name_lower for w in ["read_file", "read_multiple", "open_document"]):
        path = params.get("path", "file")
        return {"success": True, "content": f"Document content from {path}. Contains {count} sections with detailed information about the topic.", "size_bytes": 512 + seed % 3000}
    
    if any(w in name_lower for w in ["convert_to_pdf", "export"]):
        return {"success": True, "output_path": params.get("path", f"/root/output/converted_{seed%100}.pdf")}
    
    if any(w in name_lower for w in ["add_paragraph", "add_slide", "add_picture"]):
        return {"success": True, "message": "Content added successfully", "element_id": seed % 100}
    
    # Search/fetch - return varied results
    if any(w in name_lower for w in ["search", "query", "find", "get_news", "trending", "rank", "get_stories"]):
        query = params.get("query", params.get("keyword", params.get("q", "topic")))
        results = []
        for j in range(count):
            item_seed = seed + j * 7
            results.append({
                "title": f"{'Top' if j==0 else 'Notable'} result about {query} #{j+1}",
                "description": f"{'Comprehensive' if j%2==0 else 'In-depth'} coverage of {query} with {10+item_seed%90} references.",
                "url": f"https://source{j+1}.example.com/{query.replace(' ', '-')[:30]}",
                "date": f"2024-{11-j%3:02d}-{15-j:02d}",
                "relevance": round(0.95 - j * 0.05, 2),
            })
        return {"results": results, "total_count": count + seed % 20}
    
    # Stock/finance - varied per symbol
    if any(w in name_lower for w in ["stock", "price", "market", "financial", "income", "cashflow", "ohlcv", "fundamental", "ticker"]):
        symbol = params.get("symbol", params.get("ticker", params.get("code", "UNKNOWN")))
        sym_seed = int(hashlib.md5(symbol.encode()).hexdigest()[:8], 16)
        base_price = 20 + (sym_seed % 980)
        change = round(-5 + (sym_seed % 100) / 10, 2)
        return {
            "symbol": symbol,
            "name": f"{symbol} Corp",
            "current_price": base_price,
            "change_percent": change,
            "volume": 1000000 + sym_seed % 50000000,
            "market_cap": f"{base_price * (10 + sym_seed % 90) / 10:.1f}B",
            "pe_ratio": round(10 + sym_seed % 40 + (sym_seed % 10) / 10, 1),
            "high_52w": round(base_price * 1.3, 2),
            "low_52w": round(base_price * 0.7, 2),
            "data": [
                {"date": f"2024-11-{15-d}", "open": round(base_price*(1-0.01*d), 2), "close": round(base_price*(1+0.005*d), 2), "volume": 1000000+d*100000}
                for d in range(min(5, int(params.get("days", 5))))
            ],
        }
    
    # Weather - varied by city
    if any(w in name_lower for w in ["weather", "forecast", "temperature"]):
        city = params.get("city", params.get("location", "Unknown"))
        city_seed = int(hashlib.md5(city.encode()).hexdigest()[:8], 16)
        base_temp = 5 + city_seed % 30
        conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear", "Overcast"]
        return {
            "location": city,
            "current": {"temperature": base_temp, "condition": conditions[city_seed % len(conditions)], "humidity": 30 + city_seed % 50, "wind_speed": 5 + city_seed % 20},
            "forecast": [
                {"date": f"2024-11-{16+d}", "high": base_temp + 3 - d, "low": base_temp - 5 + d, "condition": conditions[(city_seed + d) % len(conditions)], "rain_chance": (city_seed * d) % 80}
                for d in range(3)
            ],
        }
    
    # Map/geocoding - varied by address
    if any(w in name_lower for w in ["geocode", "coordinate", "location", "address"]):
        addr = params.get("address", params.get("query", params.get("name", "Unknown")))
        h = hashlib.md5(addr.encode()).hexdigest()
        lat = round(30 + int(h[:4], 16) / 6553.6, 6)
        lng = round(100 + int(h[4:8], 16) / 3276.8, 6)
        return {"address": addr, "latitude": lat, "longitude": lng, "formatted_address": f"{addr}, detailed location"}
    
    if any(w in name_lower for w in ["direction", "route", "distance"]):
        origin = params.get("origin", "A")
        dest = params.get("destination", "B")
        dist_seed = _hash_seed("", "", {"o": origin, "d": dest})
        dist = round(10 + dist_seed % 500, 1)
        return {"origin": origin, "destination": dest, "distance_km": dist, "duration_minutes": int(dist * 1.2), "steps": [{"instruction": f"Drive toward {dest}", "distance_km": dist}]}
    
    if any(w in name_lower for w in ["nearby", "places", "parking", "charging", "restaurant", "meeting"]):
        results = []
        for j in range(count):
            results.append({"name": f"Location #{seed+j}", "address": f"{100+j*10} Main St", "distance_km": round(0.3 + j * 0.5, 1), "rating": round(3.5 + (seed+j)%15/10, 1)})
        return {"results": results}
    
    # Chart/visualization
    if any(w in name_lower for w in ["chart", "plot", "graph", "word_cloud", "visualization"]):
        return {"success": True, "image_url": f"https://charts.example.com/{seed%10000}.png", "width": 800, "height": 600}
    
    # Browser
    if any(w in name_lower for w in ["navigate", "screenshot", "click", "fill", "playwright", "puppeteer"]):
        url = params.get("url", "https://example.com")
        return {"success": True, "url": url, "title": f"Page at {url[:40]}", "status": 200}
    
    # Code/docs
    if any(w in name_lower for w in ["component", "library", "docs", "npm", "package", "resolve", "get_library"]):
        name = params.get("name", params.get("libraryName", params.get("package", "lib")))
        return {"name": name, "version": f"{1+seed%5}.{seed%10}.{seed%20}", "description": f"A library for {name}", "documentation": f"# {name}\n\nInstall: `npm install {name}`\n\n## Usage\n```\nimport {name}\n```"}
    
    # Audio
    if any(w in name_lower for w in ["audio", "beat", "mfcc", "chroma", "load", "music"]):
        return {"success": True, "data": [[round(0.1*j + seed%10/100, 3) for j in range(5)] for _ in range(3)], "sample_rate": 22050, "duration_seconds": round(2 + seed % 30, 1)}
    
    # Wikipedia
    if any(w in name_lower for w in ["wikipedia", "wiki"]):
        q = params.get("query", params.get("search_query", "topic"))
        return {"title": q, "summary": f"{q} is a significant subject. It was established in {1900+seed%124} and has since become influential in its field with {10+seed%90} notable achievements.", "url": f"https://en.wikipedia.org/wiki/{q}"}
    
    # Train/transport
    if any(w in name_lower for w in ["train", "ticket", "station", "flight"]):
        return {"results": [
            {"id": f"T{seed+j}", "departure": f"{8+j}:00", "arrival": f"{12+j}:30", "duration": f"{4+j%2}h{30-j*10}m", "price": 200 + seed%500 + j*50, "available": (seed+j)%3 != 0}
            for j in range(count)
        ]}
    
    # Calculate
    if any(w in name_lower for w in ["calculate", "compute", "math"]):
        expr = params.get("expression", "0")
        try:
            allowed = set("0123456789+-*/.() ")
            if all(c in allowed for c in expr):
                return {"result": eval(expr), "expression": expr}
        except:
            pass
        return {"result": seed % 1000, "expression": expr}
    
    # Email/message
    if any(w in name_lower for w in ["email", "send", "notify", "message"]):
        return {"success": True, "message_id": f"MSG{seed%100000}", "status": "sent"}
    
    # Process/command
    if any(w in name_lower for w in ["process", "command", "execute", "start_process", "run"]):
        cmd = params.get("command", "echo ok")
        return {"success": True, "stdout": f"[output of: {cmd[:50]}]", "exit_code": 0}
    
    # Airbnb/booking
    if any(w in name_lower for w in ["listing", "airbnb", "hotel", "booking"]):
        return {"results": [
            {"id": f"L{seed+j}", "name": f"{'Cozy' if j%2==0 else 'Luxury'} Place #{seed+j}", "price_per_night": 80+seed%200+j*30, "rating": round(3.5+(seed+j)%15/10, 1), "reviews": 10+seed%200}
            for j in range(count)
        ]}
    
    # Default
    return {"success": True, "tool": tool_name, "server": server_name, "data": {"info": f"Result from {tool_name} with {len(params)} parameters", "items_count": count}}


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
