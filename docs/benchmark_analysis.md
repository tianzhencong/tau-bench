# Tool Calling Benchmark 数据集深度分析报告

> 生成日期: 2024-02-28
> 目的: 分析老板列出的10个数据集，判断哪些对优化model tool_calling能力有实际价值

---

## 一、总览

| 数据集 | 相关度 | 有SFT数据？ | 工具数 | 任务数 | 核心考察能力 |
|--------|-------|-----------|-------|-------|------------|
| **MCP-Bench** | ⭐⭐⭐⭐⭐ | ✅ 有JSONL轨迹 | 250 | 大量 | 大工具池选择+跨域编排 |
| **LiveMCPBench** | ⭐⭐⭐⭐⭐ | ✅ 有完整对话轨迹 | 527 | 95 | 海量工具导航+长链 |
| **MCP-Universe** | ⭐⭐⭐⭐ | ⚠️ 仅元数据 | 11 servers | 231 | 真实MCP交互 |
| **Toolathlon** | ⭐⭐⭐⭐⭐ | 需要跑 | 604 | 108 | 真实软件20轮交互 |
| **MCPEval** | ⭐⭐⭐ | ⚠️ 仅评估指标 | 多个 | 自动生成 | 评估框架 |
| CVE-Bench | ⭐⭐ | ❌ | 命令行 | 40 | 安全漏洞利用 |
| BountyBench | ⭐⭐ | ❌ | 终端 | 40 | 漏洞生命周期 |
| SEC-bench | ⭐⭐ | ❌ | 代码 | 大量 | 安全工程 |
| App-Bench | ⭐ | ❌ | 代码生成 | 6 | 全栈应用生成 |
| Design2Code | ⭐ | ❌ | 无 | 484 | 视觉→代码 |

---

## 二、最有价值的5个数据集（详细分析）

### 2.1 MCP-Bench（Accenture, NeurIPS 2025 Workshop）

**它是什么：** 28个真实MCP server、250个工具，测试agent在大工具池中选择和编排工具完成复杂任务。

**GitHub：** https://github.com/Accenture/mcp-bench

**任务数据格式（实际样本）：**
```json
{
  "task_id": "openapi_explorer_000",
  "task_description": "Detailed step-by-step instructions...",
  "fuzzy_description": "Natural language user request...",
  "dependency_analysis": "Tool dependency chain description...",
  "distraction_servers": ["Bibliomantic", "Call for Papers", ...]
}
```

**关键特点：**
- 每个任务有两种描述：`task_description`（详细步骤）和 `fuzzy_description`（模糊自然语言，更接近真实用户）
- `dependency_analysis` 描述了工具之间的依赖链
- `distraction_servers` 是干扰项 —— agent必须在大量无关工具中选对
- 有**单server**和**多server**两种任务类型

**已有轨迹数据：** ✅ 有JSONL格式的评估输出（在 `mcp_servers/medcalc/MedCalcBench/evaluation/outputs/` 中）

**对你的价值：**
- 🟢 直接可用的tool calling轨迹数据
- 🟢 "干扰工具"设计 —— 你现在的数据缺少这个维度（agent只看到本域的15-17个工具）
- 🟢 `fuzzy_description` 训练模型理解模糊指令

**你能怎么用：**
1. 直接用已有轨迹做SFT
2. 参考"干扰server"的设计，在你的域里加入无关工具增加难度

---

### 2.2 LiveMCPBench（ICLR 2026提交）

**它是什么：** 70个MCP server、527个工具、95个真实任务，最大规模的MCP工具池benchmark。

**GitHub：** https://github.com/icip-cas/LiveMCPBench

**任务数据格式（实际样本）：**
```json
{
  "task_id": "0e3287cb-c0ff-4d2a-8c3d-d8833014a7b0",
  "Question": "Generate a well-formatted PDF report...",
  "answers": "file /root/pdf/wechat_reading_report.pdf",
  "category": "Office",
  "Annotator Metadata": {
    "Steps": "1. Getting the current trends...\n2. Generate a word cloud...",
    "Number of steps": "5",
    "Tools": "1. get-weread-rank\n2. generate_word_cloud_chart...",
    "Number of tools": "6"
  }
}
```

**工具定义格式（实际样本）：**
```json
{
  "name": "MCP Yahoo Finance",
  "tools": {
    "yahoo-finance": {
      "tools": [
        {
          "name": "get_current_stock_price",
          "description": "Get the current stock price...",
          "inputSchema": {
            "type": "object",
            "properties": {
              "symbol": {"type": "string", "description": "Stock symbol..."}
            },
            "required": ["symbol"]
          }
        }
      ]
    }
  }
}
```

**已有轨迹数据（实际样本）：** ✅ 完整的多轮对话轨迹，格式与OpenAI function calling完全一致！
```json
{
  "task_id": "...",
  "messages": [
    {"role": "system", "content": "You are an agent..."},
    {"role": "user", "content": "Generate a well-formatted PDF report..."},
    {
      "role": "assistant",
      "content": "I'll help you generate...",
      "tool_calls": [
        {
          "id": "toolu_01P4irvih3iqHJ9uBU5bsE5X",
          "function": {
            "arguments": "{\"query\": \"...\"}",
            "name": "route"
          },
          "type": "function"
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "toolu_01P4irvih3iqHJ9uBU5bsE5X",
      "content": "..."
    }
  ]
}
```

**对你的价值：**
- 🟢🟢🟢 **最有价值** —— 已有完整对话轨迹，格式与OpenAI训练格式一致
- 🟢 527个工具池 + 95个任务的轨迹 → 直接可转SFT数据
- 🟢 Annotator Metadata记录了ground truth步骤和工具
- 🟢 覆盖Office/Finance/Research等多种场景

**你能怎么用：**
1. **直接提取** `baseline/output/*.json` 中的 `messages` 数组作为SFT训练数据
2. 轨迹格式已经是 system + user + assistant(tool_calls) + tool(result)，与你的训练目标完全一致
3. 可以按 category 过滤，选择与你目标最相关的场景

---

### 2.3 Toolathlon（ICLR 2026）

**它是什么：** 32个真实软件应用、604个工具、108个手工任务，平均每个任务需要20轮tool calling。

**注意：** GitHub repo没找到（可能未公开代码），但论文数据公开。

**关键特点：**
- 使用真实软件：Google Calendar、Notion、WooCommerce、Kubernetes、BigQuery等
- 任务平均需要**20轮**tool calling（你现在的数据平均5轮）
- 手工标注的108个任务，质量非常高
- 工具基于MCP server标准

**性能：** 最强模型(Claude)仅44.8%成功率

**对你的价值：**
- 🟢 20轮长horizon的tool calling训练数据（你最缺的）
- 🟢 真实软件系统交互
- 🟡 需要自己搭环境跑benchmark收集轨迹

**你能怎么用：**
1. 等代码公开后搭建环境
2. 用强模型跑benchmark收集成功轨迹
3. 20轮长horizon的数据对提升长链推理能力最有价值

---

### 2.4 MCP-Universe（Salesforce, NeurIPS 2025）

**它是什么：** 11个真实MCP server、231个任务，首个综合MCP benchmark。

**GitHub：** https://github.com/SalesforceAIResearch/MCP-Universe

**任务数据格式（实际样本）：**
```json
{
  "category": "general",
  "question": "Plan a road trip starting from Johor Bahru...",
  "mcp_servers": [{"name": "google-maps"}],
  "output_format": {
    "starting_city": "[Starting City]",
    "routes": [
      {
        "route_id": "1",
        "cities_visited": ["[City 1]", ...],
        "total_distance_km": "[Estimated Distance]"
      }
    ]
  },
  "evaluators": [
    {
      "func": "json -> get(starting_city)",
      "op": "=",
      "value": "Johor Bahru"
    }
  ]
}
```

**关键特点：**
- 6个领域：导航、搜索、浏览器自动化、金融分析、仓库管理、3D设计
- 有结构化的评估器（evaluators）和清理函数
- 需要真实API key（Google Maps、GitHub等）

**已有轨迹数据：** ⚠️ 主要是元数据和评估配置，没有预收集的完整轨迹

**对你的价值：**
- 🟡 需要配置API key后自己跑来收集轨迹
- 🟢 任务设计质量高（231个任务，覆盖6个领域）
- 🟢 评估框架可复用

---

### 2.5 MCPEval（Salesforce, EMNLP 2025）

**它是什么：** 自动化MCP评估框架，5个领域端到端评估。

**GitHub：** https://github.com/SalesforceAIResearch/MCPEval

**关键特点：**
- 更偏向**评估框架**而非数据集
- 包含多个MCP server实现（yfinance、sqlite、travel_assistant等）
- 支持自动任务生成
- 有Web UI和CLI

**已有轨迹数据：** ⚠️ 只有评估指标（metrics），没有完整对话轨迹

**对你的价值：**
- 🟡 可以用这个框架自动生成新的评估任务
- 🟡 内置的MCP server可以作为你构造新domain的参考
- 🔴 本身不提供可直接用的训练数据

---

## 三、不太相关的5个数据集（简要分析）

### CVE-Bench（ICML 2025 Spotlight）
- **做什么：** 40个真实Web应用CVE漏洞，让agent写利用代码
- **格式：** 输入CVE描述 → agent在Docker沙盒中执行攻击代码
- **为什么不相关：** 主要是代码生成+执行，不是标准tool calling格式。Agent使用的是命令行工具，不是function calling API。
- **数据：** 无预收集轨迹

### BountyBench（Stanford 2025）
- **做什么：** 25个真实系统的bug bounty任务（检测/利用/修补）
- **格式：** Agent在Kali Linux容器中操作
- **为什么不相关：** 和CVE-Bench类似，是终端命令式交互，不是function calling
- **数据：** GitHub有代码但无训练轨迹

### SEC-bench（NeurIPS 2025）
- **做什么：** 自动化安全benchmark，PoC生成+漏洞修补
- **为什么不相关：** 代码agent，不是tool calling agent

### App-Bench（AfterQuery 2025）
- **做什么：** 从自然语言生成完整Web应用
- **为什么不相关：** 完全是代码生成任务，不涉及tool calling

### Design2Code（NAACL 2025）
- **做什么：** 484个网页截图→HTML/CSS代码
- **为什么不相关：** 多模态代码生成，与tool calling完全无关

---

## 四、行动建议

### 立即可做（本周）

| 优先级 | 数据集 | 行动 | 预期产出 |
|-------|--------|------|---------|
| **P0** | LiveMCPBench | 直接从 `baseline/output/` 提取对话轨迹 | 95个任务的完整SFT数据，格式现成 |
| **P1** | MCP-Bench | 从 `evaluation/outputs/` 提取轨迹 | 多server组合的tool calling数据 |
| **P2** | 你的5个域 | 用kimi-k2.5跑全量任务 | 415个任务的thinking+tool calling轨迹 |

### 中期可做（2-4周）

| 优先级 | 数据集 | 行动 | 预期产出 |
|-------|--------|------|---------|
| **P3** | MCP-Universe | 配置API key，用强模型跑231个任务 | 真实MCP交互轨迹 |
| **P4** | Toolathlon | 等代码公开，搭建环境 | 20轮长horizon轨迹 |
| **P5** | MCPEval | 用其框架生成新评估任务 | 扩大评估覆盖面 |

### 不建议投入

CVE-Bench、BountyBench、SEC-bench、App-Bench、Design2Code — 它们考察的是代码生成/安全能力，不是tool calling。如果后续要做coding agent可以再看。

---

## 五、LiveMCPBench 数据提取指南（最有价值）

LiveMCPBench 的轨迹数据已经是OpenAI function calling格式，可以直接提取：

```python
import json

# 读取轨迹
with open("baseline/output/claude-sonnet-4-*.json") as f:
    trajectories = json.load(f)

# 提取训练数据
for traj in trajectories:
    messages = traj["messages"]  # 直接可用的SFT数据
    # messages 格式:
    # [
    #   {"role": "system", "content": "..."},
    #   {"role": "user", "content": "..."},
    #   {"role": "assistant", "content": "...", "tool_calls": [...]},
    #   {"role": "tool", "tool_call_id": "...", "content": "..."},
    #   ...
    # ]
```

工具定义在 `tools/LiveMCPTool/tools.json`，格式与OpenAI tools schema完全一致。

---

## 六、与你现有数据的互补关系

| 维度 | 你的5个域 | LiveMCPBench/MCP-Bench | 互补性 |
|------|----------|----------------------|--------|
| 工具类型 | mock CRUD | 真实MCP server | 🟢 互补 |
| 工具池大小 | 15-20个/域 | 250-527个 | 🟢 互补 |
| 任务长度 | 平均5步 | 平均6-20步 | 🟢 互补 |
| 数据流 | workflow域有 | 全部都有 | ✅ 一致 |
| 用户模拟 | LLM模拟 | 人工标注任务 | 🟢 互补 |
| thinking数据 | kimi-k2.5有 | 无reasoning | 🟢 你独有 |

**最佳策略：** 你的5个域提供thinking model的SFT数据（带reasoning_content），外部benchmark提供真实工具交互的SFT数据。两者混合训练。
