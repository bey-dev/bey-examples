import asyncio
import os

import aiohttp
from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.openai.stt import OpenAISTTService
from pipecat.services.openai.tts import OpenAITTSService

from pipecat_bey.transport import BeyParams, BeyTransport

SYSTEM_PROMPT = (
    "You are Chatbot, a friendly, helpful robot. Your goal is to demonstrate your "
    "capabilities in a succinct way. Your output will be converted to audio so don't "
    "include special characters in your answers. Respond to what the user said in a "
    "creative and helpful way, but keep your responses brief. Start by introducing "
    "yourself. Keep all your responses to 12 words or fewer."
)


async def main() -> None:
    speech_to_text = OpenAISTTService()
    language_model = OpenAILLMService()
    text_to_speech = OpenAITTSService()

    # # Uncomment for latency optimization
    # # pip install 'pipecat-ai[azure,deepgram,elevenlabs]'
    # from deepgram import LiveOptions
    # from pipecat.services.azure.llm import AzureLLMService
    # from pipecat.services.deepgram.stt import DeepgramSTTService
    # from pipecat.services.elevenlabs.tts import ElevenLabsTTSService
    #
    # speech_to_text = DeepgramSTTService(
    #     api_key=os.environ["DEEPGRAM_API_KEY"],
    #     live_options=LiveOptions(
    #         model="nova-3-general",
    #         language="en-US",
    #         smart_format=True,
    #         vad_events=True,
    #     ),
    # )
    # language_model = AzureLLMService(
    #     api_key=os.environ["AZURE_OPENAI_API_KEY"],
    #     endpoint="https://your.own.azure.com",
    #     model="gpt-4o-mini",
    #     api_version="2025-01-01-preview",
    # )
    # text_to_speech = ElevenLabsTTSService(
    #     api_key=os.environ["ELEVEN_API_KEY"],
    #     voice_id="21m00Tcm4TlvDq8ikWAM",
    #     model="eleven_flash_v2_5",
    # )

    context = OpenAILLMContext(messages=[{"role": "system", "content": SYSTEM_PROMPT}])
    context_aggregator = language_model.create_context_aggregator(context)

    async with aiohttp.ClientSession() as session:
        bey_transport = BeyTransport(
            bot_name="Pipecat bot",
            session=session,
            bey_api_key=os.environ["BEY_API_KEY"],
            daily_api_key=os.environ["DAILY_API_KEY"],
            avatar_id=os.environ["BEY_AVATAR_ID"],
            room_url=os.environ["DAILY_ROOM_URL"],
            params=BeyParams(
                vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
            ),
        )

        pipeline = Pipeline(
            [
                bey_transport.input(),
                speech_to_text,
                context_aggregator.user(),
                language_model,
                text_to_speech,
                bey_transport.output(),
                context_aggregator.assistant(),
            ]
        )

        task = PipelineTask(
            pipeline,
            # # Uncomment for metrics in logs
            # # from pipecat.pipeline.task import PipelineParams
            # params=PipelineParams(
            #     enable_metrics=True,
            #     enable_usage_metrics=True,
            # ),
        )

        @bey_transport.event_handler("on_client_connected")
        async def on_client_connected(transport, participant):
            logger.info("Client connected")
            context.add_message(
                {
                    "role": "system",
                    "content": "Start by greeting the user and ask how you can help.",
                }
            )
            await task.queue_frames([LLMRunFrame()])

        @bey_transport.event_handler("on_client_disconnected")
        async def on_client_disconnected(transport, participant):
            logger.info("Client disconnected")
            await task.cancel()

        runner = PipelineRunner()
        await runner.run(task)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
