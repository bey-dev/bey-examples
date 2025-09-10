# Beyond Presence Pipecat Agent

A minimal Pipecat avatar agent using the Beyond Presence API.

Your local agent powers the conversation, while the API renders video and streams synced audio-video to the room.

## Requirements

Make sure to have an account for the following services:

- [Daily ](https://www.daily.co) (Choose "Daily Video")
- [Beyond Presence](https://app.bey.chat)
- [OpenAI Platform](https://platform.openai.com)

## Setup

### Environment

Copy `.env.template` to `.env`, then provide the required values for:

- **DAILY_ROOM_URL & DAILY_API_KEY**: [Room page](https://dashboard.daily.co/rooms)
- **Beyond Presence API**: [Create and manage API keys](https://docs.bey.dev/api-key#creating-and-managing-api-keys)
- **OpenAI API**: [API Keys page](https://platform.openai.com/settings/organization/api-keys)

### Agent Worker

Requires Python `>=3.9`. Run:

```sh
pip install -r requirements.txt
python main.py [--avatar-id YOUR_AVATAR_ID]
```

If no `--avatar-id` is passed, the default avatar is used.

**Note**: Pipecat code often require the latest Python package versions to function as expected. Keeping dependencies up to date is recommended.

### Client

Use any browser and join the DAILY_ROOM_URL specified above

## Documentation

- [Beyond Presence Integration & API Reference](https://docs.bey.dev/integration/livekit)
- [Pipecat Quickstart](https://docs.pipecat.ai/getting-started/quickstart)
