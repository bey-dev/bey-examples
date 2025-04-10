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

- **Beyond Presence**: [Creator Dashboard](https://app.bey.chat) > Settings > API Keys
- **OpenAI**: [API Keys page](https://platform.openai.com/settings/organization/api-keys)
- **LiveKit**: [Cloud Project page](https://cloud.livekit.io/projects) > Settings > Keys

### Agent Worker

Requires Python `>=3.9`. Run:

```sh
pip install -e .
python main.py [--avatar-id YOUR_AVATAR_ID]
```

If no `--avatar-id` is passed, the default avatar is used.

### Client

Install [Node.js](https://nodejs.org/en/download) if missing, then:

```sh
cd .client
npm install
npm run dev
```

Visit <http://localhost:3000> to join calls and interact with the avatar agent.

You can also use your own video-enabled LiveKit client.

## Documentation

For detailed usage instructions and API reference, visit [our docs](https://docs.bey.dev/integration/livekit).
