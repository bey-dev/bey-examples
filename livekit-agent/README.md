# Beyond Presence LiveKit Agent

A minimal video agent using the Beyond Presence speech-to-video integration for LiveKit.

Your local LLM voice agent powers the conversation, while Beyond Presence renders and streams the video avatar directly to the room.

## Requirements

Make sure to have an account for the following services:

- [Beyond Presence](https://app.bey.chat)
- [LiveKit Cloud](https://cloud.livekit.io)
- [OpenAI Platform](https://platform.openai.com)

## Setup

### Environment

Copy `.env.template` to `.env`, then provide the required values for:

- **LiveKit Server**: [API Keys](https://cloud.livekit.io/projects/p_/settings/keys)
- **Beyond Presence API**: [API Keys](https://app.bey.chat/apiKeys)
- **OpenAI API**: [API Keys](https://platform.openai.com/settings/organization/api-keys)

You can use a default avatar by leaving the avatar ID variable empty, or provide one to use a specific avatar.
See [available default avatars](https://docs.bey.dev/get-started/avatars/default).

**Note**: The Beyond Presence speech-to-video integration requires a publicly accessible LiveKit server; local-only instances won't suffice.

### Agent Worker

Choose your preferred implementation:

#### Python

Requires Python `>=3.9`. Run:

```sh
pip install -r requirements.txt
python main.py
```

#### JavaScript

Install dependencies and run the example:

```
pnpm install
node --env-file .env main.js
```

---

On start, a LiveKit worker subscribes to the server and dispatches agents to handle calls.
Your voice agent processes the conversation but streams its audio output to the Beyond Presence video agent rather than directly to the room.
Our video agent then generates synchronized avatar video from this audio stream and posts the combined video/audio feed to the room for end users.

**Note**: The code also features snippets to uncomment that let you customize your agent's behavior!

**Note**: LiveKit code often require the latest versions to work as expected. Keeping dependencies up to date is recommended.

### Client

Join a call in the [Agents Playground](https://agents-playground.livekit.io) by connecting to your LiveKit Cloud project.

**Note**: The playground shows a three-way conversation, but you can hide the voice agent in your own frontend.

## Next Steps

- [LiveKit React Quickstart](https://docs.livekit.io/home/quickstarts/react): integrate LiveKit into your React frontend
- [LiveKit Voice AI Quickstart](https://docs.livekit.io/agents/start/voice-ai): learn how to build voice agents with LiveKit
- [Beyond Presence Integrations](https://docs.bey.dev/integrations): discover more integration options
