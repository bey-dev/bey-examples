# Beyond Presence LiveKit Agent

A minimal avatar agent using the Beyond Presence API (Beta).

## Overview

This beta release provides a lightweight avatar agent built on the Beyond Presence API and LiveKit.
It leverages voice, STT, TTS, and LLM functionalities via several LiveKit plugins.

### Files

- `pyproject.toml`: Project configuration and dependency management
- `.env.template`: Template dotenv file containing API keys and connection details
- `main.py`: Main entry point that initializes and runs the agent

## Setup

Ensure you have Python `>=3.9` installed, then install dependencies:

```sh
pip install -e .
```

Next, copy `.env.template` to `.env` and update it with your LiveKit server credentials and API keys.

**Note**: To generate a Beyond Presence API key, login to the [creator dashboard](https://app.bey.chat) and navigate to Settings > API Keys > Create API Key.

## Running the Agent

Launch the agent with:

```sh
python main.py [--avatar-id YOUR_AVATAR_ID]
```

Replace `YOUR_AVATAR_ID` with a valid avatar ID if needed.
Omitting the flag will run the default configuration.

## Documentation

For detailed usage instructions and API reference, visit [our docs](https://docs.bey.dev/integration/livekit).
