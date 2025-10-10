import 'dotenv/config';
import { type JobContext, WorkerOptions, cli, defineAgent, voice } from '@livekit/agents';
import * as bey from '@livekit/agents-plugin-bey';
import * as openai from '@livekit/agents-plugin-openai';
import { fileURLToPath } from 'node:url';

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

export default defineAgent({
  entry: async (ctx: JobContext) => {
    console.log('🚀 Starting Bey Avatar Agent...');

    // Create the voice agent with instructions
    const agent = new voice.Agent({
      instructions: `You are a friendly and helpful AI assistant with a visual avatar.
        You can see and interact with users through your avatar.
        Keep your responses natural and conversational.
        When users join, warmly greet them and ask how you can help.`,
    });

    // Create the agent session with OpenAI Realtime
    console.log('🤖 Creating agent session with OpenAI Realtime...');
    const session = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        voice: 'alloy', // Options: alloy, echo, fable, onyx, nova, shimmer
        temperature: 0.8,
      }),
    });

    // Connect to the LiveKit room
    await ctx.connect();
    console.log('✅ Connected to room:', ctx.room.name);

    // Start the agent session
    console.log('🎙️ Starting agent session...');
    await session.start({
      agent,
      room: ctx.room,
    });
    console.log('✅ Agent session started');

    // Initialize the Bey avatar session
    console.log('🎭 Initializing Bey avatar...');
    const avatarId = process.env.BEY_AVATAR_ID;
    const avatar = new bey.AvatarSession({
      avatarId: avatarId || undefined,
    });

    // Start the avatar (this will make the avatar join the room)
    console.log('🎬 Starting avatar session...');
    await avatar.start(session, ctx.room);
    console.log('✅ Avatar session started successfully');

    // Generate initial greeting
    console.log('👋 Generating greeting...');
    session.generateReply({
      instructions: `Greet the user warmly and introduce yourself as their AI assistant.
      Mention that you have a visual avatar and you're here to help with whatever they need.`,
    });

    console.log('🎉 Agent is ready and waiting for user input!');
  },
});

// Configure and start the worker
console.log('⚙️  Configuring worker...');
cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));