import argparse
import asyncio
import os
from typing import Optional
import aiohttp
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.pipeline.pipeline import Pipeline
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.services.daily import DailyParams, DailyTransport
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.deepgram.tts import DeepgramTTSService
from pipecat.transports.services.helpers.daily_rest import DailyRESTHelper
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.deepgram.stt import LiveOptions
from dotenv import load_dotenv
from integration_code import BeyVideoService


async def configure_with_args(
    aiohttp_session: aiohttp.ClientSession,
    parser: Optional[argparse.ArgumentParser] = None,
):
    if not parser:
        parser = argparse.ArgumentParser(description="Daily AI SDK Bot Sample")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=False,
        help="URL of the Daily room to join",
    )
    parser.add_argument(
        "-k",
        "--apikey",
        type=str,
        required=False,
        help="Daily API Key (needed to create an owner token for the room)",
    )

    args, unknown = parser.parse_known_args()

    url = args.url or os.getenv("DAILY_SAMPLE_ROOM_URL")
    key = args.apikey or os.getenv("DAILY_API_KEY")

    if not url:
        raise Exception(
            "No Daily room specified. use the -u/--url option from the command line, or set DAILY_SAMPLE_ROOM_URL in your environment to specify a Daily room URL."
        )

    if not key:
        raise Exception(
            "No Daily API key specified. use the -k/--apikey option from the command line, or set DAILY_API_KEY in your environment to specify a Daily API key, available from https://dashboard.daily.co/developers."
        )

    daily_rest_helper = DailyRESTHelper(
        daily_api_key=key,
        daily_api_url=os.getenv("DAILY_API_URL", "https://api.daily.co/v1"),
        aiohttp_session=aiohttp_session,
    )

    # Create a meeting token for the given room with an expiration 1 hour in
    # the future.
    expiry_time: float = 60 * 60

    token = await daily_rest_helper.get_token(url, expiry_time)

    return (url, token, args)


async def main():
    async with aiohttp.ClientSession() as session:
        (room_url, token, _) = await configure_with_args(session)

        stt = DeepgramSTTService(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
            live_options=LiveOptions(
                model="nova-2-general",
                language="en-US",
                smart_format=True,
                vad_events=True,
            ),
        )

        llm = OpenAILLMService(
            api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini"
        )

        tts = DeepgramTTSService(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
        )

        messages = [
            {
                "role": "system",
                "content": "You are Chatbot, a friendly, helpful robot. Your goal is to demonstrate your capabilities in a succinct way. Your output will be converted to audio so don't include special characters in your answers. Respond to what the user said in a creative and helpful way, but keep your responses brief. Start by introducing yourself. Keep all your responses to 12 words or fewer.",
            },
        ]
        context = OpenAILLMContext(messages)

        context_aggregator = llm.create_context_aggregator(context)

        transport = DailyTransport(
            room_url,
            token,
            "Bey example Bot",
            DailyParams(
                audio_in_enabled=True,
                video_out_enabled=False,
                video_out_is_live=False,
                microphone_out_enabled=False,
                vad_analyzer=SileroVADAnalyzer(),
            ),
        )
        
        
        bey = BeyVideoService(client=transport._client)

        pipeline = Pipeline(
            [
                transport.input(),
                stt,
                context_aggregator.user(),
                llm,
                tts,
                bey,
                transport.output(),
                context_aggregator.assistant(),
            ],
        )

        task = PipelineTask(
            pipeline,
            params=PipelineParams(
                audio_out_sample_rate=16000,
            ),
        )

        @transport.event_handler("on_participant_joined")
        async def on_participant_joined(transport, participant):
            # Kick off the conversation.
            if participant["info"]["userName"] == "Bey Video Bot":
                await transport.update_subscriptions(participant_settings={participant["id"]: {"media": {"microphone": "unsubscribed"}}})
                return

            messages.append(
                {
                    "role": "system",
                    "content": "Please introduce yourself to the user.",
                }
            )

            await task.queue_frames(
                [context_aggregator.user().get_context_frame()]
            )

        @transport.event_handler("on_participant_left")
        async def on_participant_left(transport, participant, reason):
            await task.cancel()

        runner = PipelineRunner()
        await runner.run(task)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())