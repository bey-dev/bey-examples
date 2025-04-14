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

### Environment

Copy `.env.template` to `.env`, then provide the required values for:

- **LiveKit Server**: [Cloud Project page](https://cloud.livekit.io/projects) > Settings > Keys
- **Beyond Presence API**: [Creator Dashboard](https://app.bey.chat) > Settings > API Keys
- **OpenAI API**: [API Keys page](https://platform.openai.com/settings/organization/api-keys)

### Agent Worker

Requires Python `>=3.9`. Run:

```sh
pip install -e .
python main.py [--avatar-id YOUR_AVATAR_ID]
```

On start, a LiveKit worker subscribes to the server and dispatches avatar agents to handle calls.

If no `--avatar-id` is passed, the default avatar is used.

#### Client

Use any LiveKit client with video support to start a call and interact with the avatar agent.

For a quick start, deploy [LiveKit Meet](https://cloud.livekit.io/projects/p_/sandbox/templates/meet) and configure it with your server URL and token.

## Documentation

For detailed usage instructions and API reference, visit [our docs](https://docs.bey.dev/integration/livekit).
