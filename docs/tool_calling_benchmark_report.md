# Tool Calling Benchmark 数据集调研与SFT数据收集方案

---

## 一、调研背景

目标：调研以下10个数据集，评估其能否用于收集SFT训练数据，提升模型的tool calling / agent工具调用能力。

调研清单：MCP-Universe、MCPEval、MCP-Bench、Toolathlon、LiveMCPBench、CVE-Bench、BountyBench、SEC-bench、App-Bench、Design2Code

---

## 二、结论总览

| 数据集 | 与tool calling相关？ | 能收集SFT？ | 有现成数据？ | 推荐优先级 |
|--------|-------------------|-----------|-----------|----------|
| **MCP-Bench** | ✅ 直接相关 | ✅ 可以 | 🟡 有任务定义 | ⭐⭐⭐⭐⭐ |
| **LiveMCPBench** | ✅ 直接相关 | ✅ 可以 | ✅ 有95条轨迹 | ⭐⭐⭐⭐⭐ |
| **Toolathlon** | ✅ 直接相关 | ✅ 可以 | ❌ 需自己跑 | ⭐⭐⭐⭐ |
| **MCP-Universe** | ✅ 直接相关 | ✅ 可以 | 🟡 有任务定义 | ⭐⭐⭐⭐ |
| **MCPEval** | ✅ 相关 | 🟡 间接 | 🟡 评估框架 | ⭐⭐⭐ |
| **CVE-Bench** | ❌ 不相关 | ❌ | ❌ | ⭐ |
| **BountyBench** | ❌ 不相关 | ❌ | ❌ | ⭐ |
| **SEC-bench** | ❌ 不相关 | ❌ | ❌ | ⭐ |
| **App-Bench** | ❌ 不相关 | ❌ | ❌ | ⭐ |
| **Design2Code** | ❌ 不相关 | ❌ | ❌ | ⭐ |

**5个相关**的都是MCP/tool calling类benchmark，agent通过function calling调用真实工具完成任务。

**5个不相关**的原因：CVE-Bench/BountyBench/SEC-bench是安全领域代码执行（不是function calling格式）；App-Bench是全栈代码生成；Design2Code是图片转代码。

---

## 三、5个相关数据集详细分析

### 3.1 MCP-Bench

| 项目 | 内容 |
|------|------|
| 来源 | Accenture，NeurIPS 2025 Workshop |
| 论文 | https://arxiv.org/abs/2508.20453 |
| 代码 | https://github.com/Accenture/mcp-bench |
| 规模 | 28个MCP server，250个工具，104个任务 |
| 领域 | 金融、旅行、科学计算、学术搜索、生物医学、地理导航、媒体娱乐、社交情报、数学、健康、天气、占卜 |
| 环境搭建 | 需启动28个MCP server |
| 现有数据 | 有任务定义(JSON)+工具配置，MedCalcBench子集有JSONL评估输出，没有完整对话轨迹 |

**核心特点：**
- **干扰工具设计**：每个任务附带10个干扰server（100+无关工具），训练模型在噪音中选对工具
- **模糊指令**：每个任务有fuzzy版本，不提工具名，迫使模型自己推断
- **任务自动合成pipeline**：依赖链发现→质量过滤→模糊化

**数据构建方法（论文Section 4.2）：**
1. 分析所有工具的输入/输出签名，自动发现A→B的依赖链
2. LLM基于依赖链自动生成自然语言任务
3. 质量过滤：可解性≥9/10，实用性≥5/10
4. 模糊化：去掉工具名和步骤提示

**评估方法：** 规则评估（tool name正确率/schema合规率/执行成功率）+ LLM-as-Judge（5次shuffle取平均）

**模型表现：** GPT-5得分0.749，kimi-k2得分0.629（dependency awareness 0.448，parallelism 0.307是最弱项）

**示例Case：**
> 我在研究黑色素瘤BRAF V600E突变的耐药机制。需要：V600E在ClinVar中的致病性信息、过去一年关于V600E阳性黑色素瘤耐药的5篇最有影响力的论文、正在招募V600E黑色素瘤患者的2/3期临床试验、FDA数据库中vemurafenib的严重不良事件。
> *需要跨Paper Search + BioMCP两个server，调用gene_getter/variant_searcher/article_searcher/trial_searcher等十多个工具*

> 我要从Denver出发做一周的徒步露营。帮我找有好trail的国家公园，按驾车时间排序选最近的3个，做7天行程——每天告诉我天气、营地、导航和海拔。
> *需要跨Google Maps + Weather Data + National Parks三个server，11步依赖链*

---

### 3.2 LiveMCPBench

| 项目 | 内容 |
|------|------|
| 来源 | 中科院信工所，ICLR 2026提交 |
| 论文 | https://arxiv.org/abs/2508.01780 |
| 代码 | https://github.com/icip-cas/LiveMCPBench |
| Docker | `docker pull hysdhlx/livemcpbench:latest` |
| 规模 | 70个MCP server，527个工具，95个任务 |
| 领域 | 办公(31)、生活(15)、休闲(14)、金融(14)、旅行(12)、购物(9) |
| 涉及服务 | 微信读书、B站、豆瓣、12306、Yahoo Finance、地图、音乐分析、Word/PPT/PDF、Playwright、Wikipedia、arXiv、Excel等 |
| 环境搭建 | Docker + Embedding模型（可用免费API），69个server全不需要外部API key |
| 现有数据 | ✅ 有Claude-Sonnet-4的95条完整对话轨迹（但含试错噪音） |

**核心特点：**
- 目前**规模最大**的MCP工具池（527个工具）
- 论文发现"检索错误占所有失败的近一半"——在大工具池中找对工具是最大挑战
- Agent使用route+execute_tool两步模式（先检索工具再执行）

**已有轨迹格式（OpenAI function calling格式）：**
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "...", "tool_calls": [{"function": {"name": "route", "arguments": "..."}}]},
    {"role": "tool", "tool_call_id": "...", "content": "..."}
  ]
}
```

**模型表现：** Claude-Sonnet-4最高78.95%

**示例Case：**
> 生成PDF报告到/root/pdf/wechat_reading_report.pdf，总结微信读书当前热门趋势，包含词云图。
> *调用: get-weread-rank → generate_word_cloud_chart → create_document → add_paragraph → convert_to_pdf*

> 我开一辆续航300km的电动车从北京到成都，帮我规划路线并标出所有充电站。
> *调用: geocode_address → get_route_directions → find_ev_charging_stations → reverse_geocode*

> 三个人分别在海淀黄庄、朝阳大悦城、石景山医院，帮我们找个公平的碰面点，然后推荐附近娱乐场所。
> *调用: geocode_address × 3 → suggest_meeting_point → find_nearby_places → reverse_geocode*

> 分析Apple过去一年的股票走势，总结成PPT保存到/root/ppt/apple.pptx。
> *调用: get_historical_stock_prices → get_news → get_recommendations → create_presentation → save_presentation*

---

### 3.3 Toolathlon (Tool Decathlon)

| 项目 | 内容 |
|------|------|
| 来源 | 香港科技大学，ICLR 2026 |
| 论文 | https://arxiv.org/abs/2510.25726 |
| 代码 | https://github.com/hkust-nlp/Toolathlon |
| 规模 | 32个真实软件，604个工具，108个手工标注任务 |
| 领域 | Google Calendar、Notion、WooCommerce、Kubernetes、BigQuery、GitHub、Slack、Canvas、Google Sheets、Docker、Trello等 |
| 环境搭建 | 需搭建32个真实软件系统（成本高） |
| 现有数据 | 有任务定义和工具代码，没有轨迹 |

**核心特点：**
- 平均每个任务需要**20轮tool calling**（所有benchmark中最长）
- 108个任务**全部手工标注**（质量最高）
- 提供**真实的软件初始状态**（Canvas课程有几十个学生、Google Sheet有真实数据）

**模型表现：** Claude-4.5-Sonnet仅38.6%

**示例Case：**
> 管理Google Calendar和Notion联动，把日历上的会议自动同步到Notion数据库中，并给与会者发Slack消息。
> *需要跨3个App，约20轮tool calling*

> 在WooCommerce上处理客户退货请求，更新库存数量，修改订单状态，并发送确认邮件。

> 查询BigQuery中的销售数据异常，生成分析报告，通过Slack通知相关团队。

---

### 3.4 MCP-Universe

| 项目 | 内容 |
|------|------|
| 来源 | Salesforce AI Research，NeurIPS 2025 |
| 论文 | https://arxiv.org/abs/2508.14704 |
| 代码 | https://github.com/SalesforceAIResearch/MCP-Universe |
| 规模 | 11个MCP server，231个任务 |
| 领域 | 导航(45)、搜索(55)、浏览器自动化(39)、金融分析(40)、代码仓库管理(33)、3D设计(19) |
| 环境搭建 | 需要Google Maps等外部API key |
| 现有数据 | 有任务定义+evaluator配置，没有轨迹 |

**核心特点：**
- 首个综合MCP benchmark
- 3种evaluator：格式检查、静态检查、动态检查（实时获取ground truth）
- 论文识别3大挑战：long-context overflow、unknown-tools、cross-domain variance

**模型表现：** GPT-5仅43.72%

**示例Case：**
> 从Johor Bahru到Kuala Lumpur的自驾路线规划，经过4个城市，给出3条不同路线、估算时间和沿途风景点。
> *调用: Google Maps的geocode/distance_matrix/directions等API*

---

### 3.5 MCPEval

| 项目 | 内容 |
|------|------|
| 来源 | Salesforce AI Research，EMNLP 2025 |
| 论文 | https://aclanthology.org/2025.emnlp-demos.27/ |
| 代码 | https://github.com/SalesforceAIResearch/MCPEval |
| 规模 | 5个MCP server |
| 领域 | 金融(yfinance)、数据库(sqlite)、旅行助手、体育数据、编剧写作 |

**核心定位：** 评估框架，不是数据集。可以自动生成评估任务。适合用来评估训练后的模型，不是收集SFT数据的主要来源。

---

## 四、5个不相关数据集简要说明

| 数据集 | 是什么 | 为什么不相关 |
|--------|-------|------------|
| **CVE-Bench** | 40个CVE漏洞利用任务 | agent写攻击代码在Docker沙盒执行，不是function calling |
| **BountyBench** | 25个系统的bug bounty | Kali Linux终端命令操作，不是function calling |
| **SEC-bench** | 自动化安全benchmark | 代码agent（PoC生成+修补），非function calling格式 |
| **App-Bench** | AI生成完整Web应用 | 代码生成评估，不涉及tool calling |
| **Design2Code** | 484个网页截图转代码 | 多模态代码生成，与tool calling无关 |

*注：CVE-Bench/BountyBench/SEC-bench如果后续做安全/coding agent可以关注，当前不是tool calling优先级。*

---

## 五、SFT数据收集方案

### 推荐执行顺序

| 优先级 | 数据集 | 行动 | 预计产出 | 搭建成本 |
|-------|--------|------|---------|---------|
| **P0** | LiveMCPBench | Docker环境+Embedding API | 95条真实MCP轨迹 | 中（Docker+Embedding） |
| **P1** | MCP-Bench | 搭建28个MCP server | 104条（含干扰工具）| 中高 |
| **P2** | MCP-Universe | 配置外部API key | 231条轨迹 | 中（需API key） |
| **P3** | Toolathlon | 搭建32个软件系统 | 108条20轮长链轨迹 | 高 |
| **P4** | MCPEval | pip install | 用于评估 | 低 |

### 数据格式

所有收集的轨迹统一转换为OpenAI SFT格式：
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "任务指令"},
    {"role": "assistant", "reasoning_content": "思考过程", "tool_calls": [{"function": {"name": "tool_name", "arguments": "{...}"}}]},
    {"role": "tool", "tool_call_id": "...", "content": "工具返回的真实数据"},
    ...
  ],
  "tools": [工具定义列表]
}
```

### 当前已有能力覆盖 vs 缺失

| 能力 | 已覆盖 | 缺失 |
|------|-------|------|
| 基础tool calling | ✅ | |
| 多步骤链式调用 | ✅ | |
| 跨App协作 | ✅ | |
| 大工具池选择（100+工具中选对） | | ❌ MCP-Bench/LiveMCPBench可补 |
| 模糊指令理解 | | ❌ MCP-Bench可补 |
| 干扰工具过滤 | | ❌ MCP-Bench可补 |
| 并行工具调用 | | ❌ 需专门构造 |
| 长horizon（20+步） | | ❌ Toolathlon可补 |
| 错误恢复 | | ❌ 需专门构造 |

---

## 六、所有链接汇总

| 数据集 | 论文 | GitHub | 其他 |
|--------|------|--------|------|
| MCP-Bench | [arXiv:2508.20453](https://arxiv.org/abs/2508.20453) | [Accenture/mcp-bench](https://github.com/Accenture/mcp-bench) | |
| LiveMCPBench | [arXiv:2508.01780](https://arxiv.org/abs/2508.01780) | [icip-cas/LiveMCPBench](https://github.com/icip-cas/LiveMCPBench) | [Docker](https://hub.docker.com/r/hysdhlx/livemcpbench) |
| Toolathlon | [arXiv:2510.25726](https://arxiv.org/abs/2510.25726) | [hkust-nlp/Toolathlon](https://github.com/hkust-nlp/Toolathlon) | [主页](https://toolathlon.xyz/) |
| MCP-Universe | [arXiv:2508.14704](https://arxiv.org/abs/2508.14704) | [SalesforceAIResearch/MCP-Universe](https://github.com/SalesforceAIResearch/MCP-Universe) | [文档](https://mcp-universe.github.io/) |
| MCPEval | [EMNLP 2025](https://aclanthology.org/2025.emnlp-demos.27/) | [SalesforceAIResearch/MCPEval](https://github.com/SalesforceAIResearch/MCPEval) | |
| CVE-Bench | [arXiv:2503.17332](https://arxiv.org/abs/2503.17332) | [uiuc-kang-lab/cve-bench](https://github.com/uiuc-kang-lab/cve-bench) | |
| BountyBench | [arXiv:2505.15216](https://arxiv.org/abs/2505.15216) | [bountybench.github.io](http://bountybench.github.io/) | [Stanford Blog](https://ai.stanford.edu/blog/bountybench/) |
| SEC-bench | [arXiv:2506.11791](https://arxiv.org/abs/2506.11791) | | |
| App-Bench | | | [appbench.ai](https://appbench.ai/) |
| Design2Code | [arXiv:2403.03163](https://arxiv.org/abs/2403.03163) | [NoviScl/Design2Code](https://github.com/NoviScl/Design2Code) | |
