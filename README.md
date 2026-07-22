# anthropic-learning

Code written while learning how to use the [Claude API](https://docs.anthropic.com/en/api/overview) with the
[Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python). It's a personal sandbox — a series of
small exercises covering conversational chat, structured/JSON output, dataset generation, prompt evaluation, and
tool use.

## How this repo is organized

Each exercise lives on its **own git branch**. The default branch holds this overview; check out a branch to work
through a specific exercise. The code also evolves across the exercises: the earliest ones are plain Python scripts
launched from a `main.py`, and the later ones move to Jupyter notebooks backed by reusable helper classes.

| Branch | Focus | Key files |
| --- | --- | --- |
| `chat-bot-exercise` | A basic multi-turn chatbot that keeps conversation history | `chat_bot_exercise.py`, `main.py` |
| `python-bot-exercise` | A chatbot specialized for Python help | `python_bot_exercise.py` |
| `structured-data-exercise` | Extracting structured data from model output | `structured_data_exercise.py` |
| `prompt_evaluations_exercise` | Evaluating prompts against a generated dataset, with syntax validation | `evaluation_dataset.py`, `prompt_evaluations_exercise.py`, `syntax_validation.py` |
| `prompting-exercise` | Improving a prompt with prompt-engineering techniques (notebook) | `prompting-exercise.ipynb` + helper classes |
| `tool-use-exercise` | Tool use / function calling | `tool-use.ipynb`, `tool_use_functions.py`, `tool_schema_example.json` |
| `develop` | Integration branch carrying the notebook-based helper classes | notebooks + `claude_*.py` |

> Because it's branch-per-exercise, the set of files present depends on which branch you have checked out.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # Windows (Git Bash);  use .venv\Scripts\Activate.ps1 in PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the repo root with your API key (it is gitignored):
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

## Running

- **Notebook exercises** (`*.ipynb`): launch JupyterLab and run the cells against the `.venv` kernel.
  ```bash
  jupyter lab
  ```
  Notebooks enable `%autoreload 2`, so edits to the imported helper `.py` files take effect without restarting
  the kernel.
- **Script exercises** (earlier branches): run the entry point directly.
  ```bash
  python main.py
  ```

Both styles load the API key with `load_dotenv()` and instantiate the client as `Anthropic()`, which reads
`ANTHROPIC_API_KEY` from the environment. The model is chosen per exercise via a `model` string variable — set it
to a current model ID such as `claude-sonnet-4-6` or `claude-opus-4-8`.

## Shared architecture (notebook exercises)

The later exercises share a small set of helper classes so the notebooks can focus on prompt content:

- **`ClaudeChat` (`claude_chat.py`)** — the single funnel for every API call. It owns the `messages` history and
  `stop_sequences` and builds the request for `client.messages.create` / `.stream`. Two calling modes:
  - `askClaude(...)` — **stateful**; uses and appends to the running conversation history.
  - `askClaudeSingle(...)` — **stateless**; a one-shot call that ignores history. Used for dataset generation and
    prompt evaluation, where each call must be independent.
  - Pass `streaming=True` to stream tokens to the terminal; otherwise the full text is returned. Both paths keep
    only `text`-type content blocks.
- **`ClaudeDataset` (`claude_dataset.py`)** — *composes* a `ClaudeChat` to generate an evaluation dataset and
  persist it to `dataset.json`.
- **`ClaudeEvaluation` (`claude_evaluation.py`)** — *composes* a `ClaudeChat` to run a prompt over the dataset and
  score it two ways: model-based grading (Claude returns a JSON score object) and code-based grading (output
  validity/format), then averages the results.
- **`ChatBot` (`chat_bot_functions.py`)** — a minimal, standalone conversation helper used by the simpler chatbot
  exercise.

### Convention: forcing clean JSON without prefilling

Instead of prefilling the assistant turn, the exercises append `"END_OF_COMMANDS"` to `stop_sequences` and pass an
explicit block of prompt rules (return only valid JSON, no markdown, no comments, then write `END_OF_COMMANDS`).
Responses are then parsed directly with `json.loads`. Reuse this pattern for any prompt that must return
machine-parseable output.
