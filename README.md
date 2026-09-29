# AI agent learning

A small Python project for learning how a local LLM can use tools. It talks to Ollama `llama3.2` over HTTP. There is no OpenAI client and no agent framework (no LangChain, LangGraph, or CrewAI).

Agent loop logic is not built yet. This repo is the file layout plus three tools and a local LLM helper.

## Prerequisites

1. Install [Ollama](https://ollama.com).
2. Start Ollama.
3. Pull the model:

   ```sh
   ollama pull llama3.2
   ```

## Run it

Create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with `.\.venv\Scripts\Activate.ps1`.

Install dependencies (none beyond the standard library):

```sh
python -m pip install -r requirements.txt
```

Ask llama3.2 a question directly:

```sh
python local_llm.py
```

The placeholder agent prints a short message and exits:

```sh
python agent.py
```

## Files

- `agent.py` — placeholder entry point. Tool-calling agent logic will go here later.
- `local_llm.py` — POSTs a prompt to `http://127.0.0.1:11434/api/generate` using model `llama3.2`.
- `calculator.py` — safely evaluates numbers, parentheses, `+`, `-`, `*`, and `/`. It parses an expression tree and never runs arbitrary Python.
- `datetime_tool.py` — returns the current local date and time.
- `file_tool.py` — reads the UTF-8 contents of a local text file.
- `requirements.txt` — empty of third-party packages; the Ollama client uses `urllib`.
- `.gitignore` — keeps virtual environments, env files, and Python cache out of version control.
