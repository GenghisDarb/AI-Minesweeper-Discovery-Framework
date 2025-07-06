# Configuring LLM Backends

The AI Minesweeper framework supports multiple LLM backends. Follow the instructions below to configure your preferred backend.

## OpenAI
1. Obtain an API key from [OpenAI](https://platform.openai.com/).
2. Paste the key into the environment variable `OPENAI_API_KEY`.

## Anthropic Claude
1. Obtain an API key from [Anthropic](https://www.anthropic.com/).
2. Paste the key into the environment variable `CLAUDE_API_KEY`.

## Local (Ollama)
1. Ensure the Ollama server is running locally.
2. No API key is required for this backend.

## None
1. Select 'none' as the backend in the Streamlit UI.
2. This option disables LLM integration.
