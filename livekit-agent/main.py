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
        llm=openai.realtime.RealtimeModel(voice="ash")
    )

    voice_agent = Agent(instructions="You are a friendly AI with a visual avatar")

    bey_avatar_id = os.environ["BEY_AVATAR_ID"]
    if avatar_id != "":
        bey_avatar_session = bey.AvatarSession(avatar_id=bey_avatar_id)
    else:
        bey_avatar_session = bey.AvatarSession()

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
