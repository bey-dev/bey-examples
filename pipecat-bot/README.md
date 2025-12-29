# Beyond Presence Pipecat Bot

A minimal Pipecat avatar video bot using Beyond Presence.

Your local voice bot powers the conversation, while our video bot renders the avatar and streams synced audio-video to the room.

## Requirements

Make sure to have an account for the following services:

- [Beyond Presence](https://app.bey.chat)
- [Daily](https://www.daily.co)
- [OpenAI Platform](https://platform.openai.com)

## Setup

### Environment

Copy `.env.template` to `.env`, then provide the required values for:

- `BEY_API_KEY`: [Bey Dashboard -> Settings](https://app.bey.chat/settings) -> API Keys
- `DAILY_ROOM_URL`: [Daily Dashboard -> Rooms](https://dashboard.daily.co/rooms)
- `DAILY_API_KEY`: [Daily Dashboard -> Developers](https://dashboard.daily.co/developers)
- `OPENAI_API_KEY`: [OpenAI Platform -> API keys](https://platform.openai.com/settings/organization/api-keys)

### Agent Worker

Requires Python `>=3.10`. Run:

```sh
pip install -r requirements.txt
python main.py
```

On start, your voice bot and the Beyond Presence video bot join the Daily room.
Your voice bot processes the conversation but streams its audio output to our video bot rather than directly to the room.
Our video bot then generates synchronized avatar video from this audio stream and posts the combined video/audio feed to the room for end users.

**Note**: The code also features snippets to uncomment that let you customize your agent's behavior!

### Client

Use any browser and join the room by visiting the `DAILY_ROOM_URL` specified above.

**Note**: The web client shows a three-way conversation, but you can hide the voice agent in your own frontend.

## Documentation

- [Beyond Presence Integration & API Reference](https://docs.bey.dev/integration/livekit)
- [Pipecat Quickstart](https://docs.pipecat.ai/getting-started/quickstart)
