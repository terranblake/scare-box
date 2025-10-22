import { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import { useApi } from '../hooks/useApi';
import type { AudioData, LightStatus, Event as EventType, SystemState, DeviceStatus } from '../types';
import AudioMeter from './AudioMeter';
import LightControl from './LightControl';
import EventLog from './EventLog';
import TriggerButton from './TriggerButton';
import ConfigPanel from './ConfigPanel';

export default function Dashboard() {
  const WS_URL = `ws://${window.location.hostname}:${window.location.port || 8000}/ws`;

  const { isConnected, lastMessage } = useWebSocket(WS_URL);
  const { data: state, refetch: refetchState } = useApi<SystemState>('/api/state', 1000);
  const { data: devices } = useApi<DeviceStatus>('/api/devices', 2000);

  const [audioData, setAudioData] = useState<AudioData | null>(null);
  const [lightStatus, setLightStatus] = useState<LightStatus>({ connected: false, devices: [] });
  const [events, setEvents] = useState<EventType[]>([]);
  const [showConfig, setShowConfig] = useState(false);

  useEffect(() => {
    if (!lastMessage) return;

    switch (lastMessage.type) {
      case 'audio_level':
        setAudioData(lastMessage.data as AudioData);
        break;
      case 'light_status':
        setLightStatus(lastMessage.data as LightStatus);
        break;
      case 'event':
      case 'notification':
        setEvents(prev => [...prev, lastMessage.data as EventType].slice(-50));
        break;
      case 'state_change':
        refetchState();
        break;
    }
  }, [lastMessage]);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-4 md:p-8">
      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-4xl font-bold text-halloween-orange">
              SCARE BOX
            </h1>
            <div className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                state?.mode === 'adult'
                  ? 'bg-red-900 text-red-100'
                  : 'bg-blue-900 text-blue-100'
              }`}>
                {state?.mode?.toUpperCase() || 'UNKNOWN'}
              </span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                state?.is_running
                  ? 'bg-green-900 text-green-100'
                  : 'bg-gray-700 text-gray-300'
              }`}>
                {state?.is_running ? '● RUNNING' : '○ STOPPED'}
              </span>
              <span className={`px-3 py-1 rounded-full text-sm ${
                isConnected
                  ? 'bg-green-900 text-green-100'
                  : 'bg-red-900 text-red-100'
              }`}>
                {isConnected ? '● CONNECTED' : '○ DISCONNECTED'}
              </span>
            </div>
          </div>
          <button
            onClick={() => setShowConfig(!showConfig)}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition"
          >
            ⚙ Settings
          </button>
        </div>
      </header>

      {/* Config Panel */}
      {showConfig && (
        <div className="mb-8">
          <ConfigPanel onClose={() => setShowConfig(false)} />
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Audio Level */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <AudioMeter audioData={audioData} />
        </div>

        {/* Light Level */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <LightControl lightStatus={lightStatus} />
        </div>

        {/* Trigger Button */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <TriggerButton
            canTrigger={state?.state === 'non_trick'}
            currentState={state?.state || 'unknown'}
          />
        </div>
      </div>

      {/* Device Status */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 mb-6">
        <h2 className="text-xl font-semibold mb-4">Connected Devices</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center gap-3">
            <span className={`text-2xl ${devices?.microphone?.connected ? 'text-green-500' : 'text-red-500'}`}>
              {devices?.microphone?.connected ? '✓' : '✗'}
            </span>
            <div>
              <div className="font-medium">Microphone</div>
              <div className="text-sm text-gray-400">USB-C Audio Input</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className={`text-2xl ${devices?.lights?.connected ? 'text-green-500' : 'text-red-500'}`}>
              {devices?.lights?.connected ? '✓' : '✗'}
            </span>
            <div>
              <div className="font-medium">LIFX Lights</div>
              <div className="text-sm text-gray-400">
                {devices?.lights?.device_count || 0} device(s)
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className={`text-2xl ${devices?.speaker?.connected ? 'text-green-500' : 'text-red-500'}`}>
              {devices?.speaker?.connected ? '✓' : '✗'}
            </span>
            <div>
              <div className="font-medium">Speaker</div>
              <div className="text-sm text-gray-400">Bluetooth Audio Output</div>
            </div>
          </div>
        </div>
      </div>

      {/* Event Log */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <EventLog events={events} />
      </div>
    </div>
  );
}
