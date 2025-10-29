import type { RoomConnectOptions, RoomOptions, ChatMessage } from 'livekit-client';
import {
  ConnectionState,
  DisconnectReason,
  Participant,
  ParticipantEvent,
  RemoteParticipant,
  Room,
  RoomEvent,
  Track,
  TrackPublication,
  VideoPresets,
  isLocalParticipant,
  setLogLevel,
  LogLevel,
} from 'livekit-client';

setLogLevel(LogLevel.info);

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

const BEY_API_URL = 'https://api.bey.dev/v1/calls';

interface BeyCallResponse {
  id: string;
  agent_id: string;
  tags: Record<string, unknown>;
  started_at: string;
  ended_at: string | null;
  livekit_url: string;
  livekit_token: string;
}

let currentRoom: Room | undefined;
let currentCallId: string | undefined;

const state = {
  chatMessages: [] as Array<{ from: string; message: string; timestamp: number }>,
};
const appActions = {
  startCall: async () => {
    const apiKey = ($('api-key') as HTMLInputElement).value.trim();
    const agentId = ($('agent-id') as HTMLInputElement).value.trim();

    if (!apiKey || !agentId) {
      showStatus('error', 'Please enter both API Key and Agent ID');
      return;
    }

    try {
      setButtonDisabled('start-call-button', true);
      showStatus('info', 'Starting call...');
      appendLog('Creating new call session...');

      const response = await fetch(BEY_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
        },
        body: JSON.stringify({
          agent_id: agentId,
        }),
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`API request failed: ${response.status} - ${errorData}`);
      }

      const callData: BeyCallResponse = await response.json();
      currentCallId = callData.id;

      appendLog(`Call created: ${callData.id}`);
      appendLog(`Connecting to room...`);

      await connectToLiveKit(callData.livekit_url, callData.livekit_token);

      showStatus('success', `Connected! Call ID: ${callData.id}`);
      setButtonsForState(true);
    } catch (error: any) {
      appendLog(`Error: ${error.message}`);
      showStatus('error', `Failed to start call: ${error.message}`);
      setButtonDisabled('start-call-button', false);
    }
  },

  toggleAudio: async () => {
    if (!currentRoom) return;
    const enabled = currentRoom.localParticipant.isMicrophoneEnabled;
    setButtonDisabled('toggle-audio-button', true);

    try {
      await currentRoom.localParticipant.setMicrophoneEnabled(!enabled);
      appendLog(`Microphone ${!enabled ? 'enabled' : 'disabled'}`);
      updateButtonsForPublishState();
    } catch (error: any) {
      appendLog(`Error toggling audio: ${error.message}`);
    }

    setButtonDisabled('toggle-audio-button', false);
  },

  toggleVideo: async () => {
    if (!currentRoom) return;
    const enabled = currentRoom.localParticipant.isCameraEnabled;
    setButtonDisabled('toggle-video-button', true);

    try {
      await currentRoom.localParticipant.setCameraEnabled(!enabled);
      appendLog(`Camera ${!enabled ? 'enabled' : 'disabled'}`);
      renderParticipant(currentRoom.localParticipant);
      updateButtonsForPublishState();
    } catch (error: any) {
      appendLog(`Error toggling video: ${error.message}`);
    }

    setButtonDisabled('toggle-video-button', false);
  },

  handleDeviceSelected: async (e: Event) => {
    const deviceId = (e.target as HTMLSelectElement).value;
    const elementId = (e.target as HTMLSelectElement).id;

    if (!currentRoom) return;

    let kind: MediaDeviceKind;
    if (elementId === 'video-input') {
      kind = 'videoinput';
    } else if (elementId === 'audio-input') {
      kind = 'audioinput';
    } else if (elementId === 'audio-output') {
      kind = 'audiooutput';
    } else {
      return;
    }

    await currentRoom.switchActiveDevice(kind, deviceId);
    appendLog(`Switched ${kind} to device: ${deviceId}`);
  },

  sendMessage: () => {
    if (!currentRoom) return;
    const textField = $('entry') as HTMLInputElement;
    if (textField.value.trim()) {
      const message = textField.value.trim();
      currentRoom.localParticipant.sendText(message, { topic: 'lk.chat' });
      addChatMessage('You', message);
      textField.value = '';
      appendLog(`Sent message: ${message}`);
    }
  },

  disconnect: () => {
    if (currentRoom) {
      appendLog('Disconnecting from call...');
      currentRoom.disconnect();
      currentRoom = undefined;
      currentCallId = undefined;
      setButtonsForState(false);
      showStatus('info', 'Call ended');
      clearParticipants();
    }
  },
};

async function connectToLiveKit(url: string, token: string): Promise<void> {
  const roomOptions: RoomOptions = {
    adaptiveStream: true,
    dynacast: true,
    publishDefaults: {
      simulcast: true,
      videoSimulcastLayers: [VideoPresets.h180, VideoPresets.h360],
      videoCodec: 'vp8',
    },
    videoCaptureDefaults: {
      resolution: VideoPresets.h720.resolution,
    },
  };

  const room = new Room(roomOptions);

  room
    .on(RoomEvent.ParticipantConnected, participantConnected)
    .on(RoomEvent.ParticipantDisconnected, participantDisconnected)
    .on(RoomEvent.ChatMessage, handleChatMessage)
    .on(RoomEvent.Disconnected, handleRoomDisconnect)
    .on(RoomEvent.Reconnecting, () => appendLog('Reconnecting...'))
    .on(RoomEvent.Reconnected, () => appendLog('Reconnected successfully'))
    .on(RoomEvent.LocalTrackPublished, () => {
      renderParticipant(room.localParticipant);
    })
    .on(RoomEvent.LocalTrackUnpublished, () => {
      renderParticipant(room.localParticipant);
    })
    .on(RoomEvent.TrackSubscribed, (track, pub, participant) => {
      appendLog(`Subscribed to track from ${participant.identity}`);
      renderParticipant(participant);
    })
    .on(RoomEvent.TrackUnsubscribed, (_, pub, participant) => {
      renderParticipant(participant);
    })
    .on(RoomEvent.AudioPlaybackStatusChanged, () => {
      if (room.canPlaybackAudio) {
        appendLog('Audio playback enabled');
      } else {
        appendLog('Audio playback blocked - user interaction required');
      }
    });

  try {
    const publishPromise = new Promise<void>(async (resolve, reject) => {
      try {
        await room.localParticipant.enableCameraAndMicrophone();
        appendLog('Camera and microphone enabled');
        resolve();
      } catch (error) {
        reject(error);
      }
    });

    await Promise.all([room.connect(url, token), publishPromise]);

    currentRoom = room;
    (window as any).currentRoom = room;

    appendLog(`Connected to room: ${room.name}`);

    room.remoteParticipants.forEach((participant) => {
      participantConnected(participant);
    });
    participantConnected(room.localParticipant);
    updateButtonsForPublishState();

    await room.startAudio();
    appendLog('Started audio playback');
  } catch (error: any) {
    appendLog(`Failed to connect: ${error.message}`);
    throw error;
  }
}
function participantConnected(participant: Participant) {
  appendLog(`Participant connected: ${participant.identity}`);
  participant
    .on(ParticipantEvent.TrackMuted, (pub: TrackPublication) => {
      appendLog(`Track muted: ${participant.identity}`);
      renderParticipant(participant);
    })
    .on(ParticipantEvent.TrackUnmuted, (pub: TrackPublication) => {
      appendLog(`Track unmuted: ${participant.identity}`);
      renderParticipant(participant);
    })
    .on(ParticipantEvent.IsSpeakingChanged, () => {
      renderParticipant(participant);
    });

  renderParticipant(participant);
}

function participantDisconnected(participant: RemoteParticipant) {
  appendLog(`Participant disconnected: ${participant.identity}`);
  renderParticipant(participant, true);
}

function handleRoomDisconnect(reason?: DisconnectReason) {
  appendLog(`Disconnected from room. Reason: ${reason}`);
  setButtonsForState(false);
  clearParticipants();
  currentRoom = undefined;
  currentCallId = undefined;
}

function handleChatMessage(msg: ChatMessage, participant?: Participant) {
  const from = participant?.identity || 'Unknown';
  addChatMessage(from, msg.message);
  appendLog(`Chat message from ${from}: ${msg.message}`);
}

// UI Helper Functions
function showStatus(type: 'success' | 'error' | 'info', message: string) {
  const statusEl = $('status-message');
  statusEl.style.display = 'block';
  statusEl.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'}`;
  statusEl.textContent = message;

  if (type === 'success' || type === 'info') {
    setTimeout(() => {
      statusEl.style.display = 'none';
    }, 5000);
  }
}

function appendLog(message: string) {
  console.log(`[Bey API] ${message}`);
}

function addChatMessage(from: string, message: string) {
  state.chatMessages.push({ from, message, timestamp: Date.now() });
  const chatEl = $('chat') as HTMLTextAreaElement;
  chatEl.value = state.chatMessages
    .map((msg) => `${msg.from}: ${msg.message}`)
    .join('\n');
  chatEl.scrollTop = chatEl.scrollHeight;
}

function setButtonDisabled(buttonId: string, disabled: boolean) {
  const el = $(buttonId) as HTMLButtonElement;
  if (el) el.disabled = disabled;
}

function updateButtonText(buttonId: string, text: string) {
  const el = $(buttonId) as HTMLButtonElement;
  if (el) el.textContent = text;
}

function setButtonsForState(connected: boolean) {
  const connectedButtons = ['toggle-audio-button', 'toggle-video-button', 'disconnect-button', 'send-button', 'entry'];
  const disconnectedButtons = ['start-call-button'];
  const deviceSelects = ['video-input', 'audio-input', 'audio-output'];

  if (connected) {
    connectedButtons.forEach((id) => {
      const el = $(id);
      if (el) el.removeAttribute('disabled');
    });
    disconnectedButtons.forEach((id) => {
      const el = $(id);
      if (el) el.setAttribute('disabled', 'true');
    });
    deviceSelects.forEach((id) => {
      const el = $(id);
      if (el) el.removeAttribute('disabled');
    });
    handleDevicesChanged();
  } else {
    connectedButtons.forEach((id) => {
      const el = $(id);
      if (el) el.setAttribute('disabled', 'true');
    });
    disconnectedButtons.forEach((id) => {
      const el = $(id);
      if (el) el.removeAttribute('disabled');
    });
    deviceSelects.forEach((id) => {
      const el = $(id);
      if (el) el.setAttribute('disabled', 'true');
    });
  }
}

function updateButtonsForPublishState() {
  if (!currentRoom) return;

  const lp = currentRoom.localParticipant;

  updateButtonText(
    'toggle-video-button',
    lp.isCameraEnabled ? 'Disable Camera' : 'Enable Camera'
  );

  updateButtonText(
    'toggle-audio-button',
    lp.isMicrophoneEnabled ? 'Disable Mic' : 'Enable Mic'
  );
}

async function handleDevicesChanged() {
  const kinds: MediaDeviceKind[] = ['videoinput', 'audioinput', 'audiooutput'];
  const ids = ['video-input', 'audio-input', 'audio-output'];

  for (let i = 0; i < kinds.length; i++) {
    const kind = kinds[i];
    const elementId = ids[i];
    const devices = await Room.getLocalDevices(kind);
    const element = $(elementId) as HTMLSelectElement;
    if (element) {
      populateSelect(element, devices);
    }
  }
}

function populateSelect(element: HTMLSelectElement, devices: MediaDeviceInfo[]) {
  element.innerHTML = '';

  for (const device of devices) {
    const option = document.createElement('option');
    option.text = device.label || `${device.kind} (${device.deviceId.slice(0, 8)})`;
    option.value = device.deviceId;
    element.appendChild(option);
  }
}

function renderParticipant(participant: Participant, remove: boolean = false) {
  const container = $('participants-area');
  if (!container) return;

  const isAgent = participant.identity === 'avatar_worker';
  const isLocal = isLocalParticipant(participant);

  if (!isAgent && !isLocal) {
    return;
  }

  const { identity } = participant;
  let div = container.querySelector(`#participant-${identity}`) as HTMLDivElement;

  if (remove) {
    if (div) div.remove();
    return;
  }

  if (!div) {
    div = document.createElement('div');
    div.id = `participant-${identity}`;
    div.className = 'participant';
    div.innerHTML = `
      <video id="video-${identity}" autoplay playsinline></video>
      <audio id="audio-${identity}" autoplay></audio>
      <div class="info-bar">
        <div id="name-${identity}" class="name"></div>
        <div class="right">
          <span id="mic-${identity}"></span>
        </div>
      </div>
    `;
    container.appendChild(div);
  }

  const videoElm = container.querySelector(`#video-${identity}`) as HTMLVideoElement;
  const audioElm = container.querySelector(`#audio-${identity}`) as HTMLAudioElement;
  const nameElm = container.querySelector(`#name-${identity}`);
  const micElm = container.querySelector(`#mic-${identity}`);

  if (nameElm) {
    nameElm.innerHTML = isLocal ? 'You' : 'Agent';
  }

  const cameraPub = participant.getTrackPublication(Track.Source.Camera);
  const cameraEnabled = cameraPub && cameraPub.isSubscribed && !cameraPub.isMuted;

  if (cameraEnabled) {
    if (isLocal) {
      videoElm.style.transform = 'scale(-1, 1)';
    }
    cameraPub?.videoTrack?.attach(videoElm);
  } else {
    if (cameraPub?.videoTrack) {
      cameraPub.videoTrack.detach(videoElm);
    }
    videoElm.src = '';
    videoElm.srcObject = null;
  }

  const micPub = participant.getTrackPublication(Track.Source.Microphone);
  const micEnabled = micPub && micPub.isSubscribed && !micPub.isMuted;

  if (micEnabled && !isLocal) {
    micPub?.audioTrack?.attach(audioElm);
  }

  if (micElm) {
    micElm.innerHTML = micEnabled ? '🎤' : '🔇';
  }

  if (participant.isSpeaking) {
    div.classList.add('speaking');
  } else {
    div.classList.remove('speaking');
  }
}

function clearParticipants() {
  const container = $('participants-area');
  if (container) {
    container.innerHTML = '';
  }
  state.chatMessages = [];
  const chatEl = $('chat') as HTMLTextAreaElement;
  if (chatEl) chatEl.value = '';
}

(window as any).appActions = appActions;
