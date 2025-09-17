# Beyond Presence LiveKit Agent

A minimal LiveKit avatar video agent using Beyond Presence.

Your local voice agent powers the conversation, while our video agent renders the avatar and streams synced audio-video to the room.

## Requirements

Make sure to have an account for the following services:

- [Beyond Presence](https://app.bey.chat)
- [LiveKit Cloud](https://cloud.livekit.io)
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
pip install -r requirements.txt
python main.py [--avatar-id YOUR_AVATAR_ID]
```

On start, a LiveKit worker subscribes to the server and dispatches agents to handle calls.
Your voice agent processes the conversation but streams its audio output to our video agent rather than directly to the room.
Our video agent then generates synchronized avatar video from this audio stream and posts the combined video/audio feed to the room for end users.

If no `--avatar-id` is passed, the default avatar is used.

**Note**: LiveKit code often require the latest Python package versions to function as expected. Keeping dependencies up to date is recommended.

### Client

Use any LiveKit client with video support to start a call and interact with the avatar agent.

For a quick start, deploy [LiveKit Meet](https://cloud.livekit.io/projects/p_/sandbox/templates/meet) via the LiveKit Cloud template.

## Documentation

- [Beyond Presence Integration & API Reference](https://docs.bey.dev/integration/livekit)
- [LiveKit Voice Agent Quickstart](https://docs.livekit.io/agents/start/voice-ai)
- [LiveKit React Integration Guide](https://docs.livekit.io/home/quickstarts/react)
