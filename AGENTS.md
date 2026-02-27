# AGENTS.md

## Cursor Cloud specific instructions

### Overview

tau-bench is a Python CLI benchmark for evaluating Tool-Agent-User interactions in airline and retail customer service domains. There is no web frontend, database, or Docker — it is a single Python package.

### Running the application

- **Install**: `pip install -e .` (editable mode from repo root)
- **CLI entry point**: `python run.py --help` for all options
- **Full benchmark run** requires at least one LLM API key set as an environment variable (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `MISTRAL_API_KEY`). Without API keys, benchmarks cannot execute.
- See `README.md` for full CLI examples.

### Testing without API keys

The tool implementations and data can be exercised directly in Python without API keys:

```python
from tau_bench.envs.airline.data import load_data
from tau_bench.envs.airline.tools.get_user_details import GetUserDetails
data = load_data()
result = GetUserDetails.invoke(data=data, user_id="mia_li_3668")
```

Both domains (airline and retail) load static JSON data bundled in the package. All tools can be invoked directly against loaded data.

### Domains

- **Airline**: 300 flights, 2000 reservations, 500 users, 50 test tasks, 14 tools
- **Retail**: 50 products, 1000 orders, 500 users, 115 test tasks (test split), 16 tools
- **Hotel**: hotel reservations, rooms, services, 17 tools
- **Course**: student registrations, courses, departments, 16 tools
- **Investment**: clients, brokerage/IRA/savings accounts, securities, holdings, orders, 18 tools

### Caveats

- There is no formal test suite (pytest/unittest). The `*_test.py` files under `tau_bench/envs/` are **task definition files**, not automated tests.
- There is no linting configuration in the repo (no flake8, pylint, ruff, pyproject.toml, etc.).
- The retail domain uses `TASKS_TEST` (not `TASKS`) as the export name in `tasks_test.py`.
- The `--model-provider` CLI flag uses `LlmProviders.*` enum values from litellm (e.g., `LlmProviders.OPENAI`).
