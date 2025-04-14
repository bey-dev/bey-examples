import argparse
import asyncio
import sys
from functools import partial
from typing import Optional

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    WorkerType,
    cli,
)
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, silero
from livekit.plugins.bey import start_bey_avatar_session


async def entrypoint(ctx: JobContext, avatar_id: Optional[str]) -> None:
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    if avatar_id is not None:
        avatar_session = await start_bey_avatar_session(
            ctx, avatar_id=avatar_id
        )
    else:
        avatar_session = await start_bey_avatar_session(ctx)

    await avatar_session.wait_for_avatar_agent()

    agent = Agent(instructions="Talk to me!")
    agent_session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )

    agent_session.output.audio = avatar_session.local_agent_audio_output
    await agent_session.start(
        agent=agent,
        room=ctx.room,
        room_output_options=avatar_session.local_agent_room_output_options,
    )

    await asyncio.sleep(2)
    await agent_session.say("Hello, how are you doing today?")


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Run a LiveKit agent with Bey avatar."
    )
    parser.add_argument("--avatar-id", type=str, help="Avatar ID to use.")
    args = parser.parse_args()

    sys.argv = [sys.argv[0], "dev"]  # overwrite args for the LiveKit CLI
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=partial(entrypoint, avatar_id=args.avatar_id),
            worker_type=WorkerType.ROOM,
        )
    )
