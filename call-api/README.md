# Bey Call API Example

A simple, interactive example demonstrating how to use the Beyond Presence Call API to connect users with AI agents through LiveKit.

## Overview

This example shows how to:
- Call the Beyond Presence API to create a new call session
- Receive LiveKit connection credentials
- Connect to a LiveKit room with audio/video
- Interact with your AI agent in real-time
- Send chat messages during the call

## Prerequisites

Before running this example, you'll need:

1. **Beyond Presence Account**: Sign up at [app.bey.dev](https://app.bey.dev)
2. **API Key**: Get your API key from the Beyond Presence dashboard
3. **Agent ID**: Create an agent and note its ID from the dashboard
4. **Node.js**: Version 18 or higher

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Run the Development Server

```bash
npm run dev
```

This will start a local development server (typically at `http://localhost:5173`).

### 3. Open in Browser

Navigate to the URL shown in your terminal (e.g., `http://localhost:5173`).

## Usage

1. **Enter Credentials**
   - Paste your Beyond Presence API key in the "API Key" field
   - Enter your Agent ID in the "Agent ID" field

2. **Start Call**
   - Click the "Start Call" button
   - The app will:
     - Call the Bey API to create a new call session
     - Receive LiveKit connection credentials
     - Automatically connect to the LiveKit room

3. **Interact with Your Agent**
   - Click "Enable Mic" to allow your microphone
   - Click "Enable Camera" to share your video (optional)
   - Use the chat box to send text messages
   - The agent will appear in the participants area when connected

4. **End Call**
   - Click "End Call" to disconnect from the session

## API Reference

### Bey Call API Endpoint

```
POST https://api.bey.dev/v1/calls
```

**Headers:**
```json
{
  "Content-Type": "application/json",
  "x-api-key": "your-api-key"
}
```

**Request Body:**
```json
{
  "agent_id": "your-agent-id"
}
```

**Response:**
```json
{
  "id": "NgEcBFTZYRgKCKPOqD10",
  "agent_id": "a0c23ce1-34f9-48ba-96a5-b0b701bef0e4",
  "tags": {},
  "started_at": "2025-10-28T10:31:25.159564",
  "ended_at": null,
  "livekit_url": "wss://prod-w0h88kyi.livekit.cloud",
  "livekit_token": "eyJhbGci..."
}
```

## Project Structure

```
call-api/
├── index.html       # Main HTML interface
├── demo.ts          # TypeScript application logic
├── styles.css       # CSS styling
├── package.json     # Project dependencies
├── tsconfig.json    # TypeScript configuration
└── README.md        # This file
```

## Features

- ✅ Simple, clean UI for API credentials
- ✅ Real-time audio/video communication
- ✅ Text chat functionality
- ✅ Participant video rendering
- ✅ Connection status logging
- ✅ Mic and camera controls
- ✅ Speaking indicator
- ✅ Responsive design

## Technologies Used

- **TypeScript** - Type-safe JavaScript
- **LiveKit Client SDK** - WebRTC communication
- **Vite** - Fast build tool and dev server
- **Bootstrap** - UI styling framework

## Troubleshooting

### API Connection Issues

If you encounter API errors:
- Verify your API key is correct
- Check that your Agent ID exists in your dashboard
- Ensure your API key has the necessary permissions

### Media Permission Issues

If camera/microphone don't work:
- Check browser permissions for camera/microphone access
- Ensure you're running on HTTPS or localhost
- Try a different browser (Chrome/Edge recommended)

### Connection Issues

If LiveKit connection fails:
- Check browser console for detailed error messages
- Verify your firewall isn't blocking WebSocket connections
- Ensure you have a stable internet connection

## Resources

- [Beyond Presence Documentation](https://docs.bey.dev)
- [Beyond Presence API Reference](https://docs.bey.dev/api-reference)
- [LiveKit Documentation](https://docs.livekit.io)
- [Join our Slack Community](https://bey.dev/community)

## Support

Need help? Reach out:
- 📧 Email: support@beyondpresence.ai
- 💬 Slack: [bey.dev/community](https://bey.dev/community)
- 📖 Docs: [docs.bey.dev](https://docs.bey.dev)

## License

This example is provided as-is for demonstration purposes.
