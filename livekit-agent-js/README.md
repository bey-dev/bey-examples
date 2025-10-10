# Bey Avatar Example for LiveKit Agents

This is a complete example project demonstrating how to use the [LiveKit Bey Avatar Plugin](https://github.com/livekit/agents-js/pull/759) to create AI voice agents with visual avatars powered by Beyond Presence.

## What This Does

This example creates voice AI agents that:
- Have **visual avatars** powered by Beyond Presence
- Engage in **natural voice conversations** using OpenAI
- Provide **realistic lip-sync** animations
- Work with any **LiveKit client** (web, mobile, desktop)

## Examples Included

### 1. Basic Agent (`src/index.ts`)
Simple avatar agent using OpenAI Realtime API for natural conversations.

```bash
npm run dev
```

### 2. Tool Calling Agent (`src/tool-calling.ts`)
Template for adding custom functions/tools. See [LiveKit Agents Tools Guide](https://docs.livekit.io/agents/build/tools/) for implementation details.

```bash
npm run dev:tools
```

### 3. STT/LLM/TTS Pipeline (`src/stt-llm-tts.ts`)
Shows how to use separate Speech-to-Text, Language Model, and Text-to-Speech components with Voice Activity Detection (VAD) instead of the Realtime API.

```bash
npm run dev:stt-llm-tts
```

## Prerequisites

Before you start, you'll need:

1. **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
2. **LiveKit Account** - [Sign up for free](https://livekit.io/)
3. **Beyond Presence API Key** - [Get your key](https://beyondpresence.com/)
4. **OpenAI API Key** - [Create an account](https://platform.openai.com/)

## Quick Start

### 1. Navigate to Directory

```bash
cd livekit-agent-js
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# LiveKit Configuration (get from https://cloud.livekit.io/)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Beyond Presence Configuration
BEY_API_KEY=your-bey-api-key
BEY_AVATAR_ID=b9be11b8-89fb-4227-8f86-4a881393cbdb  # Your avatar ID (Optional)

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
```

### 4. Run the Agent

**Development mode** (with hot reload):
```bash
npm run dev                # Basic example
npm run dev:tools          # With tool calling
npm run dev:stt-llm-tts    # With STT/LLM/TTS pipeline
```

**Production mode**:
```bash
npm run build
npm start                  # Basic example
npm start:tools            # With tool calling
npm start:stt-llm-tts      # With STT/LLM/TTS pipeline
```

You should see output like:
```
Starting Bey Avatar Agent
Connected to room: your-room-name
Agent session started
Avatar session started
Agent is ready
```

## Testing Your Agent

### Option 1: LiveKit Agents Playground (Easiest)

1. Go to [https://agents-playground.livekit.io/](https://agents-playground.livekit.io/)
2. Enter your LiveKit credentials
3. Click "Connect"
4. Start talking to your avatar agent!

### Option 2: Agent Starter React App

```bash
# In a new terminal
git clone https://github.com/livekit-examples/agent-starter-react.git
cd agent-starter-react
npm install

# Create .env.local with your LiveKit credentials
echo "LIVEKIT_URL=wss://your-project.livekit.cloud" > .env.local
echo "LIVEKIT_API_KEY=your-api-key" >> .env.local
echo "LIVEKIT_API_SECRET=your-api-secret" >> .env.local

npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Option 3: Build Your Own Client

Use any [LiveKit client SDK](https://docs.livekit.io/client-sdk-js/) to connect to a room. The agent will automatically join when a room is created.

## Customization Guide

### Change Avatar Voice

Edit the agent file and modify the `voice` parameter:

```typescript
const session = new voice.AgentSession({
  llm: new openai.realtime.RealtimeModel({
    voice: 'nova', // Options: alloy, echo, fable, onyx, nova, shimmer
  }),
});
```

### Customize Avatar Behavior

Modify the instructions in the `Agent` constructor:

```typescript
const agent = new voice.Agent({
  instructions: `You are a helpful assistant specialized in customer support.
    Be professional, friendly, and concise in your responses.`,
});
```

### Use Different Avatar

Set a different `BEY_AVATAR_ID` in your `.env` file with your custom avatar ID from Beyond Presence.

### Add Custom Tools/Functions

LiveKit Agents supports function/tool calling, allowing your agent to invoke custom functions. For detailed implementation, see the [LiveKit Agents Tools Guide](https://docs.livekit.io/agents/build/tools/).

The `src/tool-calling.ts` file provides a template for setting up agents with tool calling capabilities. Tools can be defined and integrated with both the Realtime API and STT/LLM/TTS pipeline.

### Use Alternative STT/LLM/TTS Providers

Instead of using OpenAI Realtime, you can mix and match providers. **Important**: When using STT/LLM/TTS pipeline, you must add a VAD (Voice Activity Detection) to the agent:

```typescript
import * as silero from '@livekit/agents-plugin-silero';
import * as deepgram from '@livekit/agents-plugin-deepgram';
import * as elevenlabs from '@livekit/agents-plugin-elevenlabs';

const agent = new voice.Agent({
  instructions: 'Your instructions...',
  vad: silero.VAD.load(),  // Required for STT/LLM/TTS pipeline
});

const session = new voice.AgentSession({
  stt: new deepgram.STT(),           // Deepgram for speech recognition
  llm: new openai.LLM(),              // OpenAI for language model
  tts: new elevenlabs.TTS(),          // ElevenLabs for speech synthesis
});
```

## Project Structure

```
livekit-agent-js/
├── src/
│   ├── index.ts           # Basic agent example
│   ├── tool-calling.ts    # Agent with custom tools
│   └── stt-llm-tts.ts     # Agent with STT/LLM/TTS pipeline
├── plugin-bey/            # Local Bey plugin (from PR #759)
├── .env                   # Your environment variables (not in git)
├── .env.example          # Template for environment variables
├── .gitignore            # Files to ignore in git
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
└── README.md             # This file
```

## Architecture Overview

### Agent Components

1. **Voice Agent**: Manages conversation flow and agent behavior
2. **Agent Session**: Coordinates STT/LLM/TTS or uses Realtime API
3. **Bey Avatar Session**: Handles avatar visualization and lip-sync
4. **LiveKit Room**: Communication layer for real-time audio/video

### Pipeline Options

**Option 1: Realtime API (Recommended for simplicity)**
```
User Speech → OpenAI Realtime API → Agent Response → Bey Avatar
```

**Option 2: STT/LLM/TTS Pipeline (Recommended for flexibility)**
```
User Speech → STT → LLM → TTS → Bey Avatar
```

## Troubleshooting

### "Cannot find module '@livekit/agents-plugin-bey'"

Try reinstalling dependencies:
```bash
npm run clean
npm install
```

### "BEY_API_KEY must be set"

Make sure:
1. You created a `.env` file (not `.env.example`)
2. Your `.env` file contains valid API keys
3. The `.env` file is in the project root directory

### Avatar Not Appearing

Check that:
- Your Bey API key is valid and active
- The avatar ID exists in your Beyond Presence account
- Video is enabled in your LiveKit room settings
- Your frontend client is subscribing to video tracks

### Connection Issues

Verify:
- LiveKit URL starts with `wss://` (not `https://`)
- API key and secret are correct
- Your LiveKit project is active
- Firewall isn't blocking WebRTC connections

### Tool Calling Not Working

Ensure:
- Tools are properly defined with zod schemas
- Tools are passed to the LLM configuration
- OpenAI model supports function calling (gpt-4o, gpt-4-turbo, etc.)


## Learn More

### Documentation
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Agents Tools Guide](https://docs.livekit.io/agents/build/tools/)
- [Beyond Presence Documentation](https://docs.beyondpresence.com/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [LiveKit JavaScript SDK](https://docs.livekit.io/client-sdk-js/)

### Plugin & Examples
- [Plugin PR #759](https://github.com/livekit/agents-js/pull/759)
- [LiveKit Agents GitHub](https://github.com/livekit/agents-js)

## Contributing

Found an issue or have a suggestion? Please:
1. Check existing issues 
2. Open a new issue with details about your environment and the problem
3. Provide logs and steps to reproduce

## License

MIT

## Support

- [Beyond Presence Discord](https://bey.dev/community)
- [LiveKit Community Slack](https://livekit.io/join-slack)

---

Made with the [LiveKit Agents Framework](https://docs.livekit.io/agents/)
