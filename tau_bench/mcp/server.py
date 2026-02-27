from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from tau_bench.envs import get_env
from tau_bench.envs.base import Env
from tau_bench.types import Action, Task, RESPOND_ACTION_NAME

DEFAULT_INSTRUCTIONS = (
    "该服务器提供工具，便于智能体通过 Model Context Protocol 与 τ-bench 的航空与零售环境交互。\n"
    "典型流程：1) 使用 create_environment 创建任务并获取初始观测；"
    "2) 依据返回的工具定义调用 step_environment 执行动作（包括 respond）；"
    "3) 完成任务时，请在 respond 的 content 中包含 '###STOP###' 以触发评分；"
    "4) 如需重新开始，调用 reset_environment 或 create_environment。"
)

_RESPOND_ACTION_SCHEMA: Dict[str, Any] = {
    "name": RESPOND_ACTION_NAME,
    "description": "向用户模拟器发送自然语言回复，必要时附带 '###STOP###' 结束会话。",
    "parameters": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "要发送给用户模拟器的消息。结束任务时必须包含 '###STOP###'。",
            }
        },
        "required": ["content"],
    },
}


@dataclass
class EnvironmentState:
    handle: str
    env: Env
    env_name: Literal["retail", "airline"]
    task_split: Literal["train", "test", "dev"]
    task_index: int
    task: Task
    tools_info: List[Dict[str, Any]]
    wiki: str
    rules: List[str]
    user_strategy: str
    user_model: str
    user_provider: Optional[str]
    done: bool = False
    turn_count: int = 0
    last_observation: str = ""
    history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TauBenchSessionStore:
    environments: Dict[str, EnvironmentState] = field(default_factory=dict)


class EnvironmentInfo(BaseModel):
    handle: str
    env: Literal["retail", "airline"]
    task_split: Literal["train", "test", "dev"]
    task_index: int
    instruction: str
    tools: List[Dict[str, Any]]
    respond_action: Dict[str, Any]
    wiki: str
    rules: List[str]
    task: Dict[str, Any]
    user_strategy: str
    user_model: str
    user_model_provider: Optional[str] = Field(default=None)


class CreateEnvironmentResult(EnvironmentInfo):
    initial_observation: str
    source: str = Field(default="user")


class ResetEnvironmentResult(EnvironmentInfo):
    observation: str
    source: str = Field(default="user")


class StepEnvironmentResult(BaseModel):
    handle: str
    turn: int
    observation: str
    source: str
    reward: float
    done: bool
    info: Dict[str, Any]


class EnvironmentMetadata(BaseModel):
    handle: str
    env: Literal["retail", "airline"]
    task_split: Literal["train", "test", "dev"]
    task_index: int
    done: bool
    turn_count: int
    user_strategy: str
    user_model: str
    user_model_provider: Optional[str] = Field(default=None)
    last_observation: str


class ListEnvironmentsResult(BaseModel):
    count: int
    environments: List[EnvironmentMetadata] = Field(default_factory=list)


class HistoryItem(BaseModel):
    turn: int
    type: Literal["action", "observation"]
    name: Optional[str] = None
    kwargs: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    content: Optional[str] = None
    reward: Optional[float] = None
    done: Optional[bool] = None


class EnvironmentHistoryResult(BaseModel):
    handle: str
    history: List[HistoryItem]


class CloseEnvironmentResult(BaseModel):
    handle: str
    removed: bool


def _get_session_store(ctx: Context) -> TauBenchSessionStore:
    session = ctx.session
    store = getattr(session, "_tau_bench_state", None)
    if store is None:
        store = TauBenchSessionStore()
        setattr(session, "_tau_bench_state", store)
    return store


def _require_environment(store: TauBenchSessionStore, handle: str) -> EnvironmentState:
    try:
        return store.environments[handle]
    except KeyError as exc:
        raise ValueError(f"未知的环境句柄 '{handle}'") from exc


def _serialize_task(task: Task) -> Dict[str, Any]:
    return task.model_dump()


def _serialize_env_info(info) -> Dict[str, Any]:
    data = info.model_dump()
    if info.reward_info is not None:
        data["reward_info"] = info.reward_info.model_dump()
    if info.task is not None:
        data["task"] = info.task.model_dump()
    return data


def _make_action_history(turn: int, action: Action) -> Dict[str, Any]:
    return {
        "turn": turn,
        "type": "action",
        "name": action.name,
        "kwargs": action.kwargs,
    }


def _make_observation_history(
    turn: int,
    source: str,
    content: str,
    reward: Optional[float],
    done: bool,
) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "turn": turn,
        "type": "observation",
        "source": source,
        "content": content,
        "done": done,
    }
    if reward is not None:
        entry["reward"] = reward
    return entry


def create_server(
    *,
    instructions: Optional[str] = None,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> FastMCP:
    server = FastMCP(
        name="tau-bench",
        instructions=instructions or DEFAULT_INSTRUCTIONS,
        host=host,
        port=port,
    )

    @server.tool(description="创建一个新的τ-bench任务并返回初始观测")
    async def create_environment(
        env: Literal["retail", "airline"],
        task_split: Literal["train", "test", "dev"] = "test",
        task_id: Optional[int] = None,
        user_strategy: str = "llm",
        user_model: str = "gpt-4o",
        user_model_provider: Optional[str] = None,
        ctx: Context,
    ) -> CreateEnvironmentResult:
        store = _get_session_store(ctx)

        env_obj = get_env(
            env,
            user_strategy=user_strategy,
            user_model=user_model,
            task_split=task_split,
            user_provider=user_model_provider,
        )
        total_tasks = len(env_obj.tasks)
        if total_tasks == 0:
            raise ValueError(f"环境 {env} 在分割 {task_split} 下没有可用任务")

        if task_id is None:
            task_index = random.randrange(total_tasks)
        else:
            if task_id < 0 or task_id >= total_tasks:
                raise ValueError(
                    f"task_id {task_id} 超出范围，合法范围为 [0, {total_tasks - 1}]"
                )
            task_index = task_id

        reset_response = env_obj.reset(task_index=task_index)
        handle = uuid4().hex

        state = EnvironmentState(
            handle=handle,
            env=env_obj,
            env_name=env,
            task_split=task_split,
            task_index=task_index,
            task=reset_response.info.task,
            tools_info=env_obj.tools_info,
            wiki=env_obj.wiki,
            rules=env_obj.rules,
            user_strategy=user_strategy,
            user_model=user_model,
            user_provider=user_model_provider,
            done=False,
            turn_count=0,
            last_observation=reset_response.observation,
            history=[
                _make_observation_history(
                    turn=0,
                    source=reset_response.info.source or "user",
                    content=reset_response.observation,
                    reward=None,
                    done=False,
                )
            ],
        )
        store.environments[handle] = state

        return CreateEnvironmentResult(
            handle=handle,
            env=env,
            task_split=task_split,
            task_index=task_index,
            instruction=state.task.instruction,
            tools=state.tools_info,
            respond_action=_RESPOND_ACTION_SCHEMA,
            wiki=state.wiki,
            rules=state.rules,
            task=_serialize_task(state.task),
            user_strategy=state.user_strategy,
            user_model=state.user_model,
            user_model_provider=state.user_provider,
            initial_observation=reset_response.observation,
            source=reset_response.info.source or "user",
        )

    @server.tool(description="对指定环境执行动作或工具调用")
    async def step_environment(
        handle: str,
        action_name: str,
        arguments: Dict[str, Any],
        ctx: Context,
    ) -> StepEnvironmentResult:
        store = _get_session_store(ctx)
        state = _require_environment(store, handle)

        if state.done:
            raise ValueError("该环境已完成执行，请先 reset 或创建新环境")

        action = Action(name=action_name, kwargs=arguments)
        turn = state.turn_count + 1
        state.history.append(_make_action_history(turn, action))

        response = state.env.step(action)
        info_dict = _serialize_env_info(response.info)
        source = info_dict.get("source") or action.name

        state.history.append(
            _make_observation_history(
                turn=turn,
                source=source,
                content=response.observation,
                reward=response.reward,
                done=response.done,
            )
        )
        state.last_observation = response.observation
        state.done = response.done
        state.turn_count = turn

        return StepEnvironmentResult(
            handle=handle,
            turn=turn,
            observation=response.observation,
            source=source,
            reward=response.reward,
            done=response.done,
            info=info_dict,
        )

    @server.tool(description="重置已存在的环境，可指定新的 task_id")
    async def reset_environment(
        handle: str,
        task_id: Optional[int] = None,
        ctx: Context,
    ) -> ResetEnvironmentResult:
        store = _get_session_store(ctx)
        state = _require_environment(store, handle)

        total_tasks = len(state.env.tasks)
        if total_tasks == 0:
            raise ValueError("当前环境没有可用任务")

        if task_id is not None:
            if task_id < 0 or task_id >= total_tasks:
                raise ValueError(
                    f"task_id {task_id} 超出范围，合法范围为 [0, {total_tasks - 1}]"
                )
            state.task_index = task_id

        reset_response = state.env.reset(task_index=state.task_index)
        state.task = reset_response.info.task
        state.done = False
        state.turn_count = 0
        state.last_observation = reset_response.observation
        state.history = [
            _make_observation_history(
                turn=0,
                source=reset_response.info.source or "user",
                content=reset_response.observation,
                reward=None,
                done=False,
            )
        ]

        return ResetEnvironmentResult(
            handle=handle,
            env=state.env_name,
            task_split=state.task_split,
            task_index=state.task_index,
            instruction=state.task.instruction,
            tools=state.tools_info,
            respond_action=_RESPOND_ACTION_SCHEMA,
            wiki=state.wiki,
            rules=state.rules,
            task=_serialize_task(state.task),
            user_strategy=state.user_strategy,
            user_model=state.user_model,
            user_model_provider=state.user_provider,
            observation=reset_response.observation,
            source=reset_response.info.source or "user",
        )

    @server.tool(description="获取指定环境的静态信息")
    async def describe_environment(
        handle: str,
        ctx: Context,
    ) -> EnvironmentInfo:
        store = _get_session_store(ctx)
        state = _require_environment(store, handle)

        return EnvironmentInfo(
            handle=handle,
            env=state.env_name,
            task_split=state.task_split,
            task_index=state.task_index,
            instruction=state.task.instruction,
            tools=state.tools_info,
            respond_action=_RESPOND_ACTION_SCHEMA,
            wiki=state.wiki,
            rules=state.rules,
            task=_serialize_task(state.task),
            user_strategy=state.user_strategy,
            user_model=state.user_model,
            user_model_provider=state.user_provider,
        )

    @server.tool(description="列出当前会话中所有已创建但尚未关闭的环境")
    async def list_environments(ctx: Context) -> ListEnvironmentsResult:
        store = _get_session_store(ctx)

        environments = [
            EnvironmentMetadata(
                handle=handle,
                env=state.env_name,
                task_split=state.task_split,
                task_index=state.task_index,
                done=state.done,
                turn_count=state.turn_count,
                user_strategy=state.user_strategy,
                user_model=state.user_model,
                user_model_provider=state.user_provider,
                last_observation=state.last_observation,
            )
            for handle, state in store.environments.items()
        ]

        return ListEnvironmentsResult(count=len(environments), environments=environments)

    @server.tool(description="返回指定环境的交互历史")
    async def get_environment_history(
        handle: str,
        ctx: Context,
    ) -> EnvironmentHistoryResult:
        store = _get_session_store(ctx)
        state = _require_environment(store, handle)

        history = [HistoryItem.model_validate(entry) for entry in state.history]
        return EnvironmentHistoryResult(handle=handle, history=history)

    @server.tool(description="关闭并移除指定环境")
    async def close_environment(
        handle: str,
        ctx: Context,
    ) -> CloseEnvironmentResult:
        store = _get_session_store(ctx)
        _require_environment(store, handle)
        del store.environments[handle]
        return CloseEnvironmentResult(handle=handle, removed=True)

    return server


def main() -> None:
    parser = argparse.ArgumentParser(description="运行 τ-bench MCP 服务器")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="通信方式，默认为 stdio",
    )
    parser.add_argument("--host", default="127.0.0.1", help="服务器主机名（SSE/HTTP 模式使用）")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口（SSE/HTTP 模式使用）")
    parser.add_argument("--mount-path", default="/tau-bench", help="SSE 模式下的挂载路径")
    parser.add_argument("--instructions", help="覆盖默认的服务器说明信息")

    args = parser.parse_args()

    server = create_server(instructions=args.instructions, host=args.host, port=args.port)
    if args.transport == "sse":
        server.run(transport="sse", mount_path=args.mount_path)
    else:
        server.run(transport=args.transport)


if __name__ == "__main__":
    main()


__all__ = ["create_server", "main"]
