# Copyright Sierra
# AppWorld → OpenAI Training Data Pipeline
#
# Generates high-quality tool calling training data from AppWorld's
# 732 tasks + 457 APIs + real data environment.
#
# Prerequisites:
#   pip install appworld
#   appworld install
#   appworld download data  (run from the working directory)
#
# Usage:
#   python run_appworld.py --task_id 024c982_1 --output results_appworld/
#   python run_appworld.py --split train --output results_appworld/
#   python run_appworld.py --split dev --output results_appworld/

import json
import os
import time
import argparse
from pathlib import Path

from openai import OpenAI
from appworld import AppWorld


def load_tools_for_task(task_id: str, data_dir: str = "data") -> list:
    """Load relevant API tools for a task.
    
    Strategy: load supervisor + api_docs always, then infer needed apps
    from the task's DB files or load all apps.
    """
    api_dir = f"{data_dir}/api_docs/function_calling"
    
    # Always include supervisor and api_docs
    must_have = ["supervisor", "api_docs"]
    
    # Check which apps the task might need from its DB files
    task_dbs_dir = f"{data_dir}/tasks/{task_id}/dbs"
    if os.path.exists(task_dbs_dir):
        db_apps = [f.replace('.jsonl', '') for f in os.listdir(task_dbs_dir) if f.endswith('.jsonl')]
    else:
        db_apps = []
    
    # Map DB names to API doc names
    app_mapping = {
        'gmail': 'gmail', 'phone': 'phone', 'spotify': 'spotify',
        'amazon': 'amazon', 'venmo': 'venmo', 'todoist': 'todoist',
        'splitwise': 'splitwise', 'simple_note': 'simple_note',
        'file_system': 'file_system', 'supervisor': 'supervisor',
        'api_docs': 'api_docs', 'admin': None,
    }
    
    needed_apps = set(must_have)
    for db_name in db_apps:
        mapped = app_mapping.get(db_name)
        if mapped:
            needed_apps.add(mapped)
    
    # Load tools
    tools = []
    for app in needed_apps:
        app_file = f"{api_dir}/{app}.json"
        if os.path.exists(app_file):
            with open(app_file) as f:
                tools.extend(json.load(f))
    
    return tools


def bridge_call(world: AppWorld, tool_name: str, params: dict) -> str:
    """Bridge function calling → AppWorld execute → real data."""
    parts = tool_name.split("__", 1)
    if len(parts) != 2:
        return f"Error: invalid tool name '{tool_name}'"
    app, method = parts
    
    args_parts = []
    for k, v in params.items():
        if isinstance(v, str):
            v_escaped = v.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
            args_parts.append(f"{k}='{v_escaped}'")
        elif isinstance(v, bool):
            args_parts.append(f"{k}={'True' if v else 'False'}")
        elif isinstance(v, (int, float)):
            args_parts.append(f"{k}={v}")
        elif isinstance(v, list):
            args_parts.append(f"{k}={json.dumps(v)}")
        elif v is None:
            continue
        else:
            args_parts.append(f"{k}={json.dumps(v)}")
    
    code = f"result = apis.{app}.{method}({', '.join(args_parts)})\nprint(result)"
    return world.execute(code)


def run_task(task_id: str, client: OpenAI, model: str, data_dir: str = "data",
             max_turns: int = 20, max_retries: int = 5) -> dict:
    """Run a single AppWorld task and collect the trajectory."""
    
    # Load task spec
    with open(f"{data_dir}/tasks/{task_id}/specs.json") as f:
        spec = json.load(f)
    
    # Load tools
    tools = load_tools_for_task(task_id, data_dir)
    print(f"  Tools: {len(tools)} APIs")
    
    # Initialize AppWorld environment
    world = AppWorld(task_id=task_id, experiment_name=f"train_{task_id}")
    
    # Build messages
    system_msg = f"""You are a helpful assistant that completes tasks using available tools.

Current user: {spec['supervisor']['first_name']} {spec['supervisor']['last_name']} ({spec['supervisor']['email']})

Important workflow:
1. Use supervisor__show_profile to get your profile info
2. Use supervisor__show_account_passwords to get login credentials for apps
3. Login to required apps using their login API (e.g., venmo__login, spotify__login)
4. Use the access_token from login for subsequent API calls in that app
5. Complete the task step by step
6. IMPORTANT: When the task is done, you MUST call supervisor__complete_task to mark it complete.
   - For action tasks (placing orders, sending money, etc.): call supervisor__complete_task(answer=null, status="success")
   - For question tasks (asking "what is...?"): call supervisor__complete_task(answer="your answer here", status="success")
   - Never end without calling supervisor__complete_task."""

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": spec['instruction']},
    ]
    
    for turn in range(max_turns):
        # Call LLM with retry
        response = None
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    temperature=1,
                )
                break
            except Exception as e:
                err = str(e)
                if "rate" in err.lower() or "429" in err or "overloaded" in err.lower():
                    wait = 2 ** attempt + 1
                    print(f"  [retry {attempt+1}/{max_retries}] waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  Error: {e}")
                    break
        
        if response is None:
            print(f"  Failed after {max_retries} retries")
            break
        
        msg = response.choices[0].message
        reasoning = getattr(msg, 'reasoning_content', '')
        
        # Build message dict
        msg_dict = msg.model_dump(exclude_none=True)
        if reasoning:
            msg_dict['reasoning_content'] = reasoning
        messages.append(msg_dict)
        
        if msg.tool_calls:
            for tc in msg.tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)
                print(f"  Turn {turn+1}: 🔧 {fn_name}")
                
                result = bridge_call(world, fn_name, fn_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result[:10000],  # Truncate very long responses
                })
        else:
            print(f"  Turn {turn+1}: 💬 Final response")
            break
    
    # Evaluate before closing
    evaluation = None
    try:
        result = world.evaluate()
        evaluation = result.to_dict()
        if evaluation['success']:
            print(f"  ✅ Eval: {len(evaluation['passes'])}/{evaluation['num_tests']} passed")
        else:
            print(f"  ❌ Eval: {len(evaluation['passes'])}/{evaluation['num_tests']} passed, {len(evaluation['failures'])} failed")
    except Exception as e:
        print(f"  ⚠️ Eval error: {e}")
        evaluation = {"success": False, "error": str(e)}
    
    world.close()
    
    return {
        "task_id": task_id,
        "instruction": spec['instruction'],
        "user": f"{spec['supervisor']['first_name']} {spec['supervisor']['last_name']}",
        "messages": messages,
        "tools": tools,
        "total_turns": turn + 1,
        "evaluation": evaluation,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate training data from AppWorld")
    parser.add_argument("--task_id", type=str, help="Run a specific task")
    parser.add_argument("--split", type=str, choices=["train", "dev", "test_normal", "test_challenge"],
                       help="Run all tasks in a split")
    parser.add_argument("--output", type=str, default="results_appworld", help="Output directory")
    parser.add_argument("--model", type=str, default="kimi-k2.5", help="Model name")
    parser.add_argument("--api_key", type=str, default=os.environ.get("OPENAI_API_KEY", ""))
    parser.add_argument("--api_base", type=str, default=os.environ.get("OPENAI_API_BASE", ""))
    parser.add_argument("--max_turns", type=int, default=20)
    parser.add_argument("--data_dir", type=str, default="data", help="AppWorld data directory")
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    client = OpenAI(api_key=args.api_key, base_url=args.api_base)
    
    # Collect task IDs
    if args.task_id:
        task_ids = [args.task_id]
    elif args.split:
        with open(f"{args.data_dir}/datasets/{args.split}.txt") as f:
            task_ids = [line.strip() for line in f if line.strip()]
    else:
        print("Please specify --task_id or --split")
        return
    
    print(f"Running {len(task_ids)} tasks with model={args.model}")
    
    output_file = f"{args.output}/appworld_{args.model.replace('/', '_')}_{args.split or args.task_id}.jsonl"
    
    for i, tid in enumerate(task_ids):
        print(f"\n[{i+1}/{len(task_ids)}] Task: {tid}")
        try:
            result = run_task(tid, client, args.model, args.data_dir, args.max_turns)
            
            with open(output_file, "a") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            
            msg_count = len(result['messages'])
            tc_count = sum(1 for m in result['messages'] if isinstance(m, dict) and m.get('tool_calls'))
            print(f"  ✅ {msg_count} messages, {tc_count} tool calls → saved")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            with open(output_file, "a") as f:
                f.write(json.dumps({"task_id": tid, "error": str(e)}) + "\n")
    
    print(f"\nDone! Results in {output_file}")


if __name__ == "__main__":
    main()
