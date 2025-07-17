import os
import sys
import json
import logging
from typing import Any, Dict, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tau_bench.run import run as tau_bench_run
from tau_bench.types import RunConfig

logger = logging.getLogger("eval_taubench")
logging.basicConfig(level=logging.INFO)

class TauBenchEnv:
    """
    适配verl风格的TauBench环境，支持retail和airline两个领域。
    """
    def __init__(self, domain: str = "retail", **kwargs):
        assert domain in ["retail", "airline"], "domain must be 'retail' or 'airline'"
        self.domain = domain
        self.kwargs = kwargs
        self.env = None

    def reset(self, *args, **kwargs):
        # 这里直接调用tau_bench的get_env逻辑
        from tau_bench.envs import get_env
        self.env = get_env(self.domain, **self.kwargs)
        return self.env

    def step(self, action):
        # 这里假设action为tau_bench的Action对象
        # 具体实现可根据verl的Action结构适配
        raise NotImplementedError("step方法请根据verl的采样流程适配")

class TauBenchDataSource:
    """
    适配verl风格的数据源，支持retail和airline任务的批量加载。
    """
    def __init__(self, domain: str = "retail", task_split: str = "test"):
        self.domain = domain
        self.task_split = task_split
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        # 直接调用tau_bench的环境加载任务
        from tau_bench.envs import get_env
        env = get_env(self.domain, task_split=self.task_split)
        return env.tasks

    def get_next_sample_batch(self, batch_size: int = 1):
        # 返回任务的子集
        for i in range(0, len(self.tasks), batch_size):
            yield self.tasks[i:i+batch_size]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="TauBench 多轮采样评估 (verl风格)")
    parser.add_argument("--domain", type=str, choices=["retail", "airline"], default="retail", help="评测领域")
    parser.add_argument("--model", type=str, required=True, help="评测模型名称")
    parser.add_argument("--model_provider", type=str, required=True, help="模型provider")
    parser.add_argument("--user_model_provider", type=str, default="openai", help="用户模型provider")
    parser.add_argument("--user_model", type=str, default="gpt-4o", help="用户模型名称")
    parser.add_argument("--num_trials", type=int, default=1, help="每个任务采样次数")
    parser.add_argument("--task_split", type=str, choices=["train", "test", "dev"], default="test", help="任务集划分")
    parser.add_argument("--start_index", type=int, default=0, help="起始任务索引")
    parser.add_argument("--end_index", type=int, default=-1, help="结束任务索引")
    parser.add_argument("--log_dir", type=str, default="results", help="日志保存目录")
    parser.add_argument("--max_concurrency", type=int, default=1, help="最大并发数")
    parser.add_argument("--seed", type=int, default=10, help="随机种子")
    parser.add_argument("--shuffle", type=int, default=0, help="是否打乱任务顺序")
    parser.add_argument("--user_strategy", type=str, default="llm", help="用户策略")
    parser.add_argument("--agent_strategy", type=str, default="tool-calling", help="agent策略")
    args = parser.parse_args()

    config = RunConfig(
        model_provider=args.model_provider,
        user_model_provider=args.user_model_provider,
        model=args.model,
        user_model=args.user_model,
        num_trials=args.num_trials,
        env=args.domain,
        agent_strategy=args.agent_strategy,
        task_split=args.task_split,
        start_index=args.start_index,
        end_index=args.end_index,
        log_dir=args.log_dir,
        max_concurrency=args.max_concurrency,
        seed=args.seed,
        shuffle=args.shuffle,
        user_strategy=args.user_strategy,
    )
    logger.info(f"TauBench评测开始，领域: {args.domain}, 任务集: {args.task_split}, 模型: {args.model}")
    results = tau_bench_run(config)
    logger.info(f"TauBench评测完成，结果数: {len(results)}")

if __name__ == "__main__":
    main()