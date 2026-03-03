# 潜在SFT数据收集榜单调研

> 调研目标：评估每个榜单能否收集到tool calling SFT训练数据

---

## 总览

| 榜单 | 能收集SFT？ | 数据形式 | 工具数 | 任务数 | 需要什么环境 | 推荐优先级 |
|------|-----------|---------|-------|-------|------------|----------|
| **MCP-Bench** | ✅ 可以 | function calling轨迹 | 250 | 104 | 28个MCP server | ⭐⭐⭐⭐⭐ |
| **LiveMCPBench** | ✅ 可以 | function calling轨迹 | 527 | 95 | Docker + Embedding模型 | ⭐⭐⭐⭐⭐ |
| **MCP-Universe** | ✅ 可以 | function calling轨迹 | 多个 | 231 | 11个MCP server + API key | ⭐⭐⭐⭐ |
| **Toolathlon** | ✅ 可以 | function calling轨迹 | 604 | 108 | 32个软件系统 | ⭐⭐⭐⭐ |
| **MCPEval** | 🟡 间接 | 评估框架可生成任务 | 多个 | 自动生成 | MCP server | ⭐⭐⭐ |
| **CVE-Bench** | ❌ 不适合 | 代码执行轨迹 | 命令行 | 40 | Docker沙盒 | ⭐ |
| **BountyBench** | ❌ 不适合 | 终端命令轨迹 | 终端 | 40 | Kali Linux | ⭐ |
| **SEC-bench** | ❌ 不适合 | 代码执行轨迹 | 代码工具 | 大量 | Docker | ⭐ |
| **App-Bench** | ❌ 不适合 | 代码生成 | 无tool calling | 6 | 无 | ⭐ |
| **Design2Code** | ❌ 不适合 | 图片→代码 | 无tool calling | 484 | 无 | ⭐ |

---

## 逐个详细分析

### 1. MCP-Bench

**来源：** Accenture，NeurIPS 2025 Workshop
**论文：** https://arxiv.org/abs/2508.20453
**代码：** https://github.com/Accenture/mcp-bench

**是什么：** 28个真实MCP server提供250个工具，agent在大工具池中完成104个跨域多步任务。每个任务附带10个干扰server（100+无关工具），测试agent从噪音中选对工具的能力。

**任务形式：** 每个任务有两个版本——`task_description`（详细步骤）和 `fuzzy_description`（模糊自然语言，不提工具名）。测试时只给模型fuzzy版本。

**任务示例：**
> "I'm working on a melanoma research project. I need: what ClinVar says about BRAF V600E pathogenicity, the 5 most influential papers on V600E-positive melanoma resistance, any Phase 2/3 trials recruiting V600E patients..."
> （需要跨 Paper Search + BioMCP 两个server，调用 gene_getter/variant_searcher/article_searcher/trial_searcher 等十多个工具）

**数据构建方法（论文Section 4.2）：**
1. 依赖链发现：分析工具输入/输出签名，自动发现A→B的依赖关系
2. LLM自动合成任务：基于依赖链生成自然语言任务
3. 质量过滤：可解性≥9/10，实用性≥5/10
4. 模糊化：去掉工具名和步骤提示

**评估方法：** 两层——规则评估（tool name正确率/schema合规率/执行成功率）+ LLM-as-Judge（任务完成/工具使用/规划效率，5次shuffle取平均）

**SFT数据收集方式：** 搭建28个MCP server → 用强模型跑104个任务 → 收集完整function calling轨迹

**环境搭建难度：** 中等。需要启动28个MCP server，部分可能需要API key。

**现有模型表现：** GPT-5得分0.749（第1），kimi-k2得分0.629（第12）

---

### 2. LiveMCPBench

**来源：** 中科院信工所，ICLR 2026提交
**论文：** https://arxiv.org/abs/2508.01780
**代码：** https://github.com/icip-cas/LiveMCPBench

**是什么：** 70个MCP server、527个工具、95个真实日常任务。目前规模最大的MCP工具池benchmark。

**任务形式：** 自然语言日常任务，每个任务有人工标注的Steps和Tools作为ground truth。

**任务示例：**
> "Generate a well-formatted PDF report summarizing current WeChat Reading trends and including a word cloud."
> （需要调用 get-weread-rank → generate_word_cloud_chart → create_document → add_paragraph → convert_to_pdf，跨3个MCP server）

**关键发现：** "检索错误占所有失败的近一半"——在527个工具中找对工具是最大挑战。

**评估方法：** LLM-as-Judge（LiveMCPEval），81%与人类评审一致。

**SFT数据收集方式：** Docker镜像（`docker pull hysdhlx/livemcpbench:latest`）→ 配置LLM API + Embedding API → 跑95个任务

**环境搭建难度：** 中等。需要Docker + Embedding模型（可用免费API如硅基流动）。69个MCP server全部不需要外部API key。

**已有轨迹：** repo中有Claude-Sonnet-4的完整对话轨迹（95条），但包含大量试错噪音，不建议直接用。

**现有模型表现：** Claude-Sonnet-4最高78.95%。

---

### 3. MCP-Universe

**来源：** Salesforce AI Research，NeurIPS 2025
**论文：** https://arxiv.org/abs/2508.14704
**代码：** https://github.com/SalesforceAIResearch/MCP-Universe

**是什么：** 首个综合MCP benchmark，11个MCP server、231个任务，覆盖6个领域（导航、搜索、浏览器自动化、金融分析、仓库管理、3D设计）。

**任务示例：**
> "Plan a road trip starting from Johor Bahru to Kuala Lumpur with 2 rest stops..."
> （需要调用 Google Maps 的 geocode/distance_matrix/directions 等API）

**评估方法：** 3种evaluator——格式检查、静态检查、动态检查（实时获取ground truth处理时间敏感数据）。

**SFT数据收集方式：** 需要配置真实API key（Google Maps等）→ 用模型跑231个任务

**环境搭建难度：** 中等偏高。需要Google Maps等外部API key。

**现有模型表现：** GPT-5仅43.72%。

---

### 4. Toolathlon (Tool Decathlon)

**来源：** 香港科技大学，ICLR 2026
**论文：** https://arxiv.org/abs/2510.25726
**代码：** https://github.com/hkust-nlp/Toolathlon

**是什么：** 32个真实软件应用（Google Calendar、Notion、WooCommerce、Kubernetes、BigQuery等）、604个工具、108个手工标注任务。

**核心特点：** 平均每个任务需要**20轮tool calling**（目前所有benchmark中最长）。提供真实的软件初始状态（Canvas课程有几十个学生、Google Sheet有真实数据等）。

**任务示例：**
> 管理邮件+日历+文件系统的跨App工作流；监控数据库异常+生成报告

**评估方法：** 每个任务有专用评估脚本，确定性执行验证。

**SFT数据收集方式：** 搭建32个软件系统 → 用模型跑108个任务

**环境搭建难度：** 高。需要搭建32个真实软件。

**现有模型表现：** Claude-4.5-Sonnet仅38.6%。

---

### 5. MCPEval

**来源：** Salesforce AI Research，EMNLP 2025
**论文：** https://aclanthology.org/2025.emnlp-demos.27/
**代码：** https://github.com/SalesforceAIResearch/MCPEval

**是什么：** 自动化MCP评估**框架**（不是数据集）。可以自动生成评估任务、支持Web UI和CLI。内置多个MCP server实现（yfinance、sqlite、travel_assistant、sports等）。

**SFT数据收集方式：** 用框架自动生成任务 → 用模型跑 → 收集轨迹。更适合作为评估工具而非数据来源。

**环境搭建难度：** 低。pip install + 配置即可。

---

### 6. CVE-Bench

**来源：** UIUC，ICML 2025 Spotlight
**论文：** https://arxiv.org/abs/2503.17332
**代码：** https://github.com/uiuc-kang-lab/cve-bench

**是什么：** 40个真实Web应用CVE漏洞，让agent在Docker沙盒中写利用代码触发crash。

**为什么不适合收集tool calling SFT：** agent使用的是命令行工具和代码执行，不是标准的function calling格式。交互模式是"写Python/C++代码 → 执行 → 看结果"，不是"选工具 → 传参数 → 获取返回"。

**如果做安全领域agent可以关注。**

---

### 7. BountyBench

**来源：** Stanford，2025
**论文：** https://arxiv.org/abs/2505.15216
**代码：** https://bountybench.github.io/

**是什么：** 25个真实开源系统的bug bounty任务，覆盖OWASP Top 10。3种任务：检测漏洞、利用漏洞、修补漏洞。

**为什么不适合：** agent在Kali Linux容器中操作，使用终端命令而非function calling。

---

### 8. SEC-bench

**来源：** NeurIPS 2025
**论文：** https://arxiv.org/abs/2506.11791

**是什么：** 自动化安全benchmark，用多agent框架自动构建漏洞数据集。评估PoC生成(18%成功率)和漏洞修补(34%成功率)。

**为什么不适合：** 代码agent任务，非function calling格式。

---

### 9. App-Bench

**来源：** AfterQuery，2025
**网站：** https://appbench.ai/

**是什么：** 评估AI从自然语言prompt生成完整Web应用的能力。6个行业场景，测试RAG集成、实时同步、认证流程等。

**为什么不适合：** 是代码生成评估，不涉及tool calling。最强工具实现77%功能。

---

### 10. Design2Code

**来源：** NAACL 2025
**论文：** https://arxiv.org/abs/2403.03163
**代码：** https://github.com/NoviScl/Design2Code

**是什么：** 484个真实网页截图→HTML/CSS代码的转换benchmark。

**为什么不适合：** 多模态代码生成任务，完全不涉及tool calling。

---

## 收集SFT数据的优先级排序

| 优先级 | 数据源 | 预计产出 | 搭建成本 | 数据质量 |
|-------|--------|---------|---------|---------|
| **P0** | AppWorld | 191条已产出，可扩展到400+ | ✅ 已完成 | 高（真实数据+评估） |
| **P1** | MCP-Bench | ~50条（按50%通过率估） | 需搭28个MCP server | 高（真实API） |
| **P2** | LiveMCPBench | ~50条 | Docker + Embedding API | 高（真实API） |
| **P3** | τ-bench新域 | ~130条（按25%通过率估） | ✅ 已完成 | 中（mock数据） |
| **P4** | MCP-Universe | ~100条 | 需外部API key | 高（真实API） |
| **P5** | Toolathlon | ~40条（20轮长链） | 搭建32个软件 | 最高（真实软件） |
| **P6** | MCPEval | 取决于生成量 | pip install | 中 |

**注意：** 通过率估算基于当前模型能力（GPT-4o级别约30-50%），用更强模型可以提高。
