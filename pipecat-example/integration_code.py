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
from pipecat.audio.utils import create_default_resampler
from pipecat.processors.frame_processor import FrameDirection, FrameProcessorSetup
from pipecat.transports.services.daily import DailyTransportClient

class BeyVideoService(AIService):
    def __init__(
        self,
        client: DailyTransportClient,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._resampler = create_default_resampler()
        self._queue = asyncio.Queue()
        self.out_sample_rate=16000
        self._audio_buffer = bytearray()
        self.client = client
        self._transport_destination: str = "stream"
        
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, StartInterruptionFrame):
            # await self._handle_interruptions()
            await self.push_frame(frame, direction)
        elif isinstance(frame, StartFrame):
            await self.client.register_audio_destination(self._transport_destination)
            await self.push_frame(frame, direction)
        elif isinstance(frame, TTSAudioRawFrame):
            print(f"Received TTS audio frame: {frame}")
            sample_rate = self.out_sample_rate
            chunk_size = int((sample_rate * 2) / 25)

            resampled = await self._resampler.resample(frame.audio, frame.sample_rate, sample_rate)
            self._audio_buffer.extend(resampled)
            while len(self._audio_buffer) >= chunk_size:
                chunk = SpeechOutputAudioRawFrame(
                    bytes(self._audio_buffer[:chunk_size]),
                    sample_rate=sample_rate,
                    num_channels=frame.num_channels,
                )
                
                chunk.transport_destination = self._transport_destination

                self._audio_buffer = self._audio_buffer[chunk_size:]
                await self.client.write_audio_frame(chunk)
                await self.push_frame(chunk, direction)
        else:
            await self.push_frame(frame, direction)
            
