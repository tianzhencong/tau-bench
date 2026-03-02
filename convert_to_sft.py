# Convert AppWorld trajectories to standard OpenAI SFT JSONL format
# Filters for high-quality trajectories (success=True or business-logic correct)
# Preserves reasoning_content for thinking model training
#
# Usage:
#   python convert_to_sft.py --input results_appworld/ --output sft_data/appworld_sft.jsonl
#   python convert_to_sft.py --input results_appworld/ --output sft_data/appworld_sft.jsonl --strict

import json
import os
import argparse


def is_business_correct(evaluation):
    """Check if all non-answer tests pass (business logic correct, ignore complete_task)."""
    if not evaluation:
        return False
    if evaluation.get('success'):
        return True
    failures = evaluation.get('failures', [])
    biz_failures = [f for f in failures if 'answers match' not in f.get('requirement', '')]
    return len(biz_failures) == 0


def clean_message(msg):
    """Clean a single message to standard OpenAI format."""
    if not isinstance(msg, dict):
        return None

    role = msg.get('role')
    if not role:
        return None

    cleaned = {"role": role}

    # System / User: just content
    if role in ("system", "user"):
        cleaned["content"] = msg.get("content", "")
        return cleaned

    # Assistant
    if role == "assistant":
        # reasoning_content (for thinking models)
        if msg.get("reasoning_content"):
            cleaned["reasoning_content"] = msg["reasoning_content"]

        # tool_calls
        if msg.get("tool_calls"):
            tool_calls = []
            for tc in msg["tool_calls"]:
                if not tc or not tc.get("function"):
                    continue
                clean_tc = {
                    "id": tc.get("id", ""),
                    "type": "function",
                    "function": {
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"]
                            if isinstance(tc["function"]["arguments"], str)
                            else json.dumps(tc["function"]["arguments"], ensure_ascii=False),
                    }
                }
                tool_calls.append(clean_tc)

            if tool_calls:
                cleaned["tool_calls"] = tool_calls
                # OpenAI requires content field even when tool_calls present
                cleaned["content"] = msg.get("content") or ""
            else:
                cleaned["content"] = msg.get("content", "")
        else:
            cleaned["content"] = msg.get("content", "")

        return cleaned

    # Tool response
    if role == "tool":
        cleaned["tool_call_id"] = msg.get("tool_call_id", "")
        cleaned["content"] = msg.get("content", "")
        return cleaned

    return None


def convert_trajectory(traj):
    """Convert a single trajectory to OpenAI SFT format."""
    messages = []
    for msg in traj.get("messages", []):
        cleaned = clean_message(msg)
        if cleaned:
            messages.append(cleaned)

    if len(messages) < 3:  # At least system + user + assistant
        return None

    result = {"messages": messages}

    # Optionally include tools definition
    if traj.get("tools"):
        result["tools"] = traj["tools"]

    return result


def main():
    parser = argparse.ArgumentParser(description="Convert AppWorld trajectories to OpenAI SFT format")
    parser.add_argument("--input", type=str, default="results_appworld/", help="Input directory with JSONL files")
    parser.add_argument("--output", type=str, default="sft_data/appworld_sft.jsonl", help="Output JSONL file")
    parser.add_argument("--strict", action="store_true", help="Only include success=True trajectories (exclude business-only-correct)")
    parser.add_argument("--no-tools", action="store_true", help="Exclude tools definitions (saves tokens)")
    parser.add_argument("--no-reasoning", action="store_true", help="Exclude reasoning_content")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    # Load all trajectories
    all_trajs = []
    for fname in sorted(os.listdir(args.input)):
        if not fname.endswith(".jsonl"):
            continue
        with open(os.path.join(args.input, fname)) as f:
            for line in f:
                if line.strip():
                    all_trajs.append(json.loads(line))

    print(f"Loaded {len(all_trajs)} trajectories")

    # Filter
    kept = 0
    skipped = 0
    with open(args.output, "w") as out:
        for traj in all_trajs:
            ev = traj.get("evaluation", {})

            if args.strict:
                if not ev.get("success"):
                    skipped += 1
                    continue
            else:
                if not is_business_correct(ev):
                    skipped += 1
                    continue

            converted = convert_trajectory(traj)
            if not converted:
                skipped += 1
                continue

            # Strip tools if requested
            if args.no_tools:
                converted.pop("tools", None)

            # Strip reasoning if requested
            if args.no_reasoning:
                for msg in converted["messages"]:
                    msg.pop("reasoning_content", None)

            out.write(json.dumps(converted, ensure_ascii=False) + "\n")
            kept += 1

    print(f"Output: {kept} training examples → {args.output}")
    print(f"Skipped: {skipped}")

    # Stats
    if kept > 0:
        total_msgs = 0
        total_tc = 0
        total_reasoning = 0
        with open(args.output) as f:
            for line in f:
                ex = json.loads(line)
                msgs = ex["messages"]
                total_msgs += len(msgs)
                for m in msgs:
                    if m.get("tool_calls"):
                        total_tc += 1
                    if m.get("reasoning_content"):
                        total_reasoning += 1

        print(f"\nStats:")
        print(f"  Total messages: {total_msgs} (avg {total_msgs/kept:.1f}/example)")
        print(f"  Total tool calls: {total_tc} (avg {total_tc/kept:.1f}/example)")
        print(f"  Total reasoning: {total_reasoning} (avg {total_reasoning/kept:.1f}/example)")


if __name__ == "__main__":
    main()
