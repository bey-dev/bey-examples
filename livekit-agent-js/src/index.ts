import 'dotenv/config';
import { type JobContext, WorkerOptions, cli, defineAgent, voice } from '@livekit/agents';
import * as bey from '@livekit/agents-plugin-bey';
import * as openai from '@livekit/agents-plugin-openai';
import { fileURLToPath } from 'node:url';
import { log } from '@livekit/agents';

/**
 * Basic Bey Avatar Agent with OpenAI Realtime
 *
 * This example demonstrates:
 * - Setting up a voice agent with Bey avatar integration
 * - Using OpenAI Realtime API for natural conversation
 * - Basic session management and error handling
 */

export default defineAgent({
  entry: async (ctx: JobContext) => {
    const logger = log();
    logger.info('Starting Bey Avatar Agent', { room: ctx.room.name });

    const agent = new voice.Agent({
      instructions: `You are a friendly and helpful AI assistant with a visual avatar.
        You can see and interact with users through your avatar.
        Keep your responses natural and conversational.
        When users join, warmly greet them and ask how you can help.`,
    });

    const session = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        voice: 'alloy',
        temperature: 0.8,
      }),
    });

    await ctx.connect();
    logger.info('Connected to room', { room: ctx.room.name });

    await session.start({
      agent,
      room: ctx.room,
    });
    logger.info('Agent session started');

    const avatarId = process.env.BEY_AVATAR_ID;
    const avatar = new bey.AvatarSession({
      avatarId: avatarId || undefined,
    });

    await avatar.start(session, ctx.room);
    logger.info('Avatar session started');

    session.generateReply({
      instructions: `Greet the user warmly and introduce yourself as their AI assistant.
      Mention that you have a visual avatar and you're here to help with whatever they need.`,
    });

    logger.info('Agent is ready');
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));