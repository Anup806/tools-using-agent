# tools-using-agent

A small, unfinished learning project for understanding LLM calls, tools, web search, function calling, agents, and short-term memory with LangChain and Groq.

This repository is intentionally a work in progress. The notebook contains guided exercises and experiments. Completing every exercise is not required before using version control or organizing the project.

## Project structure

- `notebooks/`: interactive learning material and experiments.
- `src/`: reusable Python code that can eventually become an application.
- `tests/`: small automated checks that protect behavior already implemented.
- `requirements.txt`: reproducible Python dependencies.
- `.env.example`: names of required environment variables without real secrets.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Groq API key.
4. Run the tests:

   ```powershell
   python -m pytest
   ```

## Run the Python agent

```powershell
python -m src.agent
```

The agent uses DuckDuckGo for web search and Groq for the language model. Type `exit` to stop the command-line program.

## Learning notebook

Open `notebooks/ddgs-and-toolcall.ipynb` in VS Code or Jupyter. The notebook is the primary learning surface and contains TODO exercises. The code in `src/` is a cleaner application-oriented version of the concepts being practiced.

## Current status

Implemented:

- Basic Groq model configuration
- DuckDuckGo search tool
- Agent construction with short-term in-memory memory
- Command-line interaction
- Tests for deterministic behavior

Planned practice:

- Add more tools
- Improve error handling and logging
- Add stronger tests with mocked model and search responses
- Try a persistent checkpointer
- Expose the agent through an API
