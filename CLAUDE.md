# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal learning repository for exploring the Claude API (Anthropic Python SDK). It is not a shipped application — there is no build step, no test suite, and no package manifest. Work happens in Jupyter notebooks (`*.ipynb`) that import reusable helper classes from the `*.py` modules at the repo root.

## Branch-per-exercise workflow

Each exercise lives on its own git branch (e.g. `chat-bot-exercise`, `python-bot-exercise`, `structured-data-exercise`, `prompt_evaluations_exercise`, `prompting_exercise`, `claude-code-exercise`). The helper `.py` files and notebooks present on any given branch reflect that branch's exercise, so the set of files differs between branches. When starting new work, expect to branch off `develop`/`main` rather than adding to an existing exercise.

## Setup & running

- Secrets: `.env` holds `ANTHROPIC_API_KEY` (gitignored). Notebooks call `load_dotenv()` then `Anthropic()`, which reads the key from the environment.
- Environment: a local `.venv/` is used. Dependencies (installed manually, no requirements file) are `anthropic`, `python-dotenv`, and `jupyter`/`ipykernel`.
- Run: open the notebook and execute cells against the `.venv` kernel. Notebooks use `%autoreload 2` so edits to the imported `.py` helpers take effect without restarting the kernel.
- Model is set per-notebook via a `model` string variable passed into the helper classes.

## Architecture

The helper classes wrap the raw SDK so notebooks stay focused on prompt content. All Claude calls funnel through `ClaudeChat`.

- **`ClaudeChat` (`claude_chat.py`)** — the core wrapper. Holds `messages` history and `stop_sequences`, and builds the `parameters` dict for `client.messages.create`/`.stream`. Two calling modes matter:
  - `askClaude(...)` uses and appends to conversation history (`userInput`/`claudeResponse` store turns).
  - `askClaudeSingle(...)` is **stateless** — a one-shot call that does not touch history. Use it for dataset generation and prompt evaluation where each call must be independent.
  - `streaming=True` streams tokens to the terminal; otherwise the full response is returned. Both paths concatenate only `text`-type content blocks.
- **`ClaudeDataset` (`claude_dataset.py`)** and **`ClaudeEvaluation` (`claude_evaluation.py`)** — each *composes* a `ClaudeChat` instance rather than subclassing it, and drives it via `askClaudeSingle`. `ClaudeDataset` generates an evaluation dataset and persists it to `dataset.json`. `ClaudeEvaluation` runs a prompt over that dataset and scores it two ways: `modelBasedGrading` (Claude returns a JSON score object) and `codeBasedGrading` (checks output validity/format), then `calculateAverage` combines them.
- **`ChatBot` (`chat_bot_functions.py`)** — a minimal, self-contained conversation helper used by the simpler chat-bot exercise; overlaps conceptually with `ClaudeChat` but is intentionally standalone.

## Conventions specific to this repo

- **Structured (JSON) output without prefilling.** Instead of assistant-message prefill, the code appends `"END_OF_COMMANDS"` to `stop_sequences` and passes explicit "prompt rules" text (return only valid JSON, no markdown, no comments, write `END_OF_COMMANDS` after the output). Follow this same pattern when adding prompts that must return parseable JSON.
- Prompts are assembled in the notebook by f-string-concatenating: the base prompt + the source text (e.g. `short_scholarly_text.txt`) + the relevant prompt-rules block.
- Grading prompts expect a fixed JSON shape (`strengths`, `weaknesses`, `reasoning`, `score`) that is later `json.loads`-ed, so any change to that shape must stay in sync with `calculateAverage`.
