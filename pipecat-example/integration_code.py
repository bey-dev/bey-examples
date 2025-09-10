import asyncio
import os
import aiohttp
from pipecat.services.ai_service import AIService
from pipecat.frames.frames import (
    BotStartedSpeakingFrame,
    Frame,
    StartFrame,
    TTSAudioRawFrame,
    TTSStartedFrame,
    SpeechOutputAudioRawFrame,
    StartInterruptionFrame,
    TransportMessageFrame,
)
from pipecat.audio.utils import create_stream_resampler
from pipecat.processors.frame_processor import FrameDirection
from pipecat.transports.services.daily import DailyTransportClient

FRAME_RATE = 25
_EGE_STOCK_AVATAR_ID = "b9be11b8-89fb-4227-8f86-4a881393cbdb"
_DEFAULT_API_URL = "https://api.bey.dev"

class BeyVideoService(AIService):
    def __init__(
        self,
        client: DailyTransportClient,
        avatar_id: str = _EGE_STOCK_AVATAR_ID,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._resampler = create_stream_resampler()
        self._queue = asyncio.Queue()
        self._out_sample_rate = 16000
        self._audio_buffer = bytearray()
        self._client = client
        self._transport_destination: str = "bey-custom-track"
        self._http_session: aiohttp.ClientSession | None = None
        self._avatar_id = avatar_id
        self._api_url = os.getenv("BEY_API_URL", _DEFAULT_API_URL)
        self._api_key = os.getenv("BEY_API_KEY", _EGE_STOCK_AVATAR_ID)

    def _ensure_http_session(self) -> aiohttp.ClientSession:
        if self._http_session is None:
            self._http_session = aiohttp.ClientSession()

        return self._http_session

    async def _start(self, room_url: str, token: str) -> None:
        async with self._ensure_http_session().post(
            f"{self._api_url}/v1/session",
            headers={
                "x-api-key": self._api_key,
            },
            json={
                "avatar_id": self._avatar_id,
                "pipecat_url": room_url,
                "pipecat_token": token,
            },
        ) as response:
            if not response.ok:
                text = await response.text()
                raise Exception(
                    "Server returned an error", status_code=response.status, body=text
                )
            return
        
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, StartFrame):
            await self._start(room_url=self._client.room_url, token=self._client._token)
            await self._client.register_audio_destination(self._transport_destination)
            await self.push_frame(frame, direction)
        elif isinstance(frame, StartInterruptionFrame):
            frame.transport_destination = self._transport_destination
            transport_frame = TransportMessageFrame(message="interrupt")
            await self._client.send_message(transport_frame)
        elif isinstance(frame, TTSAudioRawFrame):
            in_sample_rate = frame.sample_rate
            chunk_size = int((self._out_sample_rate * 2) / FRAME_RATE)

            resampled = await self._resampler.resample(frame.audio, in_sample_rate, self._out_sample_rate)
            self._audio_buffer.extend(resampled)
            while len(self._audio_buffer) >= chunk_size:
                chunk = SpeechOutputAudioRawFrame(
                    bytes(self._audio_buffer[:chunk_size]),
                    sample_rate=self._out_sample_rate,
                    num_channels=frame.num_channels,
                )
                
                chunk.transport_destination = self._transport_destination

                self._audio_buffer = self._audio_buffer[chunk_size:]
                await self._client.write_audio_frame(chunk)
        elif isinstance(frame, TTSStartedFrame):
            await self.start_ttfb_metrics()
        elif isinstance(frame, BotStartedSpeakingFrame):
            # We constantly receive audio through WebRTC, but most of the time it is silence.
            # As soon as we receive actual audio, the base output transport will create a
            # BotStartedSpeakingFrame, which we can use as a signal for the TTFB metrics.
            await self.stop_ttfb_metrics()
        else:
            await self.push_frame(frame, direction)
            
    def can_generate_metrics(self) -> bool:
        """Check if the service can generate metrics.

        Returns:
            True if metrics generation is supported.
        """
        return True
            
