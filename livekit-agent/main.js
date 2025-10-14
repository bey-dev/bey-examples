import { fileURLToPath } from "node:url";
import {
  JobContext,
  WorkerOptions,
  cli,
  defineAgent,
  voice,
} from "@livekit/agents";
import * as bey from "@livekit/agents-plugin-bey";
import * as openai from "@livekit/agents-plugin-openai";

const beyAvatarId = process.env.BEY_AVATAR_ID;

export default defineAgent({
  entry: async (ctx) => {
    await ctx.connect();

    const voiceAgentSession = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        // Use a voice that matches your avatar
        // Ref: https://platform.openai.com/docs/guides/text-to-speech#voice-options
        // voice: "alloy",
      }),

      // // Uncomment for STT/LLM/TTS configuration
      // // You can also swap in different providers for each service or build your own
      // // See supported providers for:
      // // - STT: https://docs.livekit.io/agents/models/stt/#plugins
      // // - LLM: https://docs.livekit.io/agents/models/llm/#plugins
      // // - TTS: https://docs.livekit.io/agents/models/tts/#plugins
      // stt: new openai.STT({ model: 'whisper-1', language: 'en' }),
      // llm: new openai.LLM({ model: 'gpt-4o', temperature: 0.8 }),
      // tts: new openai.TTS({ model: 'tts-1', voice: 'alloy', speed: 1.2 }),

      // // Uncomment for Silero VAD (better detects when to start/stop talking)
      // // Ref: https://docs.livekit.io/agents/build/turns/vad
      // // pnpm install @livekit/agents-plugin-silero
      // // import * as silero from '@livekit/agents-plugin-silero';
      // vad: await silero.VAD.load(),
    });

    const voiceAgent = new voice.Agent({
      instructions: "You are a friendly AI with a visual avatar",
    });

    // // Uncomment for tool calling
    // // Ref: https://docs.livekit.io/agents/build/tools
    // import { llm } from '@livekit/agents';
    //
    // const voiceAgent = new voice.Agent({
    //   instructions: "You are a friendly AI with a visual avatar",
    //   tools: {
    //     lookupWeather: llm.tool({
    //       description: 'Look up weather information for a given location.',
    //       parameters: {
    //         type: "object",
    //         properties: {
    //           location: {
    //             type: "string",
    //             description: "The location to look up weather information for."
    //           }
    //         }
    //       },
    //       execute: async ({ location }, { ctx }) => {
    //         // Implement tool here
    //         return { weather: "sunny", temperature: 70 };
    //       },
    //     }),
    //   },
    // });

    const beyAvatarSession = new bey.AvatarSession({ beyAvatarId })

    await voiceAgentSession.start({ agent: voiceAgent, room: ctx.room });
    await beyAvatarSession.start(voiceAgentSession, ctx.room);
  },
});

// Overwrite args for the LiveKit CLI
process.argv = [process.argv[0], process.argv[1], "dev"];
cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
