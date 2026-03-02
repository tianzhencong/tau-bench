# Copyright Sierra
# Per-tool mock response templates for the 150 tools used in 95 LiveMCPBench tasks
# Organized by category. Each tool returns semantically appropriate data.

import hashlib
import json
from typing import Dict, Any


def _seed(server: str, tool: str, params: Dict) -> int:
    return int(hashlib.md5(f"{server}_{tool}_{json.dumps(params, sort_keys=True)}".encode()).hexdigest()[:8], 16)


# === NEWS / TRENDING ===
NEWS_TOOLS = {
    "get-36kr-trending", "get-9to5mac-news", "get-bbc-news", "get-bilibili-rank",
    "get-douban-rank", "get-douyin-trending", "get-ifanr-news", "get-infoq-news",
    "get-juejin-article-rank", "get-netease-news-trending", "get-nytimes-news",
    "get-smzdm-rank", "get-theverge-news", "get-weibo-trending", "get-weread-rank",
    "get-zhihu-trending", "getStories", "get_github_trending_repositories", "get_news",
    "get-gcores-new",
}

def news_response(tool: str, params: Dict, s: int) -> Dict:
    source_map = {
        "get-36kr-trending": "36氪", "get-bbc-news": "BBC News", "get-bilibili-rank": "哔哩哔哩",
        "get-douban-rank": "豆瓣", "get-douyin-trending": "抖音", "get-weibo-trending": "微博",
        "get-weread-rank": "微信读书", "get-zhihu-trending": "知乎", "get-nytimes-news": "NY Times",
        "get-theverge-news": "The Verge", "get-9to5mac-news": "9to5Mac", "getStories": "Hacker News",
        "get-smzdm-rank": "什么值得买", "get_news": "Yahoo Finance News", "get-gcores-new": "机核",
        "get_github_trending_repositories": "GitHub Trending",
    }
    source = source_map.get(tool, "News")
    topics = ["AI革命","量子计算突破","新能源汽车","芯片战争","太空探索","气候变化","数字货币","元宇宙","机器人","基因编辑",
              "Tech layoffs","Apple Vision Pro","SpaceX launch","Market rally","AI regulation"]
    items = []
    count = 5 + s % 6
    for j in range(count):
        js = s + j * 7
        items.append({
            "rank": j + 1,
            "title": f"{topics[(js)%len(topics)]}{'的最新进展' if js%2==0 else '引发热议'}",
            "hot_score": 10000 - j * 800 + js % 500,
            "url": f"https://{source.lower().replace(' ','')}.com/article/{js%100000}",
            "source": source,
            "publish_time": f"2024-11-{15-j%5:02d} {8+j}:00",
        })
    return {"source": source, "items": items, "update_time": "2024-11-15 10:00"}


# === FINANCE ===
FINANCE_TOOLS = {
    "get-crypto-price", "get-market-analysis", "get_asset_price", "get_cashflow",
    "get_current_stock_price", "get_historical_stock_prices", "get_income_statement",
    "get_stock_fundamental", "get_stock_market_cap", "get_stock_ohlcv",
    "get_stock_price_date_range", "get_ticker_info", "load_all_tickers",
    "get_cnn_fear_greed_index", "get_crypto_fear_greed_index", "get_recommendations",
    "exchange_rate",
}

def finance_response(tool: str, params: Dict, s: int) -> Dict:
    symbol = params.get("symbol", params.get("ticker", params.get("code", params.get("asset", "UNKNOWN"))))
    sym_s = int(hashlib.md5(symbol.encode()).hexdigest()[:8], 16)
    base = 20 + sym_s % 980
    chg = round(-8 + sym_s % 160 / 10, 2)

    if "ohlcv" in tool or "historical" in tool or "date_range" in tool:
        days = int(params.get("days", params.get("period_days", 30)))
        data = [{"date": f"2024-{11 - d//30:02d}-{15 - d%30:02d}", "open": round(base*(1-0.002*d), 2), "high": round(base*(1+0.005*d), 2), "low": round(base*(1-0.008*d), 2), "close": round(base*(1+0.001*d), 2), "volume": 1000000+d*50000} for d in range(min(days, 30))]
        return {"symbol": symbol, "data": data, "period": f"{days} days"}

    if "fundamental" in tool:
        return {"symbol": symbol, "per": round(10+sym_s%30+sym_s%10/10, 1), "pbr": round(1+sym_s%40/10, 1), "dividend_yield": round(sym_s%50/10, 2), "roe": round(5+sym_s%25, 1), "market_cap": f"{base*(10+sym_s%90)/10:.0f}B"}

    if "income" in tool:
        rev = base * 1000000
        return {"symbol": symbol, "revenue": rev, "net_income": round(rev*0.15, 0), "gross_profit": round(rev*0.4, 0), "operating_income": round(rev*0.2, 0), "period": "2024-Q3"}

    if "cashflow" in tool:
        return {"symbol": symbol, "operating_cashflow": base*500000, "investing_cashflow": -base*200000, "financing_cashflow": -base*100000, "free_cashflow": base*300000, "period": "2024-Q3"}

    if "market_cap" in tool:
        return {"symbol": symbol, "market_cap": base * (10+sym_s%90) * 1000000, "market_cap_display": f"{base*(10+sym_s%90)/10:.1f}B", "shares_outstanding": (10+sym_s%90)*1000000}

    if "ticker" in tool or "all_ticker" in tool.lower():
        return {"tickers": [{"symbol": f"T{i}", "name": f"Company {i}", "market": "KOSPI" if sym_s%2==0 else "KOSDAQ"} for i in range(s%20+5)]}

    if "recommendation" in tool:
        return {"symbol": symbol, "recommendations": [{"firm": f"{'Goldman' if s%3==0 else 'Morgan' if s%3==1 else 'JP Morgan'} Sachs", "rating": ["Buy","Hold","Sell"][s%3], "target_price": round(base*1.2, 2)}]}

    if "crypto" in tool or "fear" in tool:
        return {"index": 40+s%50, "label": ["Extreme Fear","Fear","Neutral","Greed","Extreme Greed"][s%5], "timestamp": "2024-11-15"}

    if "exchange_rate" in tool:
        return {"from": params.get("from","USD"), "to": params.get("to","CNY"), "rate": round(7.1+s%10/100, 4), "timestamp": "2024-11-15"}

    # Default stock price
    return {"symbol": symbol, "name": f"{symbol} Corp", "current_price": base, "change_percent": chg, "volume": 1000000+sym_s%50000000, "market_cap": f"{base*(10+sym_s%90)/10:.1f}B", "pe_ratio": round(10+sym_s%40, 1), "high_52w": round(base*1.3, 2), "low_52w": round(base*0.7, 2)}


# === SEARCH / KNOWLEDGE ===
SEARCH_TOOLS = {
    "search_papers", "get_paper_data", "download_paper", "read_paper",
    "search_wikipedia", "get_article", "fetch", "deepwiki_fetch",
    "article_searcher", "trial_searcher", "variant_searcher", "trial_references",
    "research-with-keywords", "ddg-search", "duckduckgo_web_search",
    "search-museum-objects", "get-museum-object", "search_cards", "get_card_image",
    "package_search", "package_show", "search_components", "search_category",
    "summarize_article_for_query", "airbnb_search",
}

def search_response(tool: str, params: Dict, s: int) -> Dict:
    query = params.get("query", params.get("keyword", params.get("q", params.get("search_query", "topic"))))

    if "paper" in tool or "arxiv" in tool:
        return {"papers": [
            {"title": f"{'Deep Learning' if s%3==0 else 'Reinforcement Learning' if s%3==1 else 'NLP'} for {query} ({2024-j})", "authors": [f"Author {s+j}"], "abstract": f"We propose a novel approach to {query} that achieves state-of-the-art results...", "arxiv_id": f"{2024+j%2}.{10000+s+j}", "published": f"2024-{10-j:02d}-01", "citations": 50-j*10+s%30}
            for j in range(min(5, 3+s%4))
        ]}

    if "wikipedia" in tool or "wiki" in tool or tool == "get_article":
        if "get_article" in tool or "article" == tool.split("_")[-1]:
            return {"title": query, "content": f"# {query}\n\n{query} is a significant topic in its field. ## History\nIt was first described in {1900+s%124}. ## Overview\n{query} has been widely studied and applied in various domains including technology, science, and industry. Key developments include innovations in {['efficiency','scale','accuracy','reliability'][s%4]}. ## Applications\nModern applications of {query} span multiple industries. ## References\n1. Smith et al. (2023)\n2. Chen et al. (2024)", "url": f"https://en.wikipedia.org/wiki/{query}"}
        return {"results": [{"title": f"{query}", "snippet": f"Article about {query} covering history, applications, and recent developments.", "pageid": s%100000}]}

    if "museum" in tool:
        return {"objects": [{"object_id": s+j, "title": f"{'Ancient' if j%2==0 else 'Modern'} Artifact #{s+j}", "culture": ["Egyptian","Greek","Chinese","Roman"][j%4], "period": f"{1000+j*200} BCE", "medium": "Bronze"} for j in range(3+s%3)]}

    if "airbnb" in tool:
        return {"listings": [{"id": f"AB{s+j}", "name": f"{'Cozy' if j%2==0 else 'Luxury'} Stay in {query}", "price_per_night": 80+s%200+j*30, "rating": round(4.0+j%10/10, 1), "reviews": 20+s%100, "bedrooms": 1+j%3} for j in range(3+s%4)]}

    if "card" in tool:
        return {"cards": [{"id": s+j, "name": f"Card #{s+j}", "type": ["Monster","Spell","Trap"][j%3], "attack": 1000+j*500, "defense": 800+j*400} for j in range(3)]}

    if "package" in tool or "component" in tool or "npm" in tool:
        return {"packages": [{"name": query, "version": f"{1+s%5}.{s%10}.{s%20}", "description": f"A package for {query}", "weekly_downloads": 10000+s%1000000}]}

    # Generic search
    return {"results": [
        {"title": f"{'Comprehensive' if j==0 else 'In-depth' if j==1 else 'Expert'} guide to {query}", "snippet": f"{'Detailed analysis' if j%2==0 else 'Practical overview'} of {query} with {10+s%90+j*5} references and case studies.", "url": f"https://source{j+1}.example.com/{query[:20]}", "relevance": round(0.95-j*0.08, 2)}
        for j in range(3+s%4)
    ]}


# === TRANSPORT ===
TRANSPORT_TOOLS = {"get-tickets", "get-station-code-by-names", "get-station-code-of-citys"}

def transport_response(tool: str, params: Dict, s: int) -> Dict:
    if "station" in tool or "code" in tool:
        city = params.get("city_name", params.get("name", params.get("from_city", "北京")))
        codes = {"北京": "BJP", "北京南": "VNP", "上海": "SHH", "上海虹桥": "AOH", "成都": "CDW", "广州": "GZQ", "深圳": "SZQ", "杭州": "HZH", "南京": "NJH", "西安": "XAY"}
        code = codes.get(city, f"ST{s%1000}")
        return {"city": city, "station_code": code, "station_name": f"{city}站"}

    if "ticket" in tool:
        trains = []
        for j in range(4+s%4):
            js = s + j * 11
            t_type = ["G", "D", "K", "Z"][j%4]
            trains.append({
                "train_no": f"{t_type}{100+js%900}",
                "from_station": params.get("from_station", "BJP"),
                "to_station": params.get("to_station", "SHH"),
                "departure_time": f"{6+j*2:02d}:{js%60:02d}",
                "arrival_time": f"{10+j*2:02d}:{(js+30)%60:02d}",
                "duration": f"{4+j}h{js%60}m",
                "business_seat": {"price": 800+js%500, "available": js%5},
                "first_seat": {"price": 500+js%300, "available": 5+js%20},
                "second_seat": {"price": 250+js%200, "available": 20+js%100},
            })
        return {"trains": trains, "date": params.get("date", "2024-11-16")}

    return {"data": "transport result"}


# === MEDIA / VISUALIZATION ===
MEDIA_TOOLS = {"generate_word_cloud_chart", "generate_bar_chart", "generate_pie_chart", "convert_markdown_to_mindmap", "beat_track", "mfcc", "chroma_cqt", "load"}

def media_response(tool: str, params: Dict, s: int) -> Dict:
    if "chart" in tool or "cloud" in tool:
        return {"success": True, "image_url": f"https://charts.example.com/{s%10000}.png", "width": 800, "height": 600, "format": "png"}
    if "mindmap" in tool:
        return {"success": True, "mindmap_url": f"https://mindmaps.example.com/{s%10000}.svg", "nodes": 10+s%20}
    if "beat" in tool:
        return {"tempo": 80+s%80, "beats": [round(0.5+j*0.5, 2) for j in range(8)], "beat_times_count": 50+s%100}
    if "mfcc" in tool:
        return {"mfcc_coefficients": [[round(s%10/10+j*0.1+k*0.01, 3) for k in range(13)] for j in range(5)], "n_mfcc": 13, "sample_rate": 22050}
    if "chroma" in tool:
        return {"chroma_features": [[round(s%10/10+j*0.08, 3) for j in range(12)] for _ in range(5)], "n_chroma": 12}
    if "load" in tool:
        path = params.get("path", params.get("file_path", "/audio/sample.wav"))
        return {"success": True, "path": path, "duration_seconds": round(2+s%60, 1), "sample_rate": 22050, "channels": 1+s%2}
    return {"success": True, "data": "media result"}


# === MISC / OTHER ===
def other_response(tool: str, params: Dict, s: int) -> Dict:
    tl = tool.lower()

    if "current_time" in tl or "current_date" in tl or "get-current-date" in tl:
        return {"date": "2024-11-15", "time": "10:00:00", "timezone": "Asia/Shanghai", "day_of_week": "Friday"}

    if "weather" in tl:
        city = params.get("city", params.get("location", "Beijing"))
        cs = int(hashlib.md5(city.encode()).hexdigest()[:6], 16)
        return {"location": city, "current": {"temp": 5+cs%30, "condition": ["Sunny","Cloudy","Rainy","Clear"][cs%4], "humidity": 30+cs%50}, "forecast": [{"date": f"2024-11-{16+d}", "high": 10+cs%25-d, "low": cs%15-d, "condition": ["Sunny","Cloudy","Rainy"][d%3]} for d in range(3)]}

    if "calculate" in tl:
        expr = params.get("expression", "0")
        try:
            if all(c in "0123456789+-*/.() " for c in expr):
                return {"result": eval(expr), "expression": expr}
        except: pass
        return {"result": 42+s%100, "expression": expr}

    if "whois" in tl:
        domain = params.get("domain", "example.com")
        return {"domain": domain, "registrar": "GoDaddy", "creation_date": "2005-03-15", "expiry_date": "2025-03-15", "nameservers": [f"ns1.{domain}", f"ns2.{domain}"]}

    if "excel" in tl:
        if "read" in tl:
            return {"data": [[f"Row{r}Col{c}" for c in range(5)] for r in range(min(10, 3+s%8))], "sheet": params.get("sheet", "Sheet1"), "rows": 3+s%8}
        return {"success": True, "message": "Excel operation completed"}

    if "git" in tl:
        return {"commits": [{"hash": hashlib.md5(f"{s}{j}".encode()).hexdigest()[:7], "message": f"{'feat' if j%3==0 else 'fix' if j%3==1 else 'docs'}: update module {j}", "author": f"dev{j}@co.com", "date": f"2024-11-{15-j}"} for j in range(5)]}

    if "recipe" in tl or "cook" in tl or "whatToEat" in tl:
        return {"recipes": [{"name": f"{'红烧肉' if s%4==0 else '宫保鸡丁' if s%4==1 else '麻婆豆腐' if s%4==2 else '糖醋排骨'}", "difficulty": ["easy","medium","hard"][s%3], "time_minutes": 30+s%60, "ingredients": ["主料", "调料", "配菜"]}]}

    if "bazi" in tl or "calendar" in tl:
        return {"bazi": "甲子 丙寅 戊辰 庚午", "wuxing": {"metal": 2, "wood": 3, "water": 1, "fire": 2, "earth": 2}, "zodiac": "Dragon"}

    if "lol" in tl or "valorant" in tl or "opgg" in tl:
        return {"characters": [{"name": f"Champion {s+j}", "win_rate": round(48+j*0.5+s%5, 1), "pick_rate": round(5+j+s%10, 1), "tier": ["S","A","B","C"][j%4]} for j in range(5)]}

    if "library" in tl or "component" in tl or "resolve" in tl or "docs" in tl:
        name = params.get("name", params.get("libraryName", params.get("library_id", "lib")))
        return {"name": name, "version": f"{1+s%5}.{s%10}.{s%20}", "description": f"Library for {name}", "documentation": f"# {name}\n\nInstall: `npm install {name}`\n\n```js\nimport {{ {name} }} from '{name}';\n```\n\n## Components\n- Button\n- Input\n- Card"}

    if "npm" in tl:
        pkg = params.get("package", params.get("name", "react"))
        return {"package": pkg, "version": f"{1+s%18}.{s%10}.{s%5}", "size_kb": 50+s%500, "dependencies": 3+s%20, "weekly_downloads": 100000+s%5000000}

    if "pdf" in tl and "read" in tl:
        return {"pages": 5+s%20, "text": f"PDF content page 1: This document covers important information about the requested topic. It contains {5+s%20} pages of detailed analysis...", "metadata": {"author": "Author", "title": "Document"}}

    if "transcript" in tl or "youtube" in tl:
        return {"title": f"Video about {params.get('url', 'topic')[:30]}", "transcript": f"Welcome to this video. Today we'll discuss important topics including recent developments and future trends. [00:30] First point... [01:00] Second point...", "duration": f"{5+s%30}:00"}

    if "sitemap" in tl:
        url = params.get("url", "https://example.com")
        return {"url": url, "pages": [f"{url}/page{j}" for j in range(5+s%10)], "total": 5+s%10}

    if "image" in tl or "extract" in tl:
        return {"success": True, "image_path": f"/tmp/image_{s%1000}.png", "width": 800, "height": 600}

    if "validate" in tl or "mermaid" in tl:
        return {"valid": True, "message": "Diagram is valid"}

    if "text_diff" in tl:
        return {"changes": 3+s%5, "additions": 2+s%3, "deletions": 1+s%2, "diff": "+added line\n-removed line"}

    if "random" in tl:
        return {"value": s % 100, "min": 0, "max": 100}

    # Truly generic fallback
    return {"success": True, "tool": tool, "message": f"Completed {tool}", "data_items": 3+s%5}


def get_mock_response(server_name: str, tool_name: str, params: Dict) -> Dict:
    """Main dispatch function."""
    s = _seed(server_name, tool_name, params)

    if tool_name in NEWS_TOOLS:
        return news_response(tool_name, params, s)
    if tool_name in FINANCE_TOOLS:
        return finance_response(tool_name, params, s)
    if tool_name in SEARCH_TOOLS:
        return search_response(tool_name, params, s)
    if tool_name in TRANSPORT_TOOLS:
        return transport_response(tool_name, params, s)
    if tool_name in MEDIA_TOOLS:
        return media_response(tool_name, params, s)

    # Delegate to other_response for misc tools
    return other_response(tool_name, params, s)
