import asyncio, os
from videosdk.agents import Agent, AgentSession, CascadingPipeline, JobContext, RoomOptions, WorkerJob,ConversationFlow
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.openai import OpenAILLM, OpenAITTS
from integration_code import BeyAvatar
from typing import AsyncIterator
from dotenv import load_dotenv

# Pre-downloading the Turn Detector model
pre_download_model()

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant that can answer questions and help with tasks.")
    async def on_enter(self): 
        await asyncio.sleep(6)
        await self.session.say("Hello! How can I help?")
    async def on_exit(self): await self.session.say("Goodbye!")
    
async def start_session(context: JobContext):
    # Create agent and conversation flow
    agent = MyVoiceAgent()
    conversation_flow = ConversationFlow(agent)

    # Create pipeline
    pipeline = CascadingPipeline(
        stt=DeepgramSTT(model="nova-2", language="en"),
        llm=OpenAILLM(model="gpt-4o"),
        tts=OpenAITTS(),
        vad=SileroVAD(threshold=0.35),
        turn_detector=TurnDetector(threshold=0.8),
        avatar=BeyAvatar(room_id=context.room_options.room_id, token=os.getenv("VIDEOSDK_AUTH_TOKEN")),
    )

    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
        conversation_flow=conversation_flow
    )

    try:
        await context.connect()
        await session.start()
        # Keep the session running until manually terminated
        await asyncio.Event().wait()
    finally:
        # Clean up resources when done
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    room_options = RoomOptions(
        # room_id="YOUR_MEETING_ID", # Set to join a pre-created room; omit to auto-create
        name="VideoSDK Cascaded Agent",
        playground=True
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    load_dotenv()

    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
