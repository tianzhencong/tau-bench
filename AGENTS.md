# AGENTS.md

## Cursor Cloud specific instructions

### Overview

**tau-bench** is a Python CLI benchmarking framework for evaluating Tool-Agent-User interactions. It has two simulated domains: `airline` and `retail`. There are no web servers, databases, or Docker containers — it is a pure Python package with in-memory simulated environments.

### Installation

Dependencies are managed via `setup.py`. Run `pip install -e .` from the repo root.

### Running the benchmark

See `README.md` for full CLI usage. The entry point is `python run.py` with flags for model, provider, environment, etc. Example:

```
python run.py --env retail --model gpt-4o --model-provider openai --user-model gpt-4o --user-model-provider openai --agent-strategy tool-calling --user-strategy llm --task-ids 0
```

Running the benchmark requires at least one LLM API key (e.g. `OPENAI_API_KEY`) set as an environment variable. Without API keys, you can still import modules, load environments/data/tools, and call tools directly — but you cannot run full end-to-end benchmark tasks.

### Key gotchas

- **No linter or test framework is configured.** The repo has no `pyproject.toml`, no `ruff.toml`, no `pytest` config. The `*_tasks_test.py` files are **data files** (task definitions), not actual test suites.
- **`user_strategy='human'` blocks on stdin.** When loading environments programmatically, avoid `human` strategy unless you intend interactive terminal input. Use `llm` strategy (requires API key) for automated runs.
- **Packages install to user site-packages** (`~/.local/lib/python3.12/site-packages`) since the system Python is used. Scripts land in `~/.local/bin` which may not be on `PATH`; this is fine since the main entry point is `python run.py`.
- **To exercise tools without an LLM API key**, import data loaders and tools directly:
  ```python
  from tau_bench.envs.retail.data import load_data
  from tau_bench.envs.retail.tools import ALL_TOOLS
  data = load_data()
  tools_map = {t.get_info()["function"]["name"]: t for t in ALL_TOOLS}
  result = tools_map["find_user_id_by_name_zip"].invoke(data=data, first_name="Yusuf", last_name="Rossi", zip="19122")
  ```
