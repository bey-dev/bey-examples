import argparse
import os
import sys

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    RoomOutputOptions,
    WorkerOptions,
    WorkerType,
    cli,
)
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import bey, openai


async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    voice_agent_session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            # Use a voice that matches your avatar
            # Ref: https://platform.openai.com/docs/guides/text-to-speech#voice-options
            # voice="alloy",
        ),

        # # Uncomment for STT/LLM/TTS configuration
        # # You can also swap in different providers for each service or build your own
        # # See supported providers for:
        # # - STT: https://docs.livekit.io/agents/models/stt/#plugins
        # # - LLM: https://docs.livekit.io/agents/models/llm/#plugins
        # # - TTS: https://docs.livekit.io/agents/models/tts/#plugins
        # stt=openai.STT(model="whisper-1", language="en"),
        # llm=openai.LLM(model="gpt-4o", temperature=0.8),
        # tts=openai.TTS(model="tts-1", voice="alloy", speed=1.2),

        # # Uncomment for Silero VAD (better detects when to start/stop talking)
        # # Ref: https://docs.livekit.io/agents/build/turns/vad
        # # pip install 'livekit-agents[silero]'
        # # from livekit.plugins import silero
        # vad=silero.VAD.load(),
    )


    voice_agent = Agent(
        instructions="You are helpful assistance with a visual presence."
    )

    # # Uncomment for tool calling
    # # Ref: https://docs.livekit.io/agents/build/tools
    # from livekit.agents import function_tool, Agent, RunContext
    #
    # class MyAgent(Agent):
    #     @function_tool()
    #     async def lookup_weather(self, context: RunContext, location: str) -> dict[str, Any]:
    #         """Look up weather information for a given location.
    #
    #         Args:
    #             location: The location to look up weather information for.
    #         """
    #         # Implement tool here
    #         return {"weather": "sunny", "temperature": 40}
    #
    # voice_agent = MyAgent(instructions="You are a friendly AI with a visual avatar")

    bey_avatar_session = bey.AvatarSession(avatar_id=os.environ["BEY_AVATAR_ID"])

    await voice_agent_session.start(agent=voice_agent, room=ctx.room)

    await bey_avatar_session.start(voice_agent_session, room=ctx.room)


if __name__ == "__main__":
    load_dotenv()

    sys.argv = [sys.argv[0], "dev"]  # overwrite args for the LiveKit CLI
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            worker_type=WorkerType.ROOM,
        )
    )
