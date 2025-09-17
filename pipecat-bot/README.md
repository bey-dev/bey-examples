# Beyond Presence Pipecat Agent

A minimal Pipecat avatar agent using the Beyond Presence API.

Your local agent powers the conversation, while the API renders video and streams synced audio-video to the room.

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

On start, a voice bot and video bot join the Daily room.
The voice bot processes the conversation but streams its audio output to the video bot rather than directly to the room.
The video bot then generates synchronized avatar video from this audio stream and posts the combined video/audio feed to the room for end users.

### Client

Use any browser and join the room by visiting the `DAILY_ROOM_URL` specified above.

### Advanced Configuration

To optimize for latency, uncomment the lines relative to Deepgram STT, Azure LLM, and ElevenLabs TTS and provide API keys for the services.

## Documentation

- [Beyond Presence Integration & API Reference](https://docs.bey.dev/integration/livekit)
- [Pipecat Quickstart](https://docs.pipecat.ai/getting-started/quickstart)
