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
      llm: new openai.realtime.RealtimeModel({ voice: "alloy" }),
    });

    const voiceAgent = new voice.Agent({
      instructions: "You are a friendly AI with a visual avatar",
    });

    const beyAvatarSession = beyAvatarId
      ? new bey.AvatarSession({ beyAvatarId })
      : new bey.AvatarSession();

    await voiceAgentSession.start({ agent: voiceAgent, room: ctx.room });

    await beyAvatarSession.start(voiceAgentSession, ctx.room);
  },
});

// Overwrite args for the LiveKit CLI
process.argv = [process.argv[0], process.argv[1], "dev"];

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
