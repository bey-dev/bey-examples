import asyncio
import os
from typing import Any

import aiohttp
from dotenv import load_dotenv
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.openai.stt import OpenAISTTService
from pipecat.services.openai.tts import OpenAITTSService
from pipecat.transports.daily.transport import DailyParams, DailyTransport
from pipecat.transports.daily.utils import (
    DailyRESTHelper,
    DailyMeetingTokenParams,
    DailyMeetingTokenProperties,
)

from bey_video import BeyVideoService


# Ege stock avatar
# Ref: https://docs.bey.dev/get-started/avatars/default
AVATAR_ID = "b9be11b8-89fb-4227-8f86-4a881393cbdb"

SYSTEM_PROMPT = (
    "You are Chatbot, a friendly, helpful robot. Your goal is to demonstrate your "
    "capabilities in a succinct way. Your output will be converted to audio so don't "
    "include special characters in your answers. Respond to what the user said in a "
    "creative and helpful way, but keep your responses brief. Start by introducing "
    "yourself. Keep all your responses to 12 words or fewer."
)


async def main() -> None:
    bey_api_key = os.environ["BEY_API_KEY"]

    daily_room_url = os.environ["DAILY_ROOM_URL"]
    daily_api_key = os.environ["DAILY_API_KEY"]

    openai_api_key = os.environ["OPENAI_API_KEY"]

    speech_to_text = OpenAISTTService(api_key=openai_api_key)
    language_model = OpenAILLMService(api_key=openai_api_key)
    text_to_speech = OpenAITTSService(api_key=openai_api_key)

    # ADVANCED CONFIGURATION
    # Use this to optimize for latency
    # from pipecat.services.deepgram.stt import DeepgramSTTService
    # from deepgram import LiveOptions
    # from pipecat.services.elevenlabs.tts import ElevenLabsTTSService
    # from pipecat.services.azure.llm import AzureLLMService
    #
    # deepgram_api_key = os.environ["DEEPGRAM_API_KEY"]
    # eleven_api_key = os.environ["ELEVEN_API_KEY"]
    # azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    #
    # speech_to_text = DeepgramSTTService(
    #     api_key=deepgram_api_key,
    #     live_options=LiveOptions(
    #         model="nova-3-general",
    #         language="en-US",
    #         smart_format=True,
    #         vad_events=True,
    #     ),
    # )
    # language_model = AzureLLMService(
    #     api_key=azure_openai_api_key,
    #     endpoint="https://your.own.azure.com",
    #     model="gpt-4o-mini",
    #     api_version="2025-01-01-preview",
    # )
    # text_to_speech = ElevenLabsTTSService(
    #     api_key=eleven_api_key,
    #     voice_id="21m00Tcm4TlvDq8ikWAM",
    #     model="eleven_flash_v2_5",
    # )

    context = OpenAILLMContext([{"role": "system", "content": SYSTEM_PROMPT}])
    context_aggregator = language_model.create_context_aggregator(context)

    async with aiohttp.ClientSession() as session:
        daily_rest_helper = DailyRESTHelper(
            daily_api_key=daily_api_key,
            aiohttp_session=session,
        )

        voice_bot_name = "My Voice Bot"
        video_bot_name = "My Video Bot"

        token = await daily_rest_helper.get_token(
            room_url=daily_room_url,
            params=DailyMeetingTokenParams(
                properties=DailyMeetingTokenProperties(user_name=voice_bot_name),
            ),
            expiry_time=3600,  # 1 hour
        )

        transport = DailyTransport(
            room_url=daily_room_url,
            token=token,
            bot_name=voice_bot_name,
            params=DailyParams(
                audio_in_enabled=True,
                video_out_enabled=False,
                video_out_is_live=False,
                microphone_out_enabled=False,
                vad_analyzer=SileroVADAnalyzer(),
            ),
        )

        speech_to_video = BeyVideoService(
            api_key=bey_api_key,
            avatar_id=AVATAR_ID,
            bot_name=video_bot_name,
            # we stream audio to a video bot in the Daily room, so we need this
            transport_client=transport._client,
            # video bot joins the room remotely on demand, we need these to manage it
            rest_helper=daily_rest_helper,
            session=session,
        )

        pipeline = Pipeline(
            [
                transport.input(),
                speech_to_text,
                context_aggregator.user(),
                language_model,
                text_to_speech,
                speech_to_video,
                transport.output(),
                context_aggregator.assistant(),
            ]
        )

        task = PipelineTask(
            pipeline,
            params=PipelineParams(
                enable_metrics=True,
                enable_usage_metrics=True,
            ),
        )

        @transport.event_handler("on_participant_joined")
        async def handle_participant_joined(transport, participant: dict[str, Any]):
            if participant["info"]["userName"] == video_bot_name:
                await transport.update_subscriptions(
                    participant_settings={
                        participant["id"]: {"media": {"microphone": "unsubscribed"}}
                    }
                )
                return

            context.add_message(
                {
                    "role": "system",
                    "content": "Please introduce yourself to the user.",
                }
            )

            await task.queue_frames([context_aggregator.user().get_context_frame()])

        @transport.event_handler("on_participant_left")
        async def handle_participant_left(
            transport, participant: dict[str, Any], reason: str
        ):
            await task.cancel()

        runner = PipelineRunner()
        await runner.run(task)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
