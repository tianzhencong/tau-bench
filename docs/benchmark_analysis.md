# Tool Calling Benchmark 数据集深度分析报告

> 生成日期: 2024-02-28
> 目的: 分析老板列出的10个数据集，判断哪些对优化model tool_calling能力有实际价值
> 方法: 逐个clone repo + 下载论文 + 查看实际数据格式

---

## 一、总览评级

| 数据集 | 对tool_calling价值 | 有可用SFT数据？ | 工具数 | 任务数 | 论文 |
|--------|-------------------|---------------|-------|-------|------|
| **LiveMCPBench** | ⭐⭐⭐⭐⭐ | ✅ 完整对话轨迹 | 527 | 95 | [arXiv:2508.01780](https://arxiv.org/abs/2508.01780) |
| **MCP-Bench** | ⭐⭐⭐⭐⭐ | ✅ JSONL轨迹 | 250 | 104 | [arXiv:2508.20453](https://arxiv.org/abs/2508.20453) |
| **Toolathlon** | ⭐⭐⭐⭐⭐ | 需自己跑 | 604 | 108 | [arXiv:2510.25726](https://arxiv.org/abs/2510.25726) |
| **MCP-Universe** | ⭐⭐⭐⭐ | ⚠️ 仅元数据 | 11 servers | 231 | [arXiv:2508.14704](https://arxiv.org/abs/2508.14704) |
| **MCPEval** | ⭐⭐⭐ | ⚠️ 仅评估指标 | 多个 | 自动生成 | [EMNLP 2025](https://aclanthology.org/2025.emnlp-demos.27/) |
| CVE-Bench | ⭐⭐ | ❌ | 命令行 | 40 | [ICML 2025](https://arxiv.org/abs/2503.17332) |
| BountyBench | ⭐⭐ | ❌ | 终端 | 40 | [arXiv:2505.15216](https://arxiv.org/abs/2505.15216) |
| SEC-bench | ⭐⭐ | ❌ | 代码 | 大量 | [arXiv:2506.11791](https://arxiv.org/abs/2506.11791) |
| App-Bench | ⭐ | ❌ | 代码生成 | 6 | [appbench.ai](https://appbench.ai/) |
| Design2Code | ⭐ | ❌ | 无 | 484 | [NAACL 2025](https://arxiv.org/abs/2403.03163) |

---

## 二、高价值数据集深度分析

---

### 2.1 MCP-Bench

**基本信息**
- 来源: Accenture (NeurIPS 2025 Workshop)
- 论文: [arXiv:2508.20453](https://arxiv.org/abs/2508.20453) (52页)
- 代码: [github.com/Accenture/mcp-bench](https://github.com/Accenture/mcp-bench)
- 规模: 28个MCP server, 250个工具, 104个任务

**论文核心思路**

MCP-Bench的核心问题是：之前的tool calling benchmark（包括τ-bench）都有一个共同缺陷——工具之间是"人为拼接"的，不是自然配合的。MCP-Bench通过使用真实MCP server来解决这个问题，因为每个MCP server内部的工具天然是配套的（例如一个科学计算server集成了数据加载、矩阵运算和可视化）。

**论文明确指出τ-bench的不足：**
> "τ-Bench moves a step further by selecting a small set of APIs whose interfaces are relatively compatible...However, its coverage is limited to only a handful of domains and tools"

**数据构建策略（论文Section 4.2，关键）**

MCP-Bench的任务是**自动合成**的，分三步：

1. **依赖链发现（Dependency Chain Discovery）**: 分析所有工具的输入/输出签名，自动发现"工具A的输出可以作为工具B的输入"的链条。这和你的workflow域的data_ref设计异曲同工，但MCP-Bench是从真实工具的schema自动推导的。

2. **质量过滤（Automatic Quality Filtering）**: 用LLM评估每个生成的任务的"可解性"(solvability ≥ 9/10) 和"实用性"(utility ≥ 5/10)。不合格的丢弃。

3. **任务模糊化（Task Description Fuzzing）**: 生成每个任务的两个版本：
   - `task_description`: 明确的步骤说明（"第一步调用X工具，第二步调用Y工具..."）
   - `fuzzy_description`: 自然语言需求（"帮我查一下..."）
   - 测试时只给模型 `fuzzy_description`，迫使模型自己规划工具链

**独特设计：干扰服务器**

每个任务都附带10个"干扰server"（distraction_servers），引入100+个无关工具。模型需要在大量工具中选对正确的。这个维度你现在的数据完全没有。

**关键发现（对你的训练有启示）：**
- Schema理解已经趋同（>95%），**不再是瓶颈**
- **规划能力是真正的差距**：dependency awareness和parallelism efficiency才是区分模型强弱的关键
- 弱模型平均需要155次tool call完成一个任务，强模型只需要20-30次
- kimi-k2得分0.629（Table 3），排名中游

**实际数据格式（从repo中提取）：**

任务文件 `tasks/mcpbench_tasks_single_runner_format.json`:
```json
{
  "server_tasks": [
    {
      "server_name": "OpenAPI Explorer",
      "tasks": [
        {
          "task_id": "openapi_explorer_000",
          "task_description": "Step 1: Use explore_api to find endpoints...\nStep 2: Use test_endpoint to...",
          "fuzzy_description": "I need to understand how the weather API works and test it with my city",
          "dependency_analysis": "explore_api → test_endpoint → format_response",
          "distraction_servers": ["Bibliomantic", "Call for Papers", "FruityVice", ...]
        }
      ],
      "servers": ["OpenAPI Explorer"],
      "combination_type": "single_server"
    }
  ]
}
```

已有轨迹数据: `mcp_servers/medcalc/MedCalcBench/evaluation/outputs/**/*.jsonl` (JSONL格式的模型输出+ground truth)

**对你的价值：**
- 🟢 任务合成pipeline可以复制（依赖链发现→质量过滤→模糊化）
- 🟢 干扰工具设计可以加入你的训练数据
- 🟢 fuzzy_description训练模型理解模糊指令
- 🟢 有预收集的轨迹数据

**链接汇总：**
- 论文PDF: https://arxiv.org/pdf/2508.20453
- GitHub: https://github.com/Accenture/mcp-bench
- HuggingFace: https://huggingface.co/papers/2508.20453
- OpenReview: https://openreview.net/forum?id=fe8mzHwMxN

---

### 2.2 LiveMCPBench

**基本信息**
- 来源: 中科院信工所 (ICLR 2026提交)
- 论文: [arXiv:2508.01780](https://arxiv.org/abs/2508.01780)
- 代码: [github.com/icip-cas/LiveMCPBench](https://github.com/icip-cas/LiveMCPBench)
- 规模: 70个MCP server, 527个工具, 95个任务

**论文核心思路**

LiveMCPBench解决的核心问题是**工具池规模**。现实中MCP生态已有超过10000个server，但之前的benchmark最多只测十几个。LiveMCPBench构建了527个工具的池子，测试agent在"海洋般"的工具中找对并使用正确工具的能力。

**关键发现：**
> "检索错误占所有失败的近一半" —— 在大工具池中，模型最大的问题不是不会用工具，而是**找不到正确的工具**

**数据构建策略（关键）**

1. **工具收集（LiveMCPTool）**: 从MCP生态中筛选了70个高质量server，提供527个工具，覆盖Finance/Office/Research/Life等类别。所有server打包成"ready-to-deploy"套件，无需逐个配置API。

2. **任务设计**: 95个真实日常任务，每个任务都有人工标注的：
   - 执行步骤（Steps）
   - 需要的工具列表（Tools）
   - 步骤数和工具数
   这些标注可以作为ground truth用于训练。

3. **评估（LiveMCPEval）**: LLM-as-Judge评估，81%与人类评审一致。处理动态数据源和多种有效解法。

4. **Agent架构（MCP Copilot Agent）**: 论文提出了一个ReACT-based的agent，支持工具路由和动态规划。

**实际数据格式（最有价值！）**

任务文件 `annotated_data/all_annotations.json`:
```json
[
  {
    "task_id": "0e3287cb-c0ff-4d2a-8c3d-d8833014a7b0",
    "Question": "Generate a well-formatted PDF report summarizing the top 50 trending books on WeChat Read this week. Include: book title, author, category, and popularity ranking. Add a word cloud visualization of the book titles.",
    "answers": "file /root/pdf/wechat_reading_report.pdf",
    "category": "Office",
    "Annotator Metadata": {
      "Steps": "1. Getting the current trends on WeChat Read\n2. Generate a word cloud based on the book titles\n3. Compile the data into a structured report\n4. Format and export the report as a PDF\n5. Verify the output file exists and contains the expected content",
      "Number of steps": "5",
      "Tools": "1. get-weread-rank\n2. generate_word_cloud_chart\n3. create_document\n4. export_to_pdf\n5. read_file",
      "Number of tools": "6"
    }
  }
]
```

**完整对话轨迹（可直接用于SFT训练！）**

文件 `baseline/output/claude-sonnet-4-20250514_*.json`:
```json
[
  {
    "task_id": "...",
    "Question": "...",
    "response": "Excellent! I have successfully generated...",
    "messages": [
      {"role": "system", "content": "You are an agent designed to assist..."},
      {"role": "user", "content": "Generate a well-formatted PDF report..."},
      {
        "role": "assistant",
        "content": "I'll help you generate...",
        "tool_calls": [
          {
            "id": "toolu_01P4irvih3iqHJ9uBU5bsE5X",
            "function": {
              "arguments": "{\"query\": \"trending books\"}",
              "name": "route"
            },
            "type": "function"
          }
        ]
      },
      {
        "role": "tool",
        "tool_call_id": "toolu_01P4irvih3iqHJ9uBU5bsE5X",
        "content": "meta=None content=[TextContent(...)]"
      },
      ...
    ]
  }
]
```

工具定义 `tools/LiveMCPTool/tools.json` (OpenAI function calling格式):
```json
{
  "name": "MCP Yahoo Finance",
  "tools": {
    "yahoo-finance": {
      "tools": [
        {
          "name": "get_current_stock_price",
          "description": "Get the current stock price for a given symbol",
          "inputSchema": {
            "type": "object",
            "properties": {
              "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
            },
            "required": ["symbol"]
          }
        }
      ]
    }
  }
}
```

**对你的价值：**
- 🟢🟢🟢 **最高优先级** —— `baseline/output/` 有Claude-Sonnet-4的完整对话轨迹，格式与OpenAI训练格式一致
- 🟢 95个任务，每个都有人工标注的Steps和Tools作为ground truth
- 🟢 527个工具的定义文件可以直接作为tools参数
- 🟢 训练模型在大工具池中做"工具路由"（这是你现在完全缺少的能力）

**你可以立即做：**
```bash
git clone https://github.com/icip-cas/LiveMCPBench
# 提取训练数据：
python -c "
import json
with open('baseline/output/claude-sonnet-4-*.json') as f:
    data = json.load(f)
for traj in data:
    # traj['messages'] 就是完整的SFT训练数据
    # 格式：system + user + assistant(tool_calls) + tool(result) + ...
    pass
"
```

**链接汇总：**
- 论文PDF: https://arxiv.org/pdf/2508.01780
- GitHub: https://github.com/icip-cas/LiveMCPBench
- 项目主页: https://icip-cas.github.io/LiveMCPBench/
- HuggingFace: https://huggingface.co/papers/2508.01780
- OpenReview: https://openreview.net/forum?id=0sPCSssY2r

---

### 2.3 Toolathlon (Tool Decathlon)

**基本信息**
- 来源: 香港科技大学 (ICLR 2026)
- 论文: [arXiv:2510.25726](https://arxiv.org/abs/2510.25726)
- 代码: [github.com/hkust-nlp/Toolathlon](https://github.com/hkust-nlp/Toolathlon)
- 规模: 32个软件应用, 604个工具, 108个任务

**论文核心思路**

Toolathlon的独特贡献是**真实性**。之前的benchmark即使用了真实API，环境初始状态也是简化的（空数据库、空日历等）。Toolathlon提供了真实的初始状态——Canvas课程有几十个学生、Google Sheet有真实数据、WooCommerce有真实商品。这使得任务更接近真实世界。

**数据构建策略：**
- 108个任务全部**手工标注**（不是自动生成），质量最高
- 每个任务平均需要**20轮**tool calling（你的数据平均5轮，差距4倍）
- 工具基于MCP server标准，但作者自己修改/实现了很多
- 覆盖32个真实软件：Google Calendar、Notion、WooCommerce、Kubernetes、BigQuery、GitHub、Slack...

**任务特点：**
- 多应用协调：发邮件+查日历+管文件
- 长horizon：平均20轮，最长可能30+轮
- 确定性评估：每个任务有专用评估脚本

**关键发现：**
- Claude-4.5-Sonnet最强但仅38.6%成功率
- 错误恢复、长context管理、自主规划是最大挑战

**对你的价值：**
- 🟢 20轮长horizon的工具调用（你最缺的训练数据维度）
- 🟢 真实软件系统交互
- 🟡 需要搭建环境（32个软件）才能跑
- 🟡 代码已公开但搭建成本较高

**链接汇总：**
- 论文PDF: https://arxiv.org/pdf/2510.25726
- GitHub: https://github.com/hkust-nlp/Toolathlon
- 项目主页: https://toolathlon.xyz/
- HuggingFace: https://huggingface.co/papers/2510.25726
- OpenReview: https://openreview.net/forum?id=z53s5p0qhf

---

### 2.4 MCP-Universe

**基本信息**
- 来源: Salesforce AI Research (NeurIPS 2025)
- 论文: [arXiv:2508.14704](https://arxiv.org/abs/2508.14704)
- 代码: [github.com/SalesforceAIResearch/MCP-Universe](https://github.com/SalesforceAIResearch/MCP-Universe)
- 规模: 11个MCP server, 231个任务, 84个evaluator

**论文核心思路**

MCP-Universe是**第一个**综合MCP benchmark（比MCP-Bench早几周发布）。它的特点是评估体系完善：3种evaluator（格式/静态/动态）处理不同类型的验证需求，特别是动态evaluator可以实时获取ground truth（处理时间敏感的数据）。

**数据构建策略：**
- 6个领域：导航(45)、搜索(55)、浏览器(39)、金融(40)、仓库管理(33)、3D设计(19)
- 需要真实API key（Google Maps, GitHub等）
- 有Docker支持，可容器化部署

**三大挑战（论文发现）：**
1. **Long-Context**: 交互步骤多了，token数暴增，context overflow
2. **Unknown-Tools**: 模型不熟悉具体MCP server的使用模式
3. **Cross-Domain**: 不同领域成功率差异巨大

**实际数据格式：**

任务文件 `tests/data/task/*.json`:
```json
{
  "category": "general",
  "question": "Plan a road trip starting from Johor Bahru to Kuala Lumpur with 2 rest stops...",
  "mcp_servers": [{"name": "google-maps"}],
  "output_format": {
    "starting_city": "[Starting City]",
    "routes": [{"route_id": "1", "cities_visited": [...]}]
  },
  "evaluators": [
    {"func": "json -> get(starting_city)", "op": "=", "value": "Johor Bahru"}
  ]
}
```

**对你的价值：**
- 🟡 需要配置API key才能跑
- 🟢 任务设计思路可借鉴（evaluator体系）
- 🟢 231个任务覆盖6个领域

**链接汇总：**
- 论文PDF: https://arxiv.org/pdf/2508.14704
- GitHub: https://github.com/SalesforceAIResearch/MCP-Universe
- 文档: https://mcp-universe.github.io/
- OpenReview: https://openreview.net/forum?id=ffYd6uJpJE

---

### 2.5 MCPEval

**基本信息**
- 来源: Salesforce AI Research (EMNLP 2025)
- 论文: [EMNLP 2025 Demo](https://aclanthology.org/2025.emnlp-demos.27/)
- 代码: [github.com/SalesforceAIResearch/MCPEval](https://github.com/SalesforceAIResearch/MCPEval)

**核心定位**

MCPEval更偏向**评估框架**而非数据集。它的核心价值是可以自动生成评估任务，并提供标准化的评估pipeline。包含多个MCP server实现（yfinance、sqlite、travel_assistant等）。

**对你的价值：**
- 🟡 框架本身不提供训练数据
- 🟡 内置MCP server可以参考
- 🟡 可以用来评估你训练后的模型

**链接汇总：**
- 论文: https://aclanthology.org/2025.emnlp-demos.27/
- GitHub: https://github.com/SalesforceAIResearch/MCPEval

---

## 三、低价值数据集简要分析

### CVE-Bench
- **做什么:** 40个真实CVE漏洞利用
- **为什么不相关:** Agent在Docker沙盒中执行攻击代码，使用的是命令行工具，不是function calling格式
- **链接:** [GitHub](https://github.com/uiuc-kang-lab/cve-bench) | [论文](https://arxiv.org/abs/2503.17332)

### BountyBench
- **做什么:** 25个系统的bug bounty（检测/利用/修补）
- **为什么不相关:** Kali Linux容器中的终端操作，不是function calling
- **链接:** [项目主页](http://bountybench.github.io/) | [论文](https://arxiv.org/abs/2505.15216) | [Stanford Blog](https://ai.stanford.edu/blog/bountybench/)

### SEC-bench
- **做什么:** 自动化安全benchmark（PoC生成+漏洞修补）
- **为什么不相关:** 代码agent任务
- **链接:** [论文](https://arxiv.org/abs/2506.11791)

### App-Bench
- **做什么:** 从自然语言生成完整Web应用
- **为什么不相关:** 代码生成任务，测的是全栈开发能力
- **链接:** [appbench.ai](https://appbench.ai/)

### Design2Code
- **做什么:** 网页截图→HTML/CSS代码
- **为什么不相关:** 多模态代码生成，与tool calling无关
- **链接:** [GitHub](https://github.com/NoviScl/Design2Code) | [论文](https://arxiv.org/abs/2403.03163)

---

## 四、对你训练策略的启示

### 4.1 从论文中提取的关键insight

**MCP-Bench论文的Table 1对比（直接批评了τ-bench）：**

| Benchmark | 域数 | 工具数 | MCP | 信息 Grounding | 模糊指令 | 复杂多目标 | 跨域编排 |
|-----------|------|-------|-----|---------------|---------|----------|---------|
| τ-Bench | 2 | 28 | ✗ | ✗ | ✗ | ✗ | ✗ |
| MCP-Bench | 28 | 250 | ✓ | ✓ | ✓ | ✓ | ✓ |

这说明你的训练数据还需要补充：
1. **模糊指令**（不指定用哪个工具）
2. **信息Grounding**（回答必须引用工具返回的数据）
3. **跨域编排**（一个任务用多个域的工具）

**MCP-Bench的kimi-k2表现：**
- Overall: 0.629（排名第12/20）
- Tool Appropriateness: 0.631（还行）
- Dependency Awareness: 0.448（弱项！）
- Parallelism and Efficiency: 0.307（最弱项！）

→ 这意味着你的训练数据应该重点强化**依赖感知**和**并行执行效率**

### 4.2 你当前数据 vs benchmark数据的互补关系

| 维度 | 你的5+1个域 | 外部benchmark | 互补性 |
|------|----------|--------------|--------|
| 工具类型 | mock CRUD + mock编排 | 真实MCP server | 🟢 互补 |
| 工具池大小 | 15-20个/域 | 250-604个 | 🟢 互补 |
| 任务长度 | 平均5步 | 平均6-20步 | 🟢 互补 |
| 模糊指令 | ❌ 都明确 | ✅ fuzzy_description | 🟢 互补 |
| 干扰工具 | ❌ 没有 | ✅ 10个干扰server | 🟢 互补 |
| thinking数据 | ✅ kimi-k2.5有 | ❌ 无reasoning | 🟢 你独有 |
| 跨域编排 | workflow域有 | ✅ 全面 | ✅ 一致 |

### 4.3 推荐行动计划

| 优先级 | 行动 | 预期产出 | 难度 |
|-------|------|---------|------|
| **P0** | 提取LiveMCPBench的`baseline/output/`轨迹 | 95个任务的完整SFT数据（格式现成） | 低 |
| **P1** | 提取MCP-Bench的评估输出轨迹 | 104个任务的JSONL数据 | 低 |
| **P2** | 用kimi-k2.5跑你的6个域全量任务 | 415个thinking+tool calling轨迹 | 中 |
| **P3** | 参考MCP-Bench的任务合成pipeline，给你的域加模糊指令+干扰工具 | 提升训练数据质量 | 中 |
| **P4** | 搭建Toolathlon环境，收集20轮长horizon轨迹 | 最长chain的训练数据 | 高 |
| **P5** | 用MCP-Universe跑231个任务 | 真实API交互轨迹（需API key） | 高 |

---

## 五、所有链接汇总

### 高价值（直接相关）
| 数据集 | GitHub | 论文 | 项目主页 |
|--------|--------|------|---------|
| MCP-Bench | [Accenture/mcp-bench](https://github.com/Accenture/mcp-bench) | [arXiv:2508.20453](https://arxiv.org/abs/2508.20453) | - |
| LiveMCPBench | [icip-cas/LiveMCPBench](https://github.com/icip-cas/LiveMCPBench) | [arXiv:2508.01780](https://arxiv.org/abs/2508.01780) | [icip-cas.github.io/LiveMCPBench](https://icip-cas.github.io/LiveMCPBench/) |
| Toolathlon | [hkust-nlp/Toolathlon](https://github.com/hkust-nlp/Toolathlon) | [arXiv:2510.25726](https://arxiv.org/abs/2510.25726) | [toolathlon.xyz](https://toolathlon.xyz/) |
| MCP-Universe | [SalesforceAIResearch/MCP-Universe](https://github.com/SalesforceAIResearch/MCP-Universe) | [arXiv:2508.14704](https://arxiv.org/abs/2508.14704) | [mcp-universe.github.io](https://mcp-universe.github.io/) |
| MCPEval | [SalesforceAIResearch/MCPEval](https://github.com/SalesforceAIResearch/MCPEval) | [EMNLP 2025](https://aclanthology.org/2025.emnlp-demos.27/) | - |

### 低价值（安全/代码领域）
| 数据集 | GitHub | 论文 |
|--------|--------|------|
| CVE-Bench | [uiuc-kang-lab/cve-bench](https://github.com/uiuc-kang-lab/cve-bench) | [arXiv:2503.17332](https://arxiv.org/abs/2503.17332) |
| BountyBench | [bountybench.github.io](http://bountybench.github.io/) | [arXiv:2505.15216](https://arxiv.org/abs/2505.15216) |
| SEC-bench | - | [arXiv:2506.11791](https://arxiv.org/abs/2506.11791) |
| App-Bench | [appbench.ai](https://appbench.ai/) | - |
| Design2Code | [NoviScl/Design2Code](https://github.com/NoviScl/Design2Code) | [arXiv:2403.03163](https://arxiv.org/abs/2403.03163) |

### 老板提到的其他benchmark（论文中引用的）
| Benchmark | 论文 | 备注 |
|-----------|------|------|
| GDPval-AA | OpenAI发布 | 44种职业真实任务评估 |
| PaperBench Code-Dev | OpenAI发布 | ML论文代码复现 |
| CyberGym | [论文](https://arxiv.org/abs/2507.04025) | 1507个真实漏洞的PoC生成 |
| WebGen-Bench | - | 多页面网站生成 |
| WebCoderBench | - | 1572条工业需求网页生成 |
| MCP-RADER | [arXiv:2505.16700](https://arxiv.org/abs/2505.16700) | MCP-Bench论文中引用的早期工作 |
