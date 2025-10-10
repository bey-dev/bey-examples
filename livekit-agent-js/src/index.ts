import 'dotenv/config';
import { AgentSession, cli, defineAgent, WorkerOptions, type JobContext } from '@livekit/agents';
import { RealtimeModel } from '@livekit/agents-plugin-openai';
import * as bey from '@livekit/agents-plugin-bey';

/**
 * This example demonstrates how to use the Bey Avatar Plugin with LiveKit Agents.
 * 
 * The agent:
 * 1. Connects to a LiveKit room
 * 2. Initializes a Bey avatar with your configured avatar ID
 * 3. Sets up an OpenAI Realtime voice agent
 * 4. Connects the avatar to display visual representation of the agent
 * 5. Greets users and engages in conversation with avatar animations
 */

const agent = defineAgent({
  entry: async (ctx: JobContext) => {
    console.log('🚀 Starting Bey Avatar Agent...');
    
    // Connect to the LiveKit room
    await ctx.connect();
    console.log('✅ Connected to room:', ctx.room.name);

    // Initialize the Bey avatar session
    console.log('🎭 Initializing Bey avatar...');
    const avatarSession = new bey.AvatarSession({
      apiKey: process.env.BEY_API_KEY,
      apiUrl: process.env.BEY_API_URL,
      avatarId: process.env.BEY_AVATAR_ID,
      avatarParticipantIdentity: 'bey-avatar',
      avatarParticipantName: 'AI Assistant',
    });

    // Create the agent session with OpenAI Realtime
    console.log('🤖 Creating agent session with OpenAI Realtime...');
    const session = new AgentSession({
      llm: new RealtimeModel({
        voice: 'alloy', // Options: alloy, echo, fable, onyx, nova, shimmer
        temperature: 0.8,
        instructions: `You are a friendly and helpful AI assistant with a visual avatar. 
        You can see and interact with users through your avatar. 
        Keep your responses natural and conversational.
        When users join, warmly greet them and ask how you can help.`,
      }),
    });

    // Start the avatar (this will make the avatar join the room)
    console.log('🎬 Starting avatar session...');
    await avatarSession.start(session, ctx.room, {
      livekitUrl: process.env.LIVEKIT_URL,
      livekitApiKey: process.env.LIVEKIT_API_KEY,
      livekitApiSecret: process.env.LIVEKIT_API_SECRET,
    });
    console.log('✅ Avatar session started successfully');

    // Start the agent session
    console.log('🎙️ Starting agent session...');
    await session.start(ctx.room);
    console.log('✅ Agent session started');

    // Generate initial greeting
    console.log('👋 Generating greeting...');
    await session.generateReply({
      instructions: `Greet the user warmly and introduce yourself as their AI assistant. 
      Mention that you have a visual avatar and you're here to help with whatever they need.`,
    });

    console.log('🎉 Agent is ready and waiting for user input!');
  },
});

// Configure and start the worker
console.log('⚙️  Configuring worker...');
const workerOptions = new WorkerOptions({
  agent,
});

console.log('🏃 Starting worker...');
cli.runApp(workerOptions);