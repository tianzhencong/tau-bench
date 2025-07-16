import random
from typing import Any, Callable, Dict, List, Type, Optional
from tau_bench.envs.tool import Tool
from tau_bench.types import Action, EnvResponse, EnvInfo, Task
from tau_bench.envs.retail.data import load_data
from tau_bench.envs.retail.tools import ALL_TOOLS
from tau_bench.envs.retail.rules import RULES
from tau_bench.envs.retail.wiki import WIKI

class RLToolEnv:
    def __init__(self, task_split: str = "test", task_index: Optional[int] = None):
        # 选择任务集
        if task_split == "test":
            from tau_bench.envs.retail.tasks_test import TASKS_TEST as tasks
        elif task_split == "train":
            from tau_bench.envs.retail.tasks_train import TASKS_TRAIN as tasks
        elif task_split == "dev":
            from tau_bench.envs.retail.tasks_dev import TASKS_DEV as tasks
        else:
            raise ValueError(f"Unknown task split: {task_split}")
        self.tasks = tasks
        self.task_index = task_index if task_index is not None else random.randint(0, len(self.tasks) - 1)
        self.task: Task = self.tasks[self.task_index]
        self.data_load_func = load_data
        self.data = self.data_load_func()
        self.tools_map: Dict[str, Type[Tool]] = {
            tool.get_info()["function"]["name"]: tool for tool in ALL_TOOLS
        }
        self.terminate_tools = ["transfer_to_human_agents"]
        self.actions: List[Action] = []
        self.done = False
        self.info = EnvInfo(task=self.task)

    def reset(self, task_index: Optional[int] = None) -> Dict[str, Any]:
        if task_index is not None:
            self.task_index = task_index
        else:
            self.task_index = random.randint(0, len(self.tasks) - 1)
        self.task = self.tasks[self.task_index]
        self.data = self.data_load_func()
        self.actions = []
        self.done = False
        self.info = EnvInfo(task=self.task)
        # 返回初始观测（可自定义）
        return {"observation": self.task.instruction, "task": self.task}

    def step(self, action: Action) -> EnvResponse:
        if self.done:
            raise RuntimeError("Episode is done. Please reset the environment.")
        self.actions.append(action)
        info = EnvInfo(task=self.task)
        reward = 0.0
        done = False
        if action.name in self.tools_map:
            try:
                observation = self.tools_map[action.name].invoke(data=self.data, **action.kwargs)
            except Exception as e:
                observation = f"Error: {e}"
            info.source = action.name
            if action.name in self.terminate_tools:
                done = True
        else:
            observation = f"Unknown action {action.name}"
            info.source = action.name
            done = True
            reward = -1.0
        # 这里reward和done逻辑可根据RL任务自定义
        self.done = done
        return EnvResponse(observation=observation, reward=reward, done=done, info=info)