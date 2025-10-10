# Beyond Presence LiveKit Agent

A minimal video agent using the Beyond Presence speech-to-video integration for LiveKit.

Your local LLM voice agent powers the conversation, while Beyond Presence renders and streams the video avatar directly to the room.

## Requirements

Make sure to have an account for the following services:

- [LiveKit Cloud](https://cloud.livekit.io)
- [Beyond Presence](https://app.bey.chat)
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

The Beyond Presence plugin is currently available in a fork pending merge.
To use it, first build the fork:

```sh
git submodule update --init .js-fork
pnpm -C .js-fork install
pnpm -C .js-fork build
```

Then install dependencies and run the example:

```
pnpm install
node --env-file .env main.js
```

---

On start, a LiveKit worker subscribes to the server and dispatches video agents to handle calls.

**Note**: LiveKit code often require the latest versions to work as expected. Keeping dependencies up to date is recommended.

### Client

Join a call in the [Agents Playground](https://agents-playground.livekit.io) by connecting to your LiveKit Cloud project.

**Note**: The playground shows a three-way conversation, but you can hide the voice agent in your own frontend.

## Next Steps

- [Hackathon Quickstart](.hackathon-quickstart.md): explore tool calling, stt/llm/tts configuration, and more
- [LiveKit Voice AI Quickstart](https://docs.livekit.io/agents/start/voice-ai): learn how to build agents with LiveKit
- [LiveKit React Quickstart](https://docs.livekit.io/home/quickstarts/react): integrate LiveKit into your React frontend
- [Beyond Presence Integrations](https://docs.bey.dev/integrations): discover more integration options
