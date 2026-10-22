# Search & Weather AI Agent

A small Streamlit app that uses a LangChain ReAct agent to answer questions with live web search and current-weather data.

Ask a question in natural language—for example, *“Find the capital of Japan and tell me its current weather.”* The agent can search the web with Tavily, look up current conditions with Weatherstack, and compose a response using OpenAI.

## Features

- Interactive query form in a Streamlit interface
- Live web search through Tavily
- Current temperature, conditions, and humidity through Weatherstack
- LangChain ReAct agent powered by OpenAI's `gpt-3.5-turbo`
- Prompt loaded from the public LangSmith prompt hub

## Project structure

```text
Search-Weather-AI-Agent-using-LangChain/
├── app.py                 # Streamlit application and agent setup
├── main.py                # Placeholder entry point
├── openai_demo.ipynb      # Notebook for trying the agent components
├── pyproject.toml         # Project metadata and dependencies
├── requirements.txt       # Pinned dependencies for pip
├── uv.lock                # Locked dependencies for uv
└── src/
    └── demo/
        ├── __init__.py
        └── py.typed
```

## Requirements

- Python 3.12 or newer
- API keys for OpenAI, Tavily, and Weatherstack
- Internet access to call the APIs and retrieve the LangSmith prompt

## Setup

1. Clone the repository and open its directory.
2. Create and activate a virtual environment, then install dependencies.

   **With uv:**

   ```powershell
   uv sync
   ```

   **Or with pip on Windows:**

   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API keys:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   WEATHERSTACK_API_KEY=your_weatherstack_api_key
   ```

   Keep `.env` private; do not commit API keys to source control.

## Run the app

From the project root:

```powershell
uv run streamlit run app.py
```

If you installed with pip and activated the virtual environment, run:

```powershell
streamlit run app.py
```

Streamlit will print a local URL to open in your browser. Enter a question and select **Run Agent**.

### Example questions

- “What are the latest developments in renewable energy?”
- “Find the capital of France and its current weather.”
- “Compare the current weather in Tokyo and Seoul.”

## How it works

```text
Your question
     │
     ▼
Streamlit UI ──► LangChain ReAct agent ──► OpenAI
                         │
                         ├── Tavily web search
                         ├── Weatherstack current weather
                         └── LangSmith public prompt
     │
     ▼
Answer displayed in the app
```

The search and weather tools are selected by the agent based on the question. Weather results include the requested city, temperature, conditions, and humidity.

## Development

The dependency versions are managed in `pyproject.toml` and `uv.lock`. `requirements.txt` is provided as a pinned pip export. The notebook contains an exploratory, step-by-step version of the app's agent setup.
