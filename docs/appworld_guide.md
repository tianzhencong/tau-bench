# AppWorld 训练数据生成指南

## 一、AppWorld 是什么

AppWorld（ACL 2024 最佳资源论文）是一个模拟真实数字生活的环境：
- **9个App**：Spotify、Amazon、Venmo、Gmail、Todoist、Splitwise、Phone、FileSystem、SimpleNote
- **457个API**：已经是 OpenAI function calling 格式
- **732个任务**：Easy(195) / Medium(258) / Hard(279)
- **~100个虚拟用户**：每个用户有完整的数字生活数据（订单、歌单、笔记、转账记录等）
- **真实数据库**：SQLite，不是mock数据
- **自带评估**：每个任务有 Python unit test，验证操作是否正确

项目主页：https://appworld.dev
GitHub：https://github.com/stonybrooknlp/appworld
论文：https://arxiv.org/abs/2407.18901

## 二、环境安装

```bash
# 建议用虚拟环境
python3 -m venv appworld_env
source appworld_env/bin/activate

# 安装 AppWorld
pip install appworld

# 安装内部组件（解压apps和tests源码）
appworld install

# 下载数据（732个任务 + 数据库，在当前目录下创建 data/ 文件夹）
# 注意：必须在你想工作的目录下执行
cd /path/to/your/workspace
appworld download data
```

安装完成后目录结构：
```
your_workspace/
├── data/
│   ├── api_docs/
│   │   ├── function_calling/   ← 457个API的OpenAI function calling定义
│   │   ├── openapi/            ← OpenAPI格式
│   │   └── standard/           ← 标准文档格式
│   ├── tasks/                  ← 732个任务
│   │   ├── 024c982_1/
│   │   │   ├── specs.json      ← 任务描述 + 用户信息
│   │   │   ├── dbs/            ← 该任务的数据库快照
│   │   │   └── ground_truth/   ← 评估代码 + 标准答案
│   │   └── ...
│   └── datasets/
│       ├── train.txt           ← 90个任务ID
│       ├── dev.txt             ← 57个任务ID
│       ├── test_normal.txt     ← 168个任务ID
│       └── test_challenge.txt  ← 417个任务ID
```

## 三、数据格式说明

### 任务定义 (specs.json)
```json
{
    "instruction": "Request $13 publicly on Venmo from my friend, Stacy, with a note, \"For yesterday's meal\".",
    "supervisor": {
        "first_name": "Joyce",
        "last_name": "Weaver",
        "email": "joyce-weav@gmail.com",
        "phone_number": "3155673041"
    },
    "datetime": "2023-05-18T12:00:00"
}
```

### API定义 (function_calling/*.json)
已经是 OpenAI tools 格式，直接可用：
```json
{
    "type": "function",
    "function": {
        "name": "venmo__create_payment_request",
        "description": "Send a payment request.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_email": {"type": "string", "format": "email"},
                "amount": {"type": "number", "exclusiveMinimum": 0.0},
                "description": {"type": "string", "default": ""},
                "private": {"type": "boolean", "default": false},
                "access_token": {"type": "string"}
            }
        }
    }
}
```

### 评估 (ground_truth/)
每个任务有：
- `evaluation.py`：Python unit test 代码
- `answer.json`：标准答案（`null` 表示不需要返回answer）
- `metadata.json`：难度、API调用次数等元信息

## 四、运行pipeline生成训练数据

### 4.1 把 run_appworld.py 复制到工作目录

```bash
# 从tau-bench仓库获取
cp /path/to/tau-bench/run_appworld.py /path/to/your/workspace/
```

### 4.2 运行单个任务（验证环境）

```bash
OPENAI_API_KEY="你的kimi key" \
OPENAI_API_BASE="https://api.moonshot.cn/v1" \
python run_appworld.py \
  --task_id 024c982_1 \
  --model kimi-k2.5 \
  --output results_appworld/
```

预期输出：
```
[1/1] Task: 024c982_1
  Tools: 94 APIs
  Turn 1: 🔧 supervisor__show_profile
  Turn 1: 🔧 supervisor__show_account_passwords
  Turn 2: 🔧 venmo__login
  Turn 3: 🔧 venmo__search_users
  Turn 4: 🔧 venmo__create_payment_request
  Turn 5: 💬 Final response
  ✅ 12 messages, 4 tool calls → saved
```

### 4.3 运行一个split的全部任务

```bash
# train split (90个任务)
OPENAI_API_KEY="你的key" \
OPENAI_API_BASE="https://api.moonshot.cn/v1" \
nohup python run_appworld.py \
  --split train \
  --model kimi-k2.5 \
  --output results_appworld/ \
  > appworld_train.log 2>&1 &

# 查看进度
tail -f appworld_train.log
```

### 4.4 输出格式

每行一个JSONL，直接是OpenAI训练格式：
```json
{
    "task_id": "024c982_1",
    "instruction": "Request $13 publicly on Venmo...",
    "user": "Joyce Weaver",
    "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "Request $13..."},
        {"role": "assistant", "reasoning_content": "思考过程...", "tool_calls": [
            {"id": "xxx", "function": {"name": "venmo__login", "arguments": "{...}"}, "type": "function"}
        ]},
        {"role": "tool", "tool_call_id": "xxx", "content": "{真实API返回数据}"},
        ...
    ],
    "tools": [...457个API定义...],
    "total_turns": 5
}
```

## 五、评估

### 5.1 自动评估（在pipeline中集成）

在 `run_appworld.py` 中，每个任务执行完后可以调用 AppWorld 自带的评估：

```python
from appworld import AppWorld

world = AppWorld(task_id="024c982_1", experiment_name="test")
# ... 执行API调用 ...
world.execute("apis.supervisor.complete_task(answer=None, status='success')")

result = world.evaluate()
d = result.to_dict()
# d['success'] = True/False
# d['num_tests'] = 7
# d['passes'] = [{requirement, label}, ...]
# d['failures'] = [{requirement, trace, label}, ...]
```

### 5.2 评估内容

AppWorld 的评估检查：
1. **answer是否正确**：查询类任务需要返回具体答案，操作类任务answer=null
2. **数据库状态是否正确**：检查哪些表被修改了，修改是否符合预期
3. **无附带损害**：确认没有意外修改其他数据

示例（Venmo转账任务，7个测试）：
```
✅ 数据库变更只涉及 venmo.Notification 和 venmo.PaymentRequest
✅ 新增了1条PaymentRequest，没有多余修改
✅ 收款人ID正确
✅ 金额正确（$13）
✅ 隐私设置正确（public）
✅ 备注正确（"For yesterday's meal"）
❌ answer格式不匹配（传了描述文字，应该传null）
```

### 5.3 注意事项

**answer的规则：**
- 操作类任务（下单、转账、发邮件）：`answer=None`
- 查询类任务（"我最贵的订单是什么？"）：`answer="具体答案"`
- 可以通过 `data/tasks/{task_id}/ground_truth/answer.json` 查看标准答案格式

**认证流程（每个任务都需要）：**
```
1. supervisor__show_profile()          → 获取用户信息
2. supervisor__show_account_passwords() → 获取各App密码
3. {app}__login(username, password)     → 获取access_token
4. 后续API调用都需要带 access_token
```

## 六、桥接层原理

AppWorld原生是Python代码执行模式，我们通过桥接层转成function calling模式：

```
kimi-k2.5 发出:
  tool_call: venmo__create_payment_request(user_email="xxx", amount=13, description="xxx")

桥接层转换为:
  world.execute("apis.venmo.create_payment_request(user_email='xxx', amount=13, description='xxx')")

AppWorld执行真实API，返回:
  {"message": "Payment request created.", "payment_request_id": 6097}

作为tool response返回给kimi-k2.5
```

桥接层代码在 `run_appworld.py` 的 `bridge_call()` 函数中，核心只有10行。

## 七、已知问题

1. **answer格式**：kimi-k2.5有时不知道该传 `null` 还是具体答案。可以在system prompt中提示，或者后处理时修正。

2. **工具数量过多**：457个API全部传给LLM会超token限制。当前pipeline按任务需要的App筛选工具（通常50-100个）。

3. **TPD限制**：kimi-k2.5每日token配额150万。中等难度任务约消耗3-5万token，一天大约能跑30-50个任务。

4. **kimi-k2.5 temperature**：必须设为1，不能设0。

## 八、训练数据筛选策略

跑完后按AppWorld评估结果筛选：

```python
import json

with open("results_appworld/appworld_kimi-k2.5_train.jsonl") as f:
    for line in f:
        traj = json.loads(line)
        if traj.get('evaluation', {}).get('success'):
            # ✅ 评估通过 → SFT正样本
            pass
        elif traj.get('evaluation', {}).get('num_tests'):
            pass_rate = len(traj['evaluation']['passes']) / traj['evaluation']['num_tests']
            if pass_rate >= 0.8:
                # 🟡 大部分通过 → 可用但需注意
                pass
            else:
                # ❌ 失败太多 → DPO负样本或丢弃
                pass
```

## 九、与τ-bench数据的配合

| 维度 | τ-bench（你的6个域） | AppWorld |
|------|-------------------|---------|
| 数据 | mock | 真实 |
| API数 | 15-20/域 | 457 |
| 任务 | 415 | 732 |
| 场景 | 客服/投资/医疗/办公 | 数字生活(9个App) |
| 用户交互 | 有user simulator多轮对话 | 无（直接执行任务） |
| thinking | ✅ reasoning_content | ✅ reasoning_content |
| 评估 | DB hash | Python unit test |

**建议混合训练：** τ-bench数据训练"多轮对话中的tool calling"，AppWorld数据训练"复杂任务规划+真实API使用"。
