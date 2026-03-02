# Copyright Sierra
# 95 LiveMCPBench tasks with ground truth actions (route → execute_tool chains)
# Actions derived from annotated Steps/Tools metadata

from tau_bench.types import Action, Task

TASKS = [
    # Task 0: Office | tools=6 | has GT
    Task(
        user_id="mcp_user_000",
        instruction="Generate a well-formatted PDF report titled wechat_reading_report.pdf in /root/pdf, summarizing current WeChat Reading trends and including a word cloud.",
        actions=[
        Action(name="route", kwargs={"query": "get-weread-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-weread-rank", "params": {}}),
        Action(name="route", kwargs={"query": "generate_word_cloud_chart"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-server-chart", "tool_name": "generate_word_cloud_chart", "params": {}}),
        Action(name="route", kwargs={"query": "create_document"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "create_document", "params": {}}),
        Action(name="route", kwargs={"query": "add_paragraph"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_paragraph", "params": {}}),
        Action(name="route", kwargs={"query": "add_picture"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_picture", "params": {}}),
        Action(name="route", kwargs={"query": "convert_to_pdf"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "convert_to_pdf", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 1: Leisure | tools=4 | has GT
    Task(
        user_id="mcp_user_001",
        instruction="Please perform a comprehensive analysis of the audio file located at /root/music/mixkit-retro-game-emergency-alarm-1000.wav. The analysis should include beat tracking, MFCC extraction, and chroma CQT calculation. Upon completion, please provide the resulting data along with a brief summary of the findings.",
        actions=[
        Action(name="route", kwargs={"query": "load"}),
        Action(name="execute_tool", kwargs={"server_name": "music-analysis", "tool_name": "load", "params": {}}),
        Action(name="route", kwargs={"query": "beat_track"}),
        Action(name="execute_tool", kwargs={"server_name": "music-analysis", "tool_name": "beat_track", "params": {}}),
        Action(name="route", kwargs={"query": "mfcc"}),
        Action(name="execute_tool", kwargs={"server_name": "music-analysis", "tool_name": "mfcc", "params": {}}),
        Action(name="route", kwargs={"query": "chroma_cqt"}),
        Action(name="execute_tool", kwargs={"server_name": "music-analysis", "tool_name": "chroma_cqt", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 2: Travel | tools=4 | has GT
    Task(
        user_id="mcp_user_002",
        instruction="I'm planning a trip to the Forbidden City in Beijing, show me where to park and what's interesting to do within 1km distance?",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "find_parking_facilities"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "find_parking_facilities", "params": {}}),
        Action(name="route", kwargs={"query": "find_nearby_places"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "find_nearby_places", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 3: Leisure | tools=2 | has GT
    Task(
        user_id="mcp_user_003",
        instruction="My goal is to reach Radiant in Valorant, what should I focus on to improve and start climbing?",
        actions=[
        Action(name="route", kwargs={"query": "valorant-characters-statistics"}),
        Action(name="execute_tool", kwargs={"server_name": "opgg-mcp", "tool_name": "valorant-characters-statistics", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 4: Travel | tools=4 | has GT
    Task(
        user_id="mcp_user_004",
        instruction="There are three of us. One person is in Haidian Huangzhuang, another is at Chaoyang Joy City, and the third is at Shijingshan Hospital. Could you please recommend a fair meeting point for us, and then suggest some places for entertainment nearby?",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "suggest_meeting_point"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "suggest_meeting_point", "params": {}}),
        Action(name="route", kwargs={"query": "find_nearby_places"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "find_nearby_places", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 5: Leisure | tools=4 | has GT
    Task(
        user_id="mcp_user_005",
        instruction="Show me today's trending topics in the gaming world across all platforms.",
        actions=[
        Action(name="route", kwargs={"query": "get-bilibili-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bilibili-rank", "params": {}}),
        Action(name="route", kwargs={"query": "get-gcores-new"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-gcores-new", "params": {}}),
        Action(name="route", kwargs={"query": "get-weibo-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-weibo-trending", "params": {}}),
        Action(name="route", kwargs={"query": "get-douyin-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-douyin-trending", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 6: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_006",
        instruction="Please help me find the latest articles about 'MCP' on arXiv. Identify the potentially most influential papers among them and analyze the current trends in this field.",
        actions=[
        Action(name="route", kwargs={"query": "search_papers"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "search_papers", "params": {}}),
        Action(name="route", kwargs={"query": "get_paper_data"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "get_paper_data", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 7: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_007",
        instruction="Run a full reconnaissance on www.baidu.com. Give me a markdown report on /root/markdown/baidu_report.md with whois information and sitemap.",
        actions=[
        Action(name="route", kwargs={"query": "whois_domain"}),
        Action(name="execute_tool", kwargs={"server_name": "whois", "tool_name": "whois_domain", "params": {}}),
        Action(name="route", kwargs={"query": "get_sitemap_tree"}),
        Action(name="execute_tool", kwargs={"server_name": "sitemap", "tool_name": "get_sitemap_tree", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 8: Travel | tools=4 | has GT
    Task(
        user_id="mcp_user_008",
        instruction="I'm driving an EV with a 300km range from Beijing to Chengdu. Can you map out a route with all the charging stations I'll need?",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "get_route_directions"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "get_route_directions", "params": {}}),
        Action(name="route", kwargs={"query": "find_ev_charging_stations"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "find_ev_charging_stations", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 9: Finance | tools=5 | has GT
    Task(
        user_id="mcp_user_009",
        instruction="Analyze Apple's stock for the past year and summarize it in a PPT in /root/ppt/apple.pptx.",
        actions=[
        Action(name="route", kwargs={"query": "get_historical_stock_prices"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_historical_stock_prices", "params": {}}),
        Action(name="route", kwargs={"query": "get_news"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_news", "params": {}}),
        Action(name="route", kwargs={"query": "get_recommendations"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_recommendations", "params": {}}),
        Action(name="route", kwargs={"query": "create_presentation"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "create_presentation", "params": {}}),
        Action(name="route", kwargs={"query": "save_presentation"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "save_presentation", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 10: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_010",
        instruction="Generate a research summary for NCT04280705 and save it as Markdown to /root/markdown/NCT04280705.md.",
        actions=[
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 11: Travel | tools=3 | has GT
    Task(
        user_id="mcp_user_011",
        instruction="Help me check the high-speed train tickets from Beijing to Shanghai on next Wednesday.",
        actions=[
        Action(name="route", kwargs={"query": "get_current_time"}),
        Action(name="execute_tool", kwargs={"server_name": "time", "tool_name": "get_current_time", "params": {}}),
        Action(name="route", kwargs={"query": "get-station-code-of-citys"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-station-code-of-citys", "params": {}}),
        Action(name="route", kwargs={"query": "get-tickets"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-tickets", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 12: Leisure | tools=1 | has GT
    Task(
        user_id="mcp_user_012",
        instruction="What are the 八字 of a boy born on August 8, 2008 at 11:00 am?",
        actions=[
        Action(name="route", kwargs={"query": "getBaziDetail"}),
        Action(name="execute_tool", kwargs={"server_name": "Bazi", "tool_name": "getBaziDetail", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 13: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_013",
        instruction="Find today's LeetCode Daily Challenge and generate a detailed markdown document in /root/markdown/leetcode_daily.md that provides a comprehensive walkthrough of the problem.",
        actions=[
        Action(name="route", kwargs={"query": "get-daily-challenge"}),
        Action(name="execute_tool", kwargs={"server_name": "coin-flip", "tool_name": "get-daily-challenge", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 14: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_014",
        instruction="Help me write a quick start tutorial for Ant Design in markdown at /root/markdown/antd_tutorial.md.",
        actions=[
        Action(name="route", kwargs={"query": "list-components"}),
        Action(name="execute_tool", kwargs={"server_name": "Ant Design Components", "tool_name": "list-components", "params": {}}),
        Action(name="route", kwargs={"query": "list-component-examples"}),
        Action(name="execute_tool", kwargs={"server_name": "Ant Design Components", "tool_name": "list-component-examples", "params": {}}),
        Action(name="route", kwargs={"query": "get-component-docs"}),
        Action(name="execute_tool", kwargs={"server_name": "Ant Design Components", "tool_name": "get-component-docs", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 15: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_015",
        instruction="Read the sales data under /root/excel/Local_Electronic_Sales.xlsx, plot it as a bar chart by month and save it in /root/figs/sale.png",
        actions=[
        Action(name="route", kwargs={"query": "excel_read_sheet"}),
        Action(name="execute_tool", kwargs={"server_name": "excel", "tool_name": "excel_read_sheet", "params": {}}),
        Action(name="route", kwargs={"query": "generate_bar_chart"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-server-chart", "tool_name": "generate_bar_chart", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 16: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_016",
        instruction="Find the trending GitHub repositories. For the top one, read its Deepwiki. Then, draft a Markdown intro document for it in /root/markdown/github_trends.md.",
        actions=[
        Action(name="route", kwargs={"query": "get_github_trending_repositories"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-github-trending", "tool_name": "get_github_trending_repositories", "params": {}}),
        Action(name="route", kwargs={"query": "deepwiki_fetch"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-deepwiki", "tool_name": "deepwiki_fetch", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 17: Office | tools=1 | has GT
    Task(
        user_id="mcp_user_017",
        instruction="Draw a flowchart of a fast sorting algorithm using Mermaid.",
        actions=[
        Action(name="route", kwargs={"query": "validateMermaid"}),
        Action(name="execute_tool", kwargs={"server_name": "mermaid-validator", "tool_name": "validateMermaid", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 18: Finance | tools=2 | has GT
    Task(
        user_id="mcp_user_018",
        instruction="Generate a deep report of bitcoin and save it in /root/markdown/bitcoin.md",
        actions=[
        Action(name="route", kwargs={"query": "research-with-keywords"}),
        Action(name="execute_tool", kwargs={"server_name": "web3-research-mcp", "tool_name": "research-with-keywords", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 19: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_019",
        instruction="Help me find Mr. Lu Yaojie's resume in the Chinese Information Processing Laboratory of the Institute of Software and save it to /root/markdown/cv.md.",
        actions=[
        Action(name="route", kwargs={"query": "fetch"}),
        Action(name="execute_tool", kwargs={"server_name": "fetch", "tool_name": "fetch", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 20: Lifestyle | tools=4 | has GT
    Task(
        user_id="mcp_user_020",
        instruction="Find today's top LLM-related news.",
        actions=[
        Action(name="route", kwargs={"query": "getStories"}),
        Action(name="execute_tool", kwargs={"server_name": "hackernews", "tool_name": "getStories", "params": {}}),
        Action(name="route", kwargs={"query": "get-36kr-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-36kr-trending", "params": {}}),
        Action(name="route", kwargs={"query": "get-bbc-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bbc-news", "params": {}}),
        Action(name="route", kwargs={"query": "get-theverge-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-theverge-news", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 21: Shopping | tools=2 | has GT
    Task(
        user_id="mcp_user_021",
        instruction="Help me recommend any cheap goodies worth buying recently? Save this information to /root/excel/goods.xlsx.",
        actions=[
        Action(name="route", kwargs={"query": "get-smzdm-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-smzdm-rank", "params": {}}),
        Action(name="route", kwargs={"query": "excel_write_to_sheet"}),
        Action(name="execute_tool", kwargs={"server_name": "excel", "tool_name": "excel_write_to_sheet", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 22: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_022",
        instruction="Get deepwiki for vercel/ai and convert its structure to mindmap",
        actions=[
        Action(name="route", kwargs={"query": "deepwiki_fetch"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-deepwiki", "tool_name": "deepwiki_fetch", "params": {}}),
        Action(name="route", kwargs={"query": "convert_markdown_to_mindmap"}),
        Action(name="execute_tool", kwargs={"server_name": "mindmap", "tool_name": "convert_markdown_to_mindmap", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 23: Leisure | tools=3 | has GT
    Task(
        user_id="mcp_user_023",
        instruction="draw cowboy using canvas",
        actions=[
        Action(name="route", kwargs={"query": "drawing_generateCanvas"}),
        Action(name="execute_tool", kwargs={"server_name": "painter", "tool_name": "drawing_generateCanvas", "params": {}}),
        Action(name="route", kwargs={"query": "drawing_fillRectangle"}),
        Action(name="execute_tool", kwargs={"server_name": "painter", "tool_name": "drawing_fillRectangle", "params": {}}),
        Action(name="route", kwargs={"query": "drawing_getCanvasPng"}),
        Action(name="execute_tool", kwargs={"server_name": "painter", "tool_name": "drawing_getCanvasPng", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 24: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_024",
        instruction="Help me make a STEINS;GATE introduction PPT and help me save it to /root/ppt/STEINS_GATE.pptx.",
        actions=[
        Action(name="route", kwargs={"query": "create_presentation"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "create_presentation", "params": {}}),
        Action(name="route", kwargs={"query": "add_slide"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "add_slide", "params": {}}),
        Action(name="route", kwargs={"query": "save_presentation"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "save_presentation", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 25: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_025",
        instruction="Read the data under /root/excel/people_data.xlsx and tell me Sophia Moore's bmi.",
        actions=[
        Action(name="route", kwargs={"query": "excel_read_sheet"}),
        Action(name="execute_tool", kwargs={"server_name": "excel", "tool_name": "excel_read_sheet", "params": {}}),
        Action(name="route", kwargs={"query": "calculate"}),
        Action(name="execute_tool", kwargs={"server_name": "calculator", "tool_name": "calculate", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 26: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_026",
        instruction="Introduce me to the article on arxiv 2203.12277",
        actions=[
        Action(name="route", kwargs={"query": "get_paper_data"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "get_paper_data", "params": {}}),
        Action(name="route", kwargs={"query": "fetch"}),
        Action(name="execute_tool", kwargs={"server_name": "fetch", "tool_name": "fetch", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 27: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_027",
        instruction="What are the emerging treatment strategies for head and neck cancer, write the report to /root/markdown/cancer.md?",
        actions=[
        Action(name="route", kwargs={"query": "article_searcher"}),
        Action(name="execute_tool", kwargs={"server_name": "biomcp", "tool_name": "article_searcher", "params": {}}),
        Action(name="route", kwargs={"query": "trial_searcher"}),
        Action(name="execute_tool", kwargs={"server_name": "biomcp", "tool_name": "trial_searcher", "params": {}}),
        Action(name="route", kwargs={"query": "variant_searcher"}),
        Action(name="execute_tool", kwargs={"server_name": "biomcp", "tool_name": "variant_searcher", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 28: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_028",
        instruction="Extract the key points of this TED talk in https://www.youtube.com/watch?v=arj7oStGLkU, organize them into a mind map, and tell me what the main content of the lecture is.",
        actions=[
        Action(name="route", kwargs={"query": "get_transcript"}),
        Action(name="execute_tool", kwargs={"server_name": "youtube-transcript", "tool_name": "get_transcript", "params": {}}),
        Action(name="route", kwargs={"query": "convert_markdown_to_mindmap"}),
        Action(name="execute_tool", kwargs={"server_name": "mindmap", "tool_name": "convert_markdown_to_mindmap", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 29: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_029",
        instruction="Make a web page about the history of AI based on Wikipedia saved at /root/html/ai.html.",
        actions=[
        Action(name="route", kwargs={"query": "summarize_article_for_query"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "summarize_article_for_query", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 30: Travel | tools=7 | has GT
    Task(
        user_id="mcp_user_030",
        instruction="Help me arrange a three-day trip from Beijing to Tianjin tomorrow, round-trip by rail, give me a detailed timetable and include an approximate total budget.",
        actions=[
        Action(name="route", kwargs={"query": "get-current-date"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-current-date", "params": {}}),
        Action(name="route", kwargs={"query": "get-station-code-of-citys"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-station-code-of-citys", "params": {}}),
        Action(name="route", kwargs={"query": "get-tickets"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-tickets", "params": {}}),
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "find_nearby_places"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "find_nearby_places", "params": {}}),
        Action(name="route", kwargs={"query": "get_route_directions"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "get_route_directions", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 31: Finance | tools=3 | has GT
    Task(
        user_id="mcp_user_031",
        instruction="Analyze the last 24h of BTC and remind me if there is anything I need to pay special attention to",
        actions=[
        Action(name="route", kwargs={"query": "get_current_time"}),
        Action(name="execute_tool", kwargs={"server_name": "time", "tool_name": "get_current_time", "params": {}}),
        Action(name="route", kwargs={"query": "get-crypto-price"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-crypto-price", "tool_name": "get-crypto-price", "params": {}}),
        Action(name="route", kwargs={"query": "get-market-analysis"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-crypto-price", "tool_name": "get-market-analysis", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 32: Shopping | tools=1 | has GT
    Task(
        user_id="mcp_user_032",
        instruction="There are three people eating in the house this week, I'm allergic to shrimp and my son doesn't eat scallions, so please help me recommend a meal plan and a rough shopping list for next week.",
        actions=[
        Action(name="route", kwargs={"query": "mcp_howtocook_recommendMeals"}),
        Action(name="execute_tool", kwargs={"server_name": "howtocook-mcp", "tool_name": "mcp_howtocook_recommendMeals", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 33: Shopping | tools=2 | has GT
    Task(
        user_id="mcp_user_033",
        instruction="Recommend me a combination of dishes for a potluck dinner for three people and then tell me what ingredients I need to prepare in total and how each dish should be prepared",
        actions=[
        Action(name="route", kwargs={"query": "mcp_howtocook_whatToEat"}),
        Action(name="execute_tool", kwargs={"server_name": "howtocook-mcp", "tool_name": "mcp_howtocook_whatToEat", "params": {}}),
        Action(name="route", kwargs={"query": "mcp_howtocook_getRecipeById"}),
        Action(name="execute_tool", kwargs={"server_name": "howtocook-mcp", "tool_name": "mcp_howtocook_getRecipeById", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 34: Travel | tools=2 | has GT
    Task(
        user_id="mcp_user_034",
        instruction="Help me find homestays in Paris, France, I want to stay tomorrow, about 3 days, one adult.",
        actions=[
        Action(name="route", kwargs={"query": "get_current_time"}),
        Action(name="execute_tool", kwargs={"server_name": "time", "tool_name": "get_current_time", "params": {}}),
        Action(name="route", kwargs={"query": "airbnb_search"}),
        Action(name="execute_tool", kwargs={"server_name": "airbnb", "tool_name": "airbnb_search", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 35: Leisure | tools=2 | has GT
    Task(
        user_id="mcp_user_035",
        instruction="I play mid lane in League of Legends and want to improve. Provide champion recommendations with optimal item builds, runes, and summoner spells.",
        actions=[
        Action(name="route", kwargs={"query": "lol-champion-positions-data"}),
        Action(name="execute_tool", kwargs={"server_name": "opgg-mcp", "tool_name": "lol-champion-positions-data", "params": {}}),
        Action(name="route", kwargs={"query": "lol-champion-analysis"}),
        Action(name="execute_tool", kwargs={"server_name": "opgg-mcp", "tool_name": "lol-champion-analysis", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 36: Leisure | tools=2 | has GT
    Task(
        user_id="mcp_user_036",
        instruction="find the painting \"Corridor in the Asylum\" and give me some background information,",
        actions=[
        Action(name="route", kwargs={"query": "search-museum-objects"}),
        Action(name="execute_tool", kwargs={"server_name": "met-museum", "tool_name": "search-museum-objects", "params": {}}),
        Action(name="route", kwargs={"query": "get-museum-object"}),
        Action(name="execute_tool", kwargs={"server_name": "met-museum", "tool_name": "get-museum-object", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 37: Shopping | tools=5 | has GT
    Task(
        user_id="mcp_user_037",
        instruction="Find the latest standard iphone prices at amazon.",
        actions=[
        Action(name="route", kwargs={"query": "playwright_navigate"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_navigate", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_screenshot"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_screenshot", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_get_visible_html"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_get_visible_html", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_fill"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_fill", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_click"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_click", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 38: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_038",
        instruction="Read the paper in /root/pdf/WebArena.pdf, and find the latest papers in this area",
        actions=[
        Action(name="route", kwargs={"query": "document_reader"}),
        Action(name="execute_tool", kwargs={"server_name": "searxng", "tool_name": "document_reader", "params": {}}),
        Action(name="route", kwargs={"query": "search_papers"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "search_papers", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 39: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_039",
        instruction="Read the paper webarena, mind2web and mind2web2, then create a Comparison Report in /root/markdown/compare_webagent.md",
        actions=[
        Action(name="route", kwargs={"query": "search_papers"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "search_papers", "params": {}}),
        Action(name="route", kwargs={"query": "get_paper_data"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "get_paper_data", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 40: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_040",
        instruction="Generate a presentation on the latest Apple product information. Save it to /root/ppt/apple_news.pptx.",
        actions=[
        Action(name="route", kwargs={"query": "get-9to5mac-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-9to5mac-news", "params": {}}),
        Action(name="route", kwargs={"query": "create_presentation"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "create_presentation", "params": {}}),
        Action(name="route", kwargs={"query": "add_slide"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "add_slide", "params": {}}),
        Action(name="route", kwargs={"query": "save_presentation"}),
        Action(name="execute_tool", kwargs={"server_name": "ppt", "tool_name": "save_presentation", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 41: Finance | tools=6 | has GT
    Task(
        user_id="mcp_user_041",
        instruction="I need a daily financial brief. Fetch today's economic news, cross-reference it with relevant stock movements, and then generate a report at /root/markdown/daily_fin.md.",
        actions=[
        Action(name="route", kwargs={"query": "get-36kr-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-36kr-trending", "params": {}}),
        Action(name="route", kwargs={"query": "get-netease-news-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-netease-news-trending", "params": {}}),
        Action(name="route", kwargs={"query": "get-nytimes-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-nytimes-news", "params": {}}),
        Action(name="route", kwargs={"query": "get_news"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_news", "params": {}}),
        Action(name="route", kwargs={"query": "get_current_stock_price"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_current_stock_price", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 42: Finance | tools=2 | has GT
    Task(
        user_id="mcp_user_042",
        instruction="I have 9.5g gold, please estimate its value based on the current price of gold",
        actions=[
        Action(name="route", kwargs={"query": "get_asset_price"}),
        Action(name="execute_tool", kwargs={"server_name": "Asset_Price_MCP", "tool_name": "get_asset_price", "params": {}}),
        Action(name="route", kwargs={"query": "calculate"}),
        Action(name="execute_tool", kwargs={"server_name": "calculator", "tool_name": "calculate", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 43: Leisure | tools=2 | has GT
    Task(
        user_id="mcp_user_043",
        instruction="What is the current effect text of 'Sky Striker Ace = Zero', and what are its ATK and DEF? Show me the picture.",
        actions=[
        Action(name="route", kwargs={"query": "search_cards"}),
        Action(name="execute_tool", kwargs={"server_name": "ygocdb", "tool_name": "search_cards", "params": {}}),
        Action(name="route", kwargs={"query": "get_card_image"}),
        Action(name="execute_tool", kwargs={"server_name": "ygocdb", "tool_name": "get_card_image", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 44: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_044",
        instruction="Create a Next.js middleware that checks for a valid JWT in cookies and redirects unauthenticated users to `/login` in /root/code/middleware.ts. use context7",
        actions=[
        Action(name="route", kwargs={"query": "resolve-library-id"}),
        Action(name="execute_tool", kwargs={"server_name": "Context7", "tool_name": "resolve-library-id", "params": {}}),
        Action(name="route", kwargs={"query": "get-library-docs"}),
        Action(name="execute_tool", kwargs={"server_name": "Context7", "tool_name": "get-library-docs", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 45: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_045",
        instruction="Download New York's Air Quality report from Government Data, saved at /root/csv/NY_AIR_QUALITY.csv",
        actions=[
        Action(name="route", kwargs={"query": "package_search"}),
        Action(name="execute_tool", kwargs={"server_name": "datagov", "tool_name": "package_search", "params": {}}),
        Action(name="route", kwargs={"query": "package_show"}),
        Action(name="execute_tool", kwargs={"server_name": "datagov", "tool_name": "package_show", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 46: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_046",
        instruction="Analyze the visual marketing strategy from the iPhone 16 page at https://www.apple.com/iphone-16/ and save the summary as a Markdown report to /root/markdown/iphone16_visual_strategy.md",
        actions=[
        Action(name="route", kwargs={"query": "fetch"}),
        Action(name="execute_tool", kwargs={"server_name": "fetch", "tool_name": "fetch", "params": {}}),
        Action(name="route", kwargs={"query": "extract_image_from_url"}),
        Action(name="execute_tool", kwargs={"server_name": "image-extractor", "tool_name": "extract_image_from_url", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 47: Office | tools=1 | has GT
    Task(
        user_id="mcp_user_047",
        instruction="Get line 10 of /root/txt/Android.txt, please note that this file is very large",
        actions=[
        Action(name="route", kwargs={"query": "get_text_file_contents"}),
        Action(name="execute_tool", kwargs={"server_name": "text-editor", "tool_name": "get_text_file_contents", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 48: Office | tools=1 | no GT
    Task(
        user_id="mcp_user_048",
        instruction="I'm looking at a PR and need to know if these libs are outdated. com.fasterxml.jackson.core:jackson-databind:2.13.4, org.apache.poi:poi-ooxml:5.2.0, and com.google.guava:guava:30.1-jre. What are the latest versions for each?",
        actions=[],
        outputs=[],
    ),
    # Task 49: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_049",
        instruction="Analyze and compare echarts-for-react, react-chartjs-2, and Tremor. It's for a FinTech app, so my top priorities are a deep security scan of all dependencies and performance, especially bundle size. Give me a comparison table and a final recommendation in a markdown report in /root/markdown/package_compare.md.",
        actions=[
        Action(name="route", kwargs={"query": "npmDeps"}),
        Action(name="execute_tool", kwargs={"server_name": "npm-sentinel-mcp", "tool_name": "npmDeps", "params": {}}),
        Action(name="route", kwargs={"query": "npmSize"}),
        Action(name="execute_tool", kwargs={"server_name": "npm-sentinel-mcp", "tool_name": "npmSize", "params": {}}),
        Action(name="route", kwargs={"query": "npmCompare"}),
        Action(name="execute_tool", kwargs={"server_name": "npm-sentinel-mcp", "tool_name": "npmCompare", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 50: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_050",
        instruction="Read all the articles in the /root/pdf/embodied_ai_papers directory. Compare their similarities and differences, then write a report summarizing your analysis. Save the final report as a Markdown file at /root/markdown/embodied_ai_report.md.",
        actions=[
        Action(name="route", kwargs={"query": "list_directory"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "list_directory", "params": {}}),
        Action(name="route", kwargs={"query": "read_pdf"}),
        Action(name="execute_tool", kwargs={"server_name": "pdf-reader-mcp", "tool_name": "read_pdf", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 51: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_051",
        instruction="I need a Word document summarizing NIO. Please title it 'NIO Company Overview' and include three headed sections: a brief introduction from Wikipedia, three major news updates from the last quarter as bullet points, and a list of their main vehicle models. Finally, save it in /root/word/nio.docx",
        actions=[
        Action(name="route", kwargs={"query": "search_wikipedia"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "search_wikipedia", "params": {}}),
        Action(name="route", kwargs={"query": "get-36kr-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-36kr-trending", "params": {}}),
        Action(name="route", kwargs={"query": "create_document"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "create_document", "params": {}}),
        Action(name="route", kwargs={"query": "add_paragraph"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_paragraph", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 52: Finance | tools=4 | has GT
    Task(
        user_id="mcp_user_052",
        instruction="How are Samsung Electronics and SK Hynix doing today? I need their current stock prices, the daily percentage change for each, and can you also calculate their current market capitalization?",
        actions=[
        Action(name="route", kwargs={"query": "get_current_time"}),
        Action(name="execute_tool", kwargs={"server_name": "time", "tool_name": "get_current_time", "params": {}}),
        Action(name="route", kwargs={"query": "get_stock_ohlcv"}),
        Action(name="execute_tool", kwargs={"server_name": "kospi-kosdaq", "tool_name": "get_stock_ohlcv", "params": {}}),
        Action(name="route", kwargs={"query": "get_stock_market_cap"}),
        Action(name="execute_tool", kwargs={"server_name": "kospi-kosdaq", "tool_name": "get_stock_market_cap", "params": {}}),
        Action(name="route", kwargs={"query": "calculate"}),
        Action(name="execute_tool", kwargs={"server_name": "calculator", "tool_name": "calculate", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 53: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_053",
        instruction="Tell me about the repository details in the /root/git directory",
        actions=[
        Action(name="route", kwargs={"query": "git_status"}),
        Action(name="execute_tool", kwargs={"server_name": "git", "tool_name": "git_status", "params": {}}),
        Action(name="route", kwargs={"query": "git_log"}),
        Action(name="execute_tool", kwargs={"server_name": "git", "tool_name": "git_log", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 54: Leisure | tools=2 | has GT
    Task(
        user_id="mcp_user_054",
        instruction="I just pulled Jiyan and want to build a team around him as my main DPS. Can you recommend a good starter team for me? I need a sub-DPS/buffer and a healer/survivor. Also, what's his best Echo set and main Echo, and please explain why.",
        actions=[
        Action(name="route", kwargs={"query": "get_character_info"}),
        Action(name="execute_tool", kwargs={"server_name": "wuwa-mcp", "tool_name": "get_character_info", "params": {}}),
        Action(name="route", kwargs={"query": "get_artifact_info"}),
        Action(name="execute_tool", kwargs={"server_name": "wuwa-mcp", "tool_name": "get_artifact_info", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 55: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_055",
        instruction="I'm using shadcn/ui to build a 'create post' page. I have two input fields, one for the title and one for the content. I want the 'Publish' button at the bottom to be disabled if either the title or content is empty. It should only become clickable when both fields are filled. How can I achieve this? Please provide a complete React/TypeScript example using the Input and Button components from shadcn/ui and save the code to /root/code/shadcn_ui.ts",
        actions=[
        Action(name="route", kwargs={"query": "search_components"}),
        Action(name="execute_tool", kwargs={"server_name": "shadcn-ui-server", "tool_name": "search_components", "params": {}}),
        Action(name="route", kwargs={"query": "get_component_details"}),
        Action(name="execute_tool", kwargs={"server_name": "shadcn-ui-server", "tool_name": "get_component_details", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 56: Leisure | tools=4 | has GT
    Task(
        user_id="mcp_user_056",
        instruction="Generate a well-formatted PDF report  in /root/pdf/douban_report.pdf, summarizing current douban trends.",
        actions=[
        Action(name="route", kwargs={"query": "get-douban-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-douban-rank", "params": {}}),
        Action(name="route", kwargs={"query": "create_document"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "create_document", "params": {}}),
        Action(name="route", kwargs={"query": "add_paragraph"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_paragraph", "params": {}}),
        Action(name="route", kwargs={"query": "convert_to_pdf"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "convert_to_pdf", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 57: Shopping | tools=2 | has GT
    Task(
        user_id="mcp_user_057",
        instruction="Help me recommend some consumer electronics that are worth buying these days.",
        actions=[
        Action(name="route", kwargs={"query": "get-ifanr-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-ifanr-news", "params": {}}),
        Action(name="route", kwargs={"query": "get-smzdm-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-smzdm-rank", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 58: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_058",
        instruction="Find the latest research paper in the web agents. Identify the best one, read the full text, and then tell me its main motivation, the methodology it employs, and its key results.",
        actions=[
        Action(name="route", kwargs={"query": "search_papers"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-simple-arxiv", "tool_name": "search_papers", "params": {}}),
        Action(name="route", kwargs={"query": "download_paper"}),
        Action(name="execute_tool", kwargs={"server_name": "arxiv-mcp-server", "tool_name": "download_paper", "params": {}}),
        Action(name="route", kwargs={"query": "read_paper"}),
        Action(name="execute_tool", kwargs={"server_name": "arxiv-mcp-server", "tool_name": "read_paper", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 59: Shopping | tools=5 | has GT
    Task(
        user_id="mcp_user_059",
        instruction="Recommend a gaming PC build for playing the latest Call of Duty, along with an approximate budget.",
        actions=[
        Action(name="route", kwargs={"query": "search_wikipedia"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "search_wikipedia", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_navigate"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_navigate", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_get_visible_html"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_get_visible_html", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_fill"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_fill", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_click"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_click", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 60: Leisure | tools=1 | has GT
    Task(
        user_id="mcp_user_060",
        instruction="What does this base64 image mean? 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",
        actions=[
        Action(name="route", kwargs={"query": "extract_image_from_base64"}),
        Action(name="execute_tool", kwargs={"server_name": "image-extractor", "tool_name": "extract_image_from_base64", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 61: Travel | tools=3 | has GT
    Task(
        user_id="mcp_user_061",
        instruction="Plan a bike route from UCAS Zhongguancun Campus to UCAS Yanqihu Campus, including an estimated travel time.",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "get_route_directions"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "get_route_directions", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 62: Leisure | tools=1 | has GT
    Task(
        user_id="mcp_user_062",
        instruction="Read the file /root/word/exchange.docx, tell me who did not give a gift",
        actions=[
        Action(name="route", kwargs={"query": "get_document_text"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "get_document_text", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 63: Office | tools=1 | has GT
    Task(
        user_id="mcp_user_063",
        instruction="Read the customer information in /root/csv/customers-100.csv and tell me Sheryl Meyers's email address",
        actions=[
        Action(name="route", kwargs={"query": "document_reader"}),
        Action(name="execute_tool", kwargs={"server_name": "searxng", "tool_name": "document_reader", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 64: Shopping | tools=2 | has GT
    Task(
        user_id="mcp_user_064",
        instruction="I have 18.9g silver, please estimate its value based on the current price",
        actions=[
        Action(name="route", kwargs={"query": "get_asset_price"}),
        Action(name="execute_tool", kwargs={"server_name": "Asset_Price_MCP", "tool_name": "get_asset_price", "params": {}}),
        Action(name="route", kwargs={"query": "calculate"}),
        Action(name="execute_tool", kwargs={"server_name": "calculator", "tool_name": "calculate", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 65: Shopping | tools=4 | has GT
    Task(
        user_id="mcp_user_065",
        instruction="Help me find the top 5 best selling gpus from amazon and tell me the links directly.",
        actions=[
        Action(name="route", kwargs={"query": "playwright_navigate"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_navigate", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_screenshot"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_screenshot", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_get_visible_html"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_get_visible_html", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_fill"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_fill", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_click"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_click", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 66: Office | tools=4 | has GT
    Task(
        user_id="mcp_user_066",
        instruction="Convert the reference list in /root/txt/paper_list.bib into a Word document. Please use APA formatting and save the final file at /root/word/paper_list.docx.",
        actions=[
        Action(name="route", kwargs={"query": "read_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "read_file", "params": {}}),
        Action(name="route", kwargs={"query": "create_document"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "create_document", "params": {}}),
        Action(name="route", kwargs={"query": "add_paragraph"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_paragraph", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 67: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_067",
        instruction="Provide a foundational overview of Convolutional Neural Networks (CNNs), referencing Wikipedia. Generate a simple CNN example as a Python script and save it to /root/code/cnn_example.py.",
        actions=[
        Action(name="route", kwargs={"query": "search_wikipedia"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "search_wikipedia", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 68: Travel | tools=2 | has GT
    Task(
        user_id="mcp_user_068",
        instruction="My office is located at Jin Mao Tower, 88 Century Avenue, Pudong New Area, Shanghai. I'm looking at a potential apartment in the Nanjing West Road area, specifically let's say near 'Nanjing West Road 2-68, Huangpu District, Shanghai'. Could you please run a detailed commute analysis for me? I need to compare three different transportation modes: driving, walking, and biking. It's crucial to get an idea of the morning rush hour, so let's set the departure time for 8:00 AM.",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "analyze_commute"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "analyze_commute", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 69: Travel | tools=2 | has GT
    Task(
        user_id="mcp_user_069",
        instruction="I'm considering relocating to New York City and need a comprehensive understanding of a potential neighborhood's livability. Please generate a detailed analysis for the area surrounding 72nd Street and 5th Avenue, Manhattan. Focus on a 1000-meter radius to assess the quality of life. I'm particularly interested in the availability of amenities, public transportation accessibility, green spaces and recreational areas, and proximity to education and healthcare facilities. The output should provide counts and proximity scores for these categories to help me evaluate the overall convenience and quality of the residential area.\"",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "analyze_neighborhood"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "analyze_neighborhood", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 70: Finance | tools=2 | has GT
    Task(
        user_id="mcp_user_070",
        instruction="I'm considering doing some initial research on a potential investment in the Korean market. Could you help me gather comprehensive data for Hyundai Motor Company.",
        actions=[
        Action(name="route", kwargs={"query": "load_all_tickers"}),
        Action(name="execute_tool", kwargs={"server_name": "kospi-kosdaq", "tool_name": "load_all_tickers", "params": {}}),
        Action(name="route", kwargs={"query": "get_stock_fundamental"}),
        Action(name="execute_tool", kwargs={"server_name": "kospi-kosdaq", "tool_name": "get_stock_fundamental", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 71: Finance | tools=3 | has GT
    Task(
        user_id="mcp_user_071",
        instruction="Help me view recent finance-related news, categorize financial news by sentiment, and extract key entities (companies, people, products) and important financial events.",
        actions=[
        Action(name="route", kwargs={"query": "get-36kr-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-36kr-trending", "params": {}}),
        Action(name="route", kwargs={"query": "get-bbc-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bbc-news", "params": {}}),
        Action(name="route", kwargs={"query": "get-nytimes-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-nytimes-news", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 72: Finance | tools=2 | has GT
    Task(
        user_id="mcp_user_072",
        instruction="Based on the current Fear & Greed Index and recent news, do you think it's a good time to take the plunge?",
        actions=[
        Action(name="route", kwargs={"query": "get_cnn_fear_greed_index"}),
        Action(name="execute_tool", kwargs={"server_name": "investor", "tool_name": "get_cnn_fear_greed_index", "params": {}}),
        Action(name="route", kwargs={"query": "get-bbc-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bbc-news", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 73: Finance | tools=2 | has GT
    Task(
        user_id="mcp_user_073",
        instruction="Any recent negative news about Bitcoin? Also, tell me how the Crypto Fear & Greed Index has changed over the past three days.",
        actions=[
        Action(name="route", kwargs={"query": "get-bbc-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bbc-news", "params": {}}),
        Action(name="route", kwargs={"query": "get_crypto_fear_greed_index"}),
        Action(name="execute_tool", kwargs={"server_name": "investor", "tool_name": "get_crypto_fear_greed_index", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 74: Travel | tools=4 | has GT
    Task(
        user_id="mcp_user_074",
        instruction="I plan to go to Shinjuku Gyoen from Tokyo Tower and then find a highly rated Japanese restaurant nearby for lunch. Give me restaurant recommendations and tell me how to get there.",
        actions=[
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "search_category"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "search_category", "params": {}}),
        Action(name="route", kwargs={"query": "get_route_directions"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "get_route_directions", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 75: Lifestyle | tools=1 | has GT
    Task(
        user_id="mcp_user_075",
        instruction="What's the weather like in Beijing in the last few days? Give me some advice on what to wear!",
        actions=[
        Action(name="route", kwargs={"query": "get_weather"}),
        Action(name="execute_tool", kwargs={"server_name": "weather", "tool_name": "get_weather", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 76: Lifestyle | tools=1 | has GT
    Task(
        user_id="mcp_user_076",
        instruction="What files are in my /root/music folder?",
        actions=[
        Action(name="route", kwargs={"query": "list_directory"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "list_directory", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 77: Lifestyle | tools=3 | has GT
    Task(
        user_id="mcp_user_077",
        instruction="Tell me what's the big news in AI today.",
        actions=[
        Action(name="route", kwargs={"query": "get-juejin-article-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-juejin-article-rank", "params": {}}),
        Action(name="route", kwargs={"query": "getStories"}),
        Action(name="execute_tool", kwargs={"server_name": "hackernews", "tool_name": "getStories", "params": {}}),
        Action(name="route", kwargs={"query": "get-infoq-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-infoq-news", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 78: Travel | tools=4 | has GT
    Task(
        user_id="mcp_user_078",
        instruction="Give me a two-day tour of Beijing based on the recent weather, and my hotel is in the Haidian District",
        actions=[
        Action(name="route", kwargs={"query": "get_weather_by_city"}),
        Action(name="execute_tool", kwargs={"server_name": "weather", "tool_name": "get_weather_by_city", "params": {}}),
        Action(name="route", kwargs={"query": "geocode_address"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "geocode_address", "params": {}}),
        Action(name="route", kwargs={"query": "find_nearby_places"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "find_nearby_places", "params": {}}),
        Action(name="route", kwargs={"query": "reverse_geocode"}),
        Action(name="execute_tool", kwargs={"server_name": "osm-mcp-server", "tool_name": "reverse_geocode", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 79: Lifestyle | tools=1 | has GT
    Task(
        user_id="mcp_user_079",
        instruction="Read the comments on hacker news story 44490510 and help me summarize the views in the comments.",
        actions=[
        Action(name="route", kwargs={"query": "getStoryWithComments"}),
        Action(name="execute_tool", kwargs={"server_name": "hackernews", "tool_name": "getStoryWithComments", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 80: Finance | tools=1 | has GT
    Task(
        user_id="mcp_user_080",
        instruction="Get today's bbc news, reserved for finance related content.",
        actions=[
        Action(name="route", kwargs={"query": "get-bbc-news"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bbc-news", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 81: Shopping | tools=3 | has GT
    Task(
        user_id="mcp_user_081",
        instruction="I want to buy a 34-inch curved monitor, please help me recommend some items with prices and links to buy.",
        actions=[
        Action(name="route", kwargs={"query": "playwright_navigate"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_navigate", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_click"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_click", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_fill"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_fill", "params": {}}),
        Action(name="route", kwargs={"query": "playwright_get_visible_html"}),
        Action(name="execute_tool", kwargs={"server_name": "playwright", "tool_name": "playwright_get_visible_html", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 82: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_082",
        instruction="Read the Wikipedia article on Llullaillaco, which briefly describes the content of this article, saved to /root/markdown/Llullaillaco.md",
        actions=[
        Action(name="route", kwargs={"query": "get_article"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "get_article", "params": {}}),
        Action(name="route", kwargs={"query": "write_file"}),
        Action(name="execute_tool", kwargs={"server_name": "filesystem", "tool_name": "write_file", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 83: Leisure | tools=1 | has GT
    Task(
        user_id="mcp_user_083",
        instruction="We have organized an online raffle with the following list of participants: [‘Alice’, ‘Bob’, ‘Charlie’, ‘David’, ‘Eve’]. Please choose one lucky winner at random from this list.",
        actions=[
        Action(name="route", kwargs={"query": "random_sample"}),
        Action(name="execute_tool", kwargs={"server_name": "random-number", "tool_name": "random_sample", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 84: Office | tools=6 | has GT
    Task(
        user_id="mcp_user_084",
        instruction="Help me create an example word that needs to have headings, tables, body, footnotes and insert clock.png under /root/picture and save it in /root/word/example.docx",
        actions=[
        Action(name="route", kwargs={"query": "create_document"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "create_document", "params": {}}),
        Action(name="route", kwargs={"query": "add_heading"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_heading", "params": {}}),
        Action(name="route", kwargs={"query": "add_table"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_table", "params": {}}),
        Action(name="route", kwargs={"query": "add_paragraph"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_paragraph", "params": {}}),
        Action(name="route", kwargs={"query": "add_footnote_to_document"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_footnote_to_document", "params": {}}),
        Action(name="route", kwargs={"query": "add_picture"}),
        Action(name="execute_tool", kwargs={"server_name": "word-document-server", "tool_name": "add_picture", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 85: Lifestyle | tools=1 | has GT
    Task(
        user_id="mcp_user_085",
        instruction="I received an email from amaz0n.com asking me to click on a link to enter my account information. Is this site official for Amazon?",
        actions=[
        Action(name="route", kwargs={"query": "whois_domain"}),
        Action(name="execute_tool", kwargs={"server_name": "whois", "tool_name": "whois_domain", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 86: Office | tools=1 | has GT
    Task(
        user_id="mcp_user_086",
        instruction="What are the changes in my log files /root/txt/log_today.txt and /root/txt/log_yesterday.txt, help me to find out all the different lines which contain 'ERROR' ?",
        actions=[
        Action(name="route", kwargs={"query": "text_diff"}),
        Action(name="execute_tool", kwargs={"server_name": "searxng", "tool_name": "text_diff", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 87: Finance | tools=2 | has GT
    Task(
        user_id="mcp_user_087",
        instruction="My after-tax income last month was 15,000 CNY, and my main expenses were 3,000 CNY for rent, 2,500 CNY for meals, 500 CNY for transportation, and 1,200 CNY for shopping. Please help me calculate what my balance was last month. And visualize these data in a pie chart. Also, please take the current exchange rate of RMB to USD and calculate how much my balance is converted to USD?",
        actions=[
        Action(name="route", kwargs={"query": "generate_pie_chart"}),
        Action(name="execute_tool", kwargs={"server_name": "mcp-server-chart", "tool_name": "generate_pie_chart", "params": {}}),
        Action(name="route", kwargs={"query": "exchange_rate"}),
        Action(name="execute_tool", kwargs={"server_name": "exchange-rate-mcp", "tool_name": "exchange_rate", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 88: Finance | tools=1 | has GT
    Task(
        user_id="mcp_user_088",
        instruction="Tell me the price of nvidia's stock right now.",
        actions=[
        Action(name="route", kwargs={"query": "get_ticker_info"}),
        Action(name="execute_tool", kwargs={"server_name": "yfmcp", "tool_name": "get_ticker_info", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 89: Office | tools=3 | has GT
    Task(
        user_id="mcp_user_089",
        instruction="I am writing a popular science article on ‘Causes of the Fall of the Roman Empire’. Please help me to list at least three main causes that are generally recognized by historians and find one authoritative reference for each. Finally, organize all this information into a structured document and save it to /root/markdown/Rome.md.",
        actions=[
        Action(name="route", kwargs={"query": "duckduckgo_web_search"}),
        Action(name="execute_tool", kwargs={"server_name": "duckduckgo-search", "tool_name": "duckduckgo_web_search", "params": {}}),
        Action(name="route", kwargs={"query": "search_wikipedia"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "search_wikipedia", "params": {}}),
        Action(name="route", kwargs={"query": "get_article"}),
        Action(name="execute_tool", kwargs={"server_name": "wikipedia", "tool_name": "get_article", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 90: Travel | tools=2 | has GT
    Task(
        user_id="mcp_user_090",
        instruction="Find the earliest available high-speed train from Beijing South to Shanghai South for tomorrow. What's the departure time and ticket price?",
        actions=[
        Action(name="route", kwargs={"query": "get-station-code-by-names"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-station-code-by-names", "params": {}}),
        Action(name="route", kwargs={"query": "get-tickets"}),
        Action(name="execute_tool", kwargs={"server_name": "12306-mcp", "tool_name": "get-tickets", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 91: Lifestyle | tools=2 | has GT
    Task(
        user_id="mcp_user_091",
        instruction="What's on the zhihu and bilibili trendings today? Help me recommend something tech related!",
        actions=[
        Action(name="route", kwargs={"query": "get-bilibili-rank"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-bilibili-rank", "params": {}}),
        Action(name="route", kwargs={"query": "get-zhihu-trending"}),
        Action(name="execute_tool", kwargs={"server_name": "trends-hub", "tool_name": "get-zhihu-trending", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 92: Leisure | tools=2 | has GT
    Task(
        user_id="mcp_user_092",
        instruction="I need you to pull up the Chinese almanac and find me the best dates to get married in the near future. Give me a list of the most auspicious Gregorian dates for a wedding in the next months.",
        actions=[
        Action(name="route", kwargs={"query": "get_current_time"}),
        Action(name="execute_tool", kwargs={"server_name": "time", "tool_name": "get_current_time", "params": {}}),
        Action(name="route", kwargs={"query": "getChineseCalendar"}),
        Action(name="execute_tool", kwargs={"server_name": "Bazi", "tool_name": "getChineseCalendar", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 93: Office | tools=2 | has GT
    Task(
        user_id="mcp_user_093",
        instruction="Convert /root/word/CV.docx and /root/word/Report_Card.docx to PDF, merge the two resulting files, and save the final combined document as /root/pdf/full_cv.pdf.",
        actions=[
        Action(name="route", kwargs={"query": "docx_to_pdf"}),
        Action(name="execute_tool", kwargs={"server_name": "searxng", "tool_name": "docx_to_pdf", "params": {}}),
        Action(name="route", kwargs={"query": "pdf_merger"}),
        Action(name="execute_tool", kwargs={"server_name": "searxng", "tool_name": "pdf_merger", "params": {}}),
        ],
        outputs=[],
    ),
    # Task 94: Finance | tools=4 | has GT
    Task(
        user_id="mcp_user_094",
        instruction="Help me do a full investment analysis on Nvidia's stock",
        actions=[
        Action(name="route", kwargs={"query": "get_stock_price_date_range"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_stock_price_date_range", "params": {}}),
        Action(name="route", kwargs={"query": "get_income_statement"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_income_statement", "params": {}}),
        Action(name="route", kwargs={"query": "get_cashflow"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_cashflow", "params": {}}),
        Action(name="route", kwargs={"query": "get_news"}),
        Action(name="execute_tool", kwargs={"server_name": "yahoo-finance", "tool_name": "get_news", "params": {}}),
        ],
        outputs=[],
    ),
]