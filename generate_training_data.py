# Copyright Sierra
# Training data generation script for tau-bench style domains
#
# This script generates training conversation trajectories by:
# 1. Programmatically executing ground-truth tool calls against the environment
# 2. Generating natural conversation flows around those tool calls
# 3. Outputting in the format needed for LLM fine-tuning
#
# Usage:
#   # Generate gold trajectories from tasks (requires API key for user simulation)
#   python generate_training_data.py --env hotel --output training_data/hotel.jsonl --mode gold
#
#   # Generate template-based trajectories (no API key needed)
#   python generate_training_data.py --env hotel --output training_data/hotel_templates.jsonl --mode template
#
#   # Generate with specific task IDs
#   python generate_training_data.py --env hotel --output training_data/hotel.jsonl --mode template --task-ids 0 1 2

import argparse
import json
import os
import copy
from typing import Any, Dict, List, Optional

from tau_bench.types import Action, Task, RESPOND_ACTION_NAME


def load_env_components(env_name: str):
    """Load environment components (data, tools, tasks, wiki) for a given domain."""
    if env_name == "hotel":
        from tau_bench.envs.hotel.data import load_data
        from tau_bench.envs.hotel.tools import ALL_TOOLS
        from tau_bench.envs.hotel.tasks_v2 import TASKS
        from tau_bench.envs.hotel.wiki import WIKI
    elif env_name == "airline":
        from tau_bench.envs.airline.data import load_data
        from tau_bench.envs.airline.tools import ALL_TOOLS
        from tau_bench.envs.airline.tasks_test import TASKS
        from tau_bench.envs.airline.wiki import WIKI
    elif env_name == "retail":
        from tau_bench.envs.retail.data import load_data
        from tau_bench.envs.retail.tools import ALL_TOOLS
        from tau_bench.envs.retail.tasks_test import TASKS_TEST as TASKS
        from tau_bench.envs.retail.wiki import WIKI
    else:
        raise ValueError(f"Unknown environment: {env_name}")

    return load_data, ALL_TOOLS, TASKS, WIKI


def generate_template_trajectory(
    task: Task,
    task_id: int,
    data_load_func,
    tools_map: Dict[str, Any],
    tools_info: List[Dict[str, Any]],
    wiki: str,
) -> Dict[str, Any]:
    """Generate a template-based training trajectory without LLM calls.

    This creates a structured conversation that demonstrates the correct
    sequence of tool calls and responses for a given task.
    """
    data = data_load_func()
    messages = [{"role": "system", "content": wiki}]

    initial_msg = _generate_user_opening(task)
    messages.append({"role": "user", "content": initial_msg})

    for i, action in enumerate(task.actions):
        if action.name == RESPOND_ACTION_NAME:
            messages.append({
                "role": "assistant",
                "content": action.kwargs.get("content", ""),
            })
            continue

        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": f"call_{task_id}_{i}",
                "type": "function",
                "function": {
                    "name": action.name,
                    "arguments": json.dumps(action.kwargs),
                },
            }],
        })

        try:
            tool_cls = tools_map[action.name]
            result = tool_cls.invoke(data=data, **action.kwargs)
        except Exception as e:
            result = f"Error: {e}"

        messages.append({
            "role": "tool",
            "tool_call_id": f"call_{task_id}_{i}",
            "name": action.name,
            "content": result,
        })

    if task.outputs:
        output_msg = "Based on the information gathered: " + ", ".join(task.outputs)
        messages.append({"role": "assistant", "content": output_msg})

    return {
        "task_id": task_id,
        "user_id": task.user_id,
        "instruction": task.instruction,
        "messages": messages,
        "tools": tools_info,
        "ground_truth_actions": [a.model_dump() for a in task.actions],
        "ground_truth_outputs": task.outputs,
        "num_actions": len(task.actions),
    }


def _generate_user_opening(task: Task) -> str:
    """Generate a natural opening message based on the task instruction."""
    instruction = task.instruction
    if "cancel" in instruction.lower():
        return "Hi, I need help cancelling a reservation."
    elif "book" in instruction.lower():
        return "Hello, I'd like to book a hotel room."
    elif "upgrade" in instruction.lower() or "modify" in instruction.lower() or "change" in instruction.lower():
        return "Hi, I need to make some changes to my reservation."
    elif "complain" in instruction.lower() or "compensation" in instruction.lower() or "upset" in instruction.lower():
        return "I need to speak with someone about a problem with my stay."
    elif "check" in instruction.lower():
        return "Hi, I'd like to check on a reservation."
    else:
        return "Hello, I need some help with my hotel booking."


def generate_gold_trajectory(
    task: Task,
    task_id: int,
    env,
    model: str = "gpt-4o",
    provider: str = "openai",
) -> Optional[Dict[str, Any]]:
    """Generate a gold trajectory by running the agent through the environment.

    This requires an LLM API key. The agent's tool calls are captured
    as training data, but only if the task succeeds (reward=1.0).
    """
    from tau_bench.agents.tool_calling_agent import ToolCallingAgent

    agent = ToolCallingAgent(
        tools_info=env.tools_info,
        wiki=env.wiki,
        model=model,
        provider=provider,
        temperature=0.0,
    )

    result = agent.solve(env, task_index=task_id, max_num_steps=30)

    return {
        "task_id": task_id,
        "user_id": task.user_id,
        "instruction": task.instruction,
        "messages": result.messages,
        "tools": env.tools_info,
        "reward": result.reward,
        "ground_truth_actions": [a.model_dump() for a in task.actions],
        "ground_truth_outputs": task.outputs,
        "total_cost": result.total_cost,
    }


def generate_synthetic_tasks(
    base_tasks: List[Task],
    data_load_func,
    tools_map: Dict[str, Any],
    num_variations: int = 3,
) -> List[Task]:
    """Generate synthetic task variations by modifying existing tasks.

    This helps increase training data volume by creating variations
    with different users, parameters, and conditions.
    """
    data = data_load_func()
    users = data.get("users", {})
    synthetic = []

    for task in base_tasks:
        if len(task.actions) == 0:
            for _ in range(num_variations):
                variation = Task(
                    user_id=task.user_id,
                    instruction=_vary_instruction(task.instruction),
                    actions=[],
                    outputs=[],
                )
                synthetic.append(variation)
    return synthetic


def _vary_instruction(instruction: str) -> str:
    """Create a minor variation of an instruction for data augmentation."""
    import random
    variations = [
        ("You are calm and cooperative.", "You are polite but firm."),
        ("You are reactive", "You don't volunteer extra information"),
        ("Be persistent.", "Don't give up easily."),
        ("insist", "be firm about"),
        ("You are in a hurry.", "You'd like this done quickly."),
    ]
    result = instruction
    for old, new in variations:
        if old.lower() in result.lower() and random.random() < 0.5:
            result = result.replace(old, new)
    return result


def main():
    parser = argparse.ArgumentParser(description="Generate training data for tau-bench")
    parser.add_argument("--env", type=str, required=True, choices=["hotel", "airline", "retail"])
    parser.add_argument("--output", type=str, required=True, help="Output JSONL file path")
    parser.add_argument("--mode", type=str, default="template", choices=["template", "gold"],
                       help="Generation mode: template (no API needed) or gold (requires API)")
    parser.add_argument("--task-ids", type=int, nargs="+", help="Specific task IDs to generate")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Model for gold mode")
    parser.add_argument("--model-provider", type=str, default="openai", help="Provider for gold mode")
    args = parser.parse_args()

    data_load_func, all_tools, tasks, wiki = load_env_components(args.env)

    tools_map = {tool.get_info()["function"]["name"]: tool for tool in all_tools}
    tools_info = [tool.get_info() for tool in all_tools]

    task_ids = args.task_ids if args.task_ids else list(range(len(tasks)))

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)

    generated = 0
    with open(args.output, "w") as f:
        for tid in task_ids:
            if tid >= len(tasks):
                print(f"Warning: task ID {tid} out of range, skipping")
                continue

            task = tasks[tid]

            if args.mode == "template":
                traj = generate_template_trajectory(
                    task=task,
                    task_id=tid,
                    data_load_func=data_load_func,
                    tools_map=tools_map,
                    tools_info=tools_info,
                    wiki=wiki,
                )
            elif args.mode == "gold":
                from tau_bench.envs.hotel.env import MockHotelDomainEnv
                env = MockHotelDomainEnv(
                    user_strategy="llm",
                    user_model=args.model,
                    user_provider=args.model_provider,
                )
                traj = generate_gold_trajectory(
                    task=task,
                    task_id=tid,
                    env=env,
                    model=args.model,
                    provider=args.model_provider,
                )
            else:
                raise ValueError(f"Unknown mode: {args.mode}")

            if traj:
                f.write(json.dumps(traj) + "\n")
                generated += 1

    print(f"Generated {generated} trajectories -> {args.output}")
    print(f"  Environment: {args.env}")
    print(f"  Mode: {args.mode}")
    print(f"  Task IDs: {task_ids}")


if __name__ == "__main__":
    main()
