import 'dotenv/config';
import { type JobContext, WorkerOptions, cli, defineAgent, voice, llm } from '@livekit/agents';
import * as bey from '@livekit/agents-plugin-bey';
import * as openai from '@livekit/agents-plugin-openai';
import { fileURLToPath } from 'node:url';
import { log } from '@livekit/agents';
import { z } from 'zod';

/**
 * Bey Avatar Agent with Tool Calling
 *
 * This example demonstrates:
 * - Defining custom tools/functions using llm.tool
 * - Using Zod schemas for type-safe tool parameters
 * - Avatar integration with tool responses
 *
 * The agent can invoke the weather tool when users ask about weather conditions.
 */

// Custom Agent class with weather tool
class WeatherAgent extends voice.Agent {
  constructor() {
    super({
      instructions: `You are a helpful AI assistant with access to weather information.
        When users ask about the weather in a specific location, use your lookupWeather tool.
        Provide the weather information in a friendly, conversational way.`,
      tools: {
        lookupWeather: llm.tool({
          description: 'Look up current weather information for a given location.',
          parameters: z.object({
            location: z.string().describe('The city and state, e.g. San Francisco, CA'),
          }),
          execute: async ({ location }) => {
            // Call a weather API here
            // For this example, we'll return mock data
            const logger = log();
            logger.info('Looking up weather', { location });

            // Simulate weather API response
            const mockWeather = {
              location,
              weather: 'partly cloudy',
              temperatureF: Math.floor(Math.random() * 30) + 60,
              temperatureC: Math.floor(Math.random() * 15) + 15,
              humidity: Math.floor(Math.random() * 40) + 40,
              windSpeed: Math.floor(Math.random() * 15) + 5,
            };

            return {
              location: mockWeather.location,
              conditions: mockWeather.weather,
              temperature: `${mockWeather.temperatureF}°F (${mockWeather.temperatureC}°C)`,
              humidity: `${mockWeather.humidity}%`,
              windSpeed: `${mockWeather.windSpeed} mph`,
            };
          },
        }),
      },
    });
  }
}

export default defineAgent({
  entry: async (ctx: JobContext) => {
    const logger = log();
    logger.info('Starting Bey Avatar Agent with Weather Tool', { room: ctx.room.name });

    const agent = new WeatherAgent();

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
    logger.info('Agent session started with weather tool');

    const avatarId = process.env.BEY_AVATAR_ID;
    const avatar = new bey.AvatarSession({
      avatarId: avatarId || undefined,
    });

    await avatar.start(session, ctx.room);
    logger.info('Avatar session started');

    session.generateReply({
      instructions: `Greet the user and let them know you can help them check the weather for any location.`,
    });

    logger.info('Agent is ready with weather tool');
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
