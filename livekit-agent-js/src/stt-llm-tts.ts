import 'dotenv/config';
import { type JobContext, WorkerOptions, cli, defineAgent, voice } from '@livekit/agents';
import * as bey from '@livekit/agents-plugin-bey';
import * as openai from '@livekit/agents-plugin-openai';
import * as silero from '@livekit/agents-plugin-silero';
import { fileURLToPath } from 'node:url';
import { log } from '@livekit/agents';

/**
 * Bey Avatar Agent with STT/LLM/TTS Pipeline
 *
 * This example demonstrates:
 * - Using separate STT, LLM, and TTS components instead of Realtime API
 * - Voice Activity Detection (VAD) for detecting when users are speaking
 * - More control over each stage of the conversation pipeline
 * - Custom configuration for speech recognition, language model, and synthesis
 *
 * This approach is useful when you need:
 * - Different providers for STT/TTS/LLM
 * - More granular control over each component
 * - Custom processing between pipeline stages
 */

export default defineAgent({
  entry: async (ctx: JobContext) => {
    const logger = log();
    logger.info('Starting Bey Avatar Agent with STT/LLM/TTS', { room: ctx.room.name });

    const agent = new voice.Agent({
      instructions: `You are a friendly and helpful AI assistant with a visual avatar.
        Keep your responses natural, conversational, and concise.
        Respond directly to what users ask without unnecessary elaboration.`,
      vad: await silero.VAD.load(),
    });

    // Configure the agent session with separate STT, LLM, and TTS
    const session = new voice.AgentSession({
      stt: new openai.STT({
        model: 'whisper-1',
        language: 'en',
      }),

      llm: new openai.LLM({
        model: 'gpt-4o',
        temperature: 0.8,
      }),

      tts: new openai.TTS({
        voice: 'alloy', 
        model: 'tts-1',
        speed: 1.0,
      }),
    });

    await ctx.connect();
    logger.info('Connected to room', { room: ctx.room.name });

    await session.start({
      agent,
      room: ctx.room,
    });
    logger.info('Agent session started with STT/LLM/TTS pipeline');

    const avatarId = process.env.BEY_AVATAR_ID;
    const avatar = new bey.AvatarSession({
      avatarId: avatarId || undefined,
    });

    await avatar.start(session, ctx.room);
    logger.info('Avatar session started');

    session.generateReply({
      instructions: `Greet the user warmly and let them know you're ready to help.`,
    });

    logger.info('Agent is ready');
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
