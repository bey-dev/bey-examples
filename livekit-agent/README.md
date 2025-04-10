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

Copy `.env.template` to `.env` and add your API keys:

- **Beyond Presence**: [Creator Dashboard](https://app.bey.chat) > Settings > API Keys > Create API Key.
- **OpenAI**: [API Keys page](https://platform.openai.com/settings/organization/api-keys).

### Services

This example uses:

- a LiveKit server to host calls
- a LiveKit agent worker to dispatch avatar agents
- a LiveKit client (video-enabled) to join calls and visualize the avatar

#### Server

Install the [LiveKit CLI](https://docs.livekit.io/home/self-hosting/server-setup/#install-livekit-server), then run:

```sh
livekit-server --dev
```

The default `.env` values point to this local instance.

To use a remote server, update `.env`:

```
LIVEKIT_URL=ws[s]://<host>[:<port>]
LIVEKIT_API_KEY=<key>
LIVEKIT_API_SECRET=<secret>
```

#### Agent Worker

Requires Python `>=3.9`. Run:

```sh
pip install -e .
python main.py [--avatar-id YOUR_AVATAR_ID]
```

If no `--avatar-id` is passed, the default avatar is used.

#### Client

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
