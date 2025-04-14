# Beyond Presence LiveKit Agent

A minimal LiveKit avatar agent using the Beyond Presence API (Beta).

## Requirements

Make sure to have an account for the following services:

- [LiveKit Cloud](https://cloud.livekit.io)
- [Beyond Presence](https://app.bey.chat)
- [OpenAI Platform](https://platform.openai.com)

## Setup

### Environment

Copy `.env.template` to `.env`, then provide the required values for:

- **LiveKit Server**: [Cloud Project page](https://cloud.livekit.io/projects) > Settings > Keys
- **Beyond Presence API**: [Create and manage API keys](https://docs.bey.dev/api-key#creating-and-managing-api-keys)
- **OpenAI API**: [API Keys page](https://platform.openai.com/settings/organization/api-keys)

**Note**: The Beyond Presence avatar service requires a publicly accessible LiveKit server; local-only instances won't suffice.

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

- [Beyond Presence Integration & API Reference](https://docs.bey.dev/integration/livekit)
- [LiveKit Voice Agent Quickstart](https://docs.livekit.io/agents/start/voice-ai)
- [LiveKit React Integration Guide](https://docs.livekit.io/home/quickstarts/react)
