# Bey Avatar Example for LiveKit Agents

This is a complete example project demonstrating how to use the [LiveKit Bey Avatar Plugin](https://github.com/livekit/agents-js/pull/759) to create an AI voice agent with a visual avatar powered by Beyond Presence.

##  What This Does

This example creates a voice AI agent that:
- Has a **visual avatar** powered by Beyond Presence
- Engages in **natural voice conversations** using OpenAI Realtime
- Provides **realistic lip-sync** animations
- Works with any **LiveKit client** (web, mobile, desktop)

## Prerequisites

Before you start, you'll need:

1. **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
2. **LiveKit Account** - [Sign up for free](https://livekit.io/)
3. **Beyond Presence API Key** - [Get your key](https://beyondpresence.com/)
4. **OpenAI API Key** - [Create an account](https://platform.openai.com/)

## Quick Start

### 1. Clone This Repository

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
npm run dev
```

**Production mode**:
```bash
npm run build
npm start
```

You should see output like:
```
Starting Bey Avatar Agent...
Connected to room: your-room-name
Initializing Bey avatar...
Creating agent session with OpenAI Realtime...
Starting avatar session...
Avatar session started successfully
Starting agent session...
Agent session started
Generating greeting...
Agent is ready and waiting for user input!
```

## 🎮 Testing Your Agent

You have several options to interact with your agent:

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

## 🛠️ Customization

### Change Avatar Voice

Edit `src/index.ts` and modify the `voice` parameter:

```typescript
const session = new AgentSession({
  llm: new RealtimeModel({
    voice: 'nova', // Options: alloy, echo, fable, onyx, nova, shimmer
    // ... other options
  }),
});
```

### Customize Avatar Behavior

Modify the instructions in `src/index.ts`:

```typescript
instructions: `You are a helpful assistant specialized in customer support.
Be professional, friendly, and concise in your responses.`,
```

### Use Different Avatar

Set a different `BEY_AVATAR_ID` in your `.env` file with your custom avatar ID from Beyond Presence.

## 📁 Project Structure

```
livekit-agent-js/
├── src/
│   └── index.ts          # Main agent code
├── .env                   # Your environment variables (not in git)
├── .env.example          # Template for environment variables
├── .gitignore            # Files to ignore in git
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
└── README.md             # This file
```

## 🔧 Troubleshooting

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

## 📦 Moving to Production

Once PR #759 is merged, update your `package.json`:

```json
{
  "dependencies": {
    "@livekit/agents-plugin-bey": "^1.0.0"
  }
}
```

Then run:
```bash
npm install
```

## 📚 Learn More

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Beyond Presence Documentation](https://docs.beyondpresence.com/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [LiveKit JavaScript SDK](https://docs.livekit.io/client-sdk-js/)
- [Plugin PR #759](https://github.com/livekit/agents-js/pull/759)

## 🤝 Contributing

Found an issue or have a suggestion? Please:
1. Check existing issues on the [PR discussion](https://github.com/livekit/agents-js/pull/759)
2. Open a new issue with details about your environment and the problem
3. Provide logs and steps to reproduce

## 📄 License

MIT

## 💬 Support

- [LiveKit Community Slack](https://livekit.io/join-slack)
- [GitHub Issues](https://github.com/livekit/agents-js/issues)
- [LiveKit Support](https://support.livekit.io/)

---
