import asyncio
import logging
from typing import Optional
from pipecat.services.ai_service import AIService
from pipecat.frames.frames import (
    CancelFrame,
    EndFrame,
    Frame,
    OutputAudioRawFrame,
    OutputImageRawFrame,
    StartFrame,
    StartInterruptionFrame,
    TTSAudioRawFrame,
    SpeechOutputAudioRawFrame,
)
from pipecat.audio.utils import create_stream_resampler
from pipecat.processors.frame_processor import FrameDirection, FrameProcessorSetup
from pipecat.transports.services.daily import DailyTransportClient

FRAME_RATE = 25

class BeyVideoService(AIService):
    def __init__(
        self,
        client: DailyTransportClient,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._resampler = create_stream_resampler()
        self._queue = asyncio.Queue()
        self.out_sample_rate = 16000
        self._audio_buffer = bytearray()
        self.client = client
        self._transport_destination: str = "stream"
        
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, StartFrame):
            await self.client.register_audio_destination(self._transport_destination)
            await self.push_frame(frame, direction)
        elif isinstance(frame, TTSAudioRawFrame):
            in_sample_rate = frame.sample_rate
            chunk_size = int((self.out_sample_rate * 2) / FRAME_RATE)

            resampled = await self._resampler.resample(frame.audio, in_sample_rate, self.out_sample_rate)
            self._audio_buffer.extend(resampled)
            while len(self._audio_buffer) >= chunk_size:
                chunk = SpeechOutputAudioRawFrame(
                    bytes(self._audio_buffer[:chunk_size]),
                    sample_rate=self.out_sample_rate,
                    num_channels=frame.num_channels,
                )
                
                chunk.transport_destination = self._transport_destination

                self._audio_buffer = self._audio_buffer[chunk_size:]
                await self.client.write_audio_frame(chunk)
        else:
            await self.push_frame(frame, direction)
            
