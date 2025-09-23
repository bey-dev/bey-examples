import asyncio
import time
import traceback
from aiortc import AudioStreamTrack, MediaStreamTrack, VideoStreamTrack
from av import VideoFrame, AudioFrame
from av.audio.resampler import AudioResampler
import logging
import numpy as np
from bey import beyConfig, beyClient
from vsaiortc.mediastreams import MediaStreamError
from videosdk import CustomVideoTrack, CustomAudioTrack


logger = logging.getLogger(__name__)

# --- Constants ---
VIDEOSDK_AUDIO_SAMPLE_RATE = 48000
BEY_INPUT_SAMPLING_RATE = 16000

VIDEO_TIME_BASE = 90000

DEFAULT_BEY_HTTP_URL = "https://api.bey.dev"

bey_input_resampler = AudioResampler(
    format="s16", layout="mono", rate=BEY_INPUT_SAMPLING_RATE
)
videosdk_output_resampler = AudioResampler(
    format="s16", layout="stereo", rate=VIDEOSDK_AUDIO_SAMPLE_RATE
)


class BeyAudioTrack(CustomAudioTrack):
    def __init__(self, loop: asyncio.AbstractEventLoop, bey_client: beyClient):
        super().__init__()
        self.kind = "audio"
        self.loop = loop
        self._timestamp = 0
        self.bey_client = bey_client
        self.queue = asyncio.Queue()

    def interrupt(self):
        asyncio.ensure_future(self.bey_client.clearBuffer())

    async def recv(self) -> AudioFrame:
        """Return next audio frame to VideoSDK."""
        try:
            if self.readyState != "live":
                raise MediaStreamError
            frame = await self.queue.get()
            return frame

        except Exception:
            traceback.print_exc()
            return self._create_silence_frame()

    async def cleanup(self):
        self.interrupt()
        self.stop()

    def add_frame(self, frame: AudioFrame):
        """Add frame from bey stream - add AudioFrame directly to buffer with quality validation"""

        if frame is None:
            return
        try:
            for resampled_frame in videosdk_output_resampler.resample(frame):
                self.queue.put_nowait(resampled_frame)
        except asyncio.QueueEmpty:
            pass
        except Exception as e:
            logger.error(f"Error adding bey audio frame: {e}")


class BeyVideoTrack(CustomVideoTrack):
    def __init__(self, is_trinity_avatar=True):
        super().__init__()
        self.kind = "video"
        self.queue = asyncio.Queue()
        self._readyState = "live"
        self._frame_rate = 25

        self._shared_start_time = None

    @property
    def readyState(self):
        return self._readyState

    async def recv(self) -> VideoFrame:
        return await self.queue.get()

    def add_frame(self, frame: VideoFrame):
        self.queue.put_nowait(frame)


class BeyAvatar:
    def __init__(
        self,
        config: beyConfig,
        bey_url: str = DEFAULT_BEY_HTTP_URL,
        is_trinity_avatar: bool = False,
    ):
        """Initialize the bey Avatar plugin.

        Args:
            config (beyConfig): The configuration for the bey avatar.
            bey_url (str): The bey API URL. Defaults to "https://api.bey.ai".
            is_trinity_avatar (bool): Specify if the face id in the bey config is a trinity avatar to ensure synchronization
        """
        super().__init__()
        self.config = config
        self._stream_start_time = None
        self.video_track: BeyVideoTrack | None = None
        self.video_receiver_track: VideoStreamTrack | None = None
        self.audio_track: BeyAudioTrack | None = None
        self.audio_receiver_track: AudioStreamTrack | None = None
        self.run = True
        self._is_speaking = False
        self._avatar_speaking = False
        self._last_error = None
        self._stopping = False
        self._keep_alive_task = None
        self._last_audio_time = 0
        self._is_trinity_avatar = is_trinity_avatar
        self.bey_url = bey_url

    async def connect(self):
        loop = asyncio.get_event_loop()
        await self._initialize_connection()
        self.audio_track = BeyAudioTrack(loop, self.bey_client)
        self.video_track = BeyVideoTrack(self._is_trinity_avatar)
        if self._stream_start_time is None:
            self._stream_start_time = time.time()

        self._last_audio_time = time.time()
        self._keep_alive_task = asyncio.create_task(self._keep_alive_loop())

    async def mark_silent(self):
        self._avatar_speaking = False

    async def mark_speaking(self):
        self._avatar_speaking = True

    async def _initialize_connection(self):
        """Initialize connection with retry logic"""
        self.bey_client = beyClient(self.config, True, 0, self.bey_url)
        await self.bey_client.Initialize()
        while not hasattr(self.bey_client, "audioReceiver"):
            await asyncio.sleep(0.0001)
        self._register_track(self.bey_client.audioReceiver)
        self._register_track(self.bey_client.videoReceiver)
        self.bey_client.registerSilentEventCallback(self.mark_silent)
        self.bey_client.registerSpeakEventCallback(self.mark_speaking)

    def _register_track(self, track: MediaStreamTrack):
        if track.kind == "video":
            self.video_receiver_track: VideoStreamTrack = track
            asyncio.ensure_future(self._process_video_frames())
        elif track.kind == "audio":
            self.audio_receiver_track: AudioStreamTrack = track
            asyncio.ensure_future(self._process_audio_frames())

    async def _process_video_frames(self):
        """Simple video frame processing for real-time playback"""

        while self.run and not self._stopping:
            try:
                frame: VideoFrame = await self.video_receiver_track.recv()
                if frame is None:
                    continue
                self.video_track.add_frame(frame)
            except Exception as e:
                logger.error(f"bey: Video processing error: {e}")
                if not self.run or self._stopping:
                    break
                await asyncio.sleep(0.1)
                continue

    async def _process_audio_frames(self):
        """Simple audio frame processing for real-time playback"""

        while self.run and not self._stopping:
            try:
                frame: AudioFrame = await self.audio_receiver_track.recv()
                if frame is None:
                    logger.warning("bey: Received None audio frame, continuing...")
                    continue
                try:
                    self.audio_track.add_frame(frame)
                except Exception as frame_error:
                    logger.error(f"bey: Error processing audio frame: {frame_error}")
                    continue
            except Exception as e:
                logger.error(f"bey: Audio processing error: {e}")
                if not self.run or self._stopping:
                    break
                await asyncio.sleep(0.1)
                continue

    async def sendSilence(self, duration: float = 0.1875):
        """Send silence to bootstrap the connection"""
        await self.bey_client.ready.wait()
        await self.bey_client.sendSilence(duration)

    async def _speech_timeout_handler(self):
        try:
            await asyncio.sleep(0.2)
            if self._is_speaking:
                await self.bey_client.clearBuffer()
                self._is_speaking = False
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in speech timeout handler: {e}")

    async def handle_audio_input(self, audio_data: bytes):
        if not self.run or self._stopping:
            return
        if self.bey_client.ready.is_set():
            try:
                if len(audio_data) % 2 != 0:
                    audio_data = audio_data + b"\x00"

                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                input_frame = AudioFrame.from_ndarray(
                    audio_array.reshape(1, -1), format="s16", layout="mono"
                )
                input_frame.sample_rate = 24000

                resampled_frames = bey_input_resampler.resample(input_frame)
                for frame in resampled_frames:
                    resampled_data = frame.to_ndarray().tobytes()

                    await self.bey_client.send(resampled_data)

                    self._last_audio_time = time.time()

            except Exception as e:
                logger.error(f"Error processing/sending audio data: {e}")
        else:
            logger.error(
                f"bey: Cannot send audio - ws available: {self.bey_client is not None}, ready: {self.bey_client.ready.is_set()}"
            )

    async def aclose(self):
        if self._stopping:
            return
        self._stopping = True
        self.run = False

        if self._keep_alive_task and not self._keep_alive_task.done():
            self._keep_alive_task.cancel()

        try:
            await self.bey_client.stop()
        except Exception:
            pass

    async def _keep_alive_loop(self):
        """Send periodic keep-alive audio to maintain bey session"""

        while self.run and not self._stopping:
            try:
                current_time = time.time()
                if current_time - self._last_audio_time > 5.0:
                    if self.bey_client.ready.is_set():
                        try:
                            self._last_audio_time = current_time
                            await self.bey_client.sendSilence()

                        except Exception as e:
                            print(f"bey: Keep-alive send failed: {e}")

                await asyncio.sleep(3.0)

            except Exception:
                if not self.run or self._stopping:
                    break
                await asyncio.sleep(1.0)