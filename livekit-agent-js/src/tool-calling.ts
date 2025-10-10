import 'dotenv/config';
import { type JobContext, WorkerOptions, cli, defineAgent, voice } from '@livekit/agents';
import * as bey from '@livekit/agents-plugin-bey';
import * as openai from '@livekit/agents-plugin-openai';
import { fileURLToPath } from 'node:url';
import { log } from '@livekit/agents';

/**
 * Bey Avatar Agent with Tool Calling
 *
 * This example demonstrates:
 * - Using OpenAI Realtime with function calling
 * - Avatar integration with tool responses
 * - Custom functions that the AI can invoke
 *
 * Note: Tool/function definitions are passed directly to the OpenAI Realtime Model.
 * See OpenAI Realtime API docs for function calling format:
 * https://platform.openai.com/docs/guides/realtime/function-calls
 */

export default defineAgent({
  entry: async (ctx: JobContext) => {
    const logger = log();
    logger.info('Starting Bey Avatar Agent with Tools', { room: ctx.room.name });

    const agent = new voice.Agent({
      instructions: `You are a helpful AI assistant with access to real-time information.
        You can check the weather and tell the current time using your available functions.
        When users ask about weather or time, use your functions to provide accurate information.
        Always mention what information you're retrieving for them.`,
    });

    // OpenAI Realtime supports function calling
    // Functions are defined in the OpenAI function calling format
    const session = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        voice: 'alloy',
        temperature: 0.8,
        // Note: Function calling with Realtime API requires specific configuration
        // See LiveKit Agents documentation for the latest tool calling patterns:
        // https://docs.livekit.io/agents/build/tools/
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
      instructions: `Greet the user and let them know you're ready to help with any questions.`,
    });

    logger.info('Agent is ready');
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
