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

Copy `.env.template` to `.env` and update it with your API keys for the Beyond Presence and OpenAI APIs.

- To generate a Beyond Presence API key, login to the [creator dashboard](https://app.bey.chat) and navigate to Settings > API Keys > Create API Key.
- To generate an OpenAI key, navigate to [this page](https://platform.openai.com/settings/organization/api-keys).

### Services

This example is based on three services:

- a LiveKit server to host calls
- a LiveKit client with video support to join calls on the server and visualize the avatar agent
- a LiveKit agent worker to subscribe to dispatch avatar agents to new calls

#### Server

To use your own LiveKit server, replace the values of of the `LIVEKIT` environment variables with your server details:

```
LIVEKIT_URL=ws[s]://<host>[:<port>]
LIVEKIT_API_KEY=<key>
LIVEKIT_API_SECRET=<secret>
```

To spin up a minimal LiveKit server, install the LiveKit CLI locally from [here](https://docs.livekit.io/home/self-hosting/server-setup/#install-livekit-server).
Then start the server with:

```sh
livekit-server --dev
```

The environment variables to specify when using the development LiveKit server are the ones from the template, so no further edit of the `.env` file is required.

**Note**: this configuration does not expose the server publicly, which means the client and agent will also need to run locally to connect to it.

#### Client

You can use any LiveKit client with video support to connect to the LiveKit server.

To use a minimal LiveKit client, install `node` from [here](https://nodejs.org/en/download) if missing, then install and run the project with:

```sh
cd .client
npm install
npm run dev
```

You can then browse to <http://localhost:3000> to use the client and connect to the server to join calls.

**Note**: Remember to specify the LiveKit environment variables in `.env` _before_ running the client.

#### Agent Worker

Ensure you have Python `>=3.9` installed, then install dependencies:

```sh
pip install -e .
```

Launch the agent with:

```sh
python main.py [--avatar-id YOUR_AVATAR_ID]
```

Replace `YOUR_AVATAR_ID` with a valid avatar ID if needed.
Omitting the flag will run the agent with the default avatar.

## Documentation

For detailed usage instructions and API reference, visit [our docs](https://docs.bey.dev/integration/livekit).
