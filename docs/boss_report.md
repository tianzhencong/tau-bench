# Tool Calling 数据集调研报告

## 一、调研结论（先说结论）

**10个数据集中，5个和我们的tool calling优化目标直接相关，5个不相关。** 其中最有价值的是 **AppWorld**——我们已经完成了pipeline搭建并产出了191条高质量SFT训练数据。

### 关键发现

1. **当前最强模型在tool calling上仍有显著短板**：GPT-5在MCP-Bench上仅74.9%，kimi-k2得分62.9%，主要弱在"依赖感知"(44.8%)和"并行效率"(30.7%)

2. **τ-bench被新benchmark明确指出局限性**：MCP-Bench论文Table 1直接批评τ-bench——"仅2个领域、28个工具，不支持模糊指令、跨域编排、信息Grounding"

3. **AppWorld是当前最适合我们的数据源**：732个任务、457个API、真实数据、自带评估、pip install即可，不需要Docker/外部API key

---

## 二、5个直接相关的数据集

### 2.1 AppWorld ⭐⭐⭐⭐⭐（已落地）

| 项目 | 内容 |
|------|------|
| 来源 | ACL 2024 最佳资源论文 |
| 规模 | 9个App、457个API、732个任务 |
| 特点 | 真实SQLite数据库、自带Python unit test评估 |
| 场景 | Spotify/Amazon/Venmo/Gmail/Todoist等日常App |
| 我们做了什么 | 搭建了function calling桥接层，用KaLM-DeepSeek-V3.2跑完4个split(433条)，筛选出191条高质量SFT数据 |
| 评估通过率 | 24.7%完全通过，43.9%业务逻辑正确（排除answer格式问题） |
| 下一步 | 用更强的模型跑可以提高通过率；提高max_turns从20到30 |

**核心价值：** 真实数据 + 真实评估 + 多App协作，是目前唯一产出了可用训练数据的外部数据源。

### 2.2 MCP-Bench ⭐⭐⭐⭐⭐

| 项目 | 内容 |
|------|------|
| 来源 | Accenture（NeurIPS 2025 Workshop） |
| 规模 | 28个MCP server、250个工具、104个任务 |
| 论文关键点 | 任务自动合成pipeline（依赖链发现→质量过滤→模糊化）；每个任务附带10个干扰server |
| kimi-k2表现 | 总分0.629（第12/20），dependency awareness 0.448（弱项），parallelism 0.307（最弱项） |
| 数据可用性 | 有任务定义和工具配置，没有现成轨迹 |
| 与我们的关系 | 指明了优化方向：依赖感知 + 并行效率 + 模糊指令理解 |

**核心价值：** 明确告诉我们模型的薄弱点在哪里——不是基础tool calling（>95%），而是规划能力。

### 2.3 LiveMCPBench ⭐⭐⭐⭐⭐

| 项目 | 内容 |
|------|------|
| 来源 | 中科院信工所（ICLR 2026提交） |
| 规模 | 70个MCP server、527个工具、95个任务 |
| 特点 | 最大工具池；有Claude-Sonnet-4的完整对话轨迹 |
| 关键发现 | "检索错误占所有失败的近一半"——大工具池中的工具发现是最大瓶颈 |
| 数据可用性 | 有Docker镜像和完整轨迹数据 |
| 轨迹质量 | 已有轨迹含大量试错/重试噪音，不建议直接用 |

**核心价值：** 揭示了"工具发现/路由"是大工具池场景的核心挑战。我们基于它的任务构建了mock版本并改进了数据质量。

### 2.4 Toolathlon ⭐⭐⭐⭐⭐

| 项目 | 内容 |
|------|------|
| 来源 | 香港科技大学（ICLR 2026） |
| 规模 | 32个真实软件、604个工具、108个手工标注任务 |
| 特点 | 平均20轮tool calling（最长）；真实软件初始状态 |
| 最强模型 | Claude-4.5-Sonnet仅38.6% |
| 数据可用性 | GitHub公开，需搭建32个软件环境 |

**核心价值：** 20轮长horizon是我们目前训练数据最缺的维度。但搭建成本高。

### 2.5 MCP-Universe ⭐⭐⭐⭐

| 项目 | 内容 |
|------|------|
| 来源 | Salesforce（NeurIPS 2025） |
| 规模 | 11个MCP server、231个任务 |
| 特点 | 首个综合MCP benchmark；3种evaluator（格式/静态/动态） |
| 最强模型 | GPT-5仅43.7% |

---

## 三、5个不相关的数据集

| 数据集 | 为什么不相关 |
|--------|------------|
| **CVE-Bench** | 安全漏洞利用，agent写攻击代码，不是function calling |
| **BountyBench** | Bug bounty（检测/利用/修补），终端命令操作，不是function calling |
| **SEC-bench** | 安全工程（PoC生成+漏洞修补），代码agent任务 |
| **App-Bench** | 从自然语言生成完整Web应用，代码生成任务 |
| **Design2Code** | 网页截图转HTML/CSS，多模态代码生成，与tool calling无关 |

这5个如果后续做coding agent可以关注，当前不是优先级。

---

## 四、我们已经做了什么

### 4.1 构建了6个τ-bench新领域（510个任务）

为了不在τ-bench原有的retail/airline上过拟合，我们构建了：

| 域 | 任务数 | 对标 |
|---|---|---|
| Course（课程注册） | 77 | Retail结构（嵌套数据） |
| Investment（投资组合） | 63 | 最复杂（4层嵌套+跨账户） |
| Travel（旅行社） | 75 | Airline失败模式 |
| Healthcare（医疗预约） | 100 | Airline失败模式 |
| Workflow（办公自动化） | 100 | MCP-Atlas（工具编排） |
| MCP Bench（工具路由） | 95 | LiveMCPBench（大工具池选择） |

### 4.2 AppWorld pipeline（191条SFT数据）

- 搭建了function calling桥接层：kimi → bridge → AppWorld真实API → 真实数据返回
- 用KaLM-DeepSeek-V3.2跑完全部4个split（433条轨迹）
- 筛选出191条业务逻辑正确的轨迹
- 转换为标准OpenAI SFT JSONL格式（带reasoning_content）
- 平均每条28.7条消息、12.9次tool call

### 4.3 能力覆盖分析

| 能力 | 覆盖状态 |
|------|---------|
| 基础tool calling | ✅ 充分 |
| 多步骤链式调用 | ✅ 充分 |
| 跨App协作 | ✅ 覆盖（AppWorld） |
| 工具编排（数据流传递） | ✅ 覆盖（Workflow域） |
| 策略合规 | ✅ 覆盖（τ-bench设计） |
| 大工具池选择 | ❌ 缺失 |
| 模糊指令理解 | ❌ 缺失 |
| 并行工具调用 | ❌ 缺失 |
| 错误恢复 | ❌ 缺失 |
| 长horizon（20+步） | 🟡 不足 |

---

## 五、下一步建议

### 短期（1-2周）
1. **用更强模型跑AppWorld**：当前24.7%通过率是KaLM-DeepSeek-V3.2的上限，用GPT-4o/Claude跑可以获得更多高质量轨迹
2. **跑τ-bench 6个域的全量轨迹**：510个任务还没生成轨迹
3. **强化3个关键缺失能力的训练数据**：大工具池选择、模糊指令、并行调用

### 中期（2-4周）
4. **搭建LiveMCPBench真实环境**（Docker，需要Embedding模型）收集527工具池的轨迹
5. **评估Toolathlon**的搭建成本，如果可行可以获取20轮长horizon数据

### 核心指标
- 目标：提升kimi在MCP-Bench上的dependency awareness（44.8%→60%+）和parallelism（30.7%→50%+）
- 数据量目标：500+条高质量SFT轨迹（当前191条）

---

## 六、参考链接

| 资源 | 链接 |
|------|------|
| MCP-Bench论文 | https://arxiv.org/abs/2508.20453 |
| MCP-Bench代码 | https://github.com/Accenture/mcp-bench |
| LiveMCPBench论文 | https://arxiv.org/abs/2508.01780 |
| LiveMCPBench代码 | https://github.com/icip-cas/LiveMCPBench |
| Toolathlon论文 | https://arxiv.org/abs/2510.25726 |
| MCP-Universe论文 | https://arxiv.org/abs/2508.14704 |
| AppWorld论文 | https://arxiv.org/abs/2407.18901 |
| AppWorld代码 | https://github.com/stonybrooknlp/appworld |
| 我们的代码仓库 | GitHub tau-bench分支 cursor/development-environment-setup-a268 |
