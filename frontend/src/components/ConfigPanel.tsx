import { useState, useEffect } from 'react';
import { useApi, apiPut, apiPost } from '../hooks/useApi';
import type { Config } from '../types';

interface ConfigPanelProps {
  onClose: () => void;
}

export default function ConfigPanel({ onClose }: ConfigPanelProps) {
  const { data: config, refetch } = useApi<Config>('/api/config');
  const [mode, setMode] = useState('child');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Audio settings
  const [triggerFreqMin, setTriggerFreqMin] = useState(800);
  const [triggerFreqMax, setTriggerFreqMax] = useState(1200);
  const [triggerThreshold, setTriggerThreshold] = useState(0.3);

  // Timing settings
  const [countdownDuration, setCountdownDuration] = useState(3.0);
  const [activeDuration, setActiveDuration] = useState(2.0);
  const [resetDuration, setResetDuration] = useState(5.0);
  const [screamDelay, setScreamDelay] = useState(2.0);

  // Device selection
  const { data: availableDevices } = useApi<{
    microphones: Array<{ id: number; name: string; channels: number; sample_rate: number }>;
    speakers: Array<{ id: number; name: string; channels: number; sample_rate: number }>;
  }>('/api/devices/available');
  const { data: currentDevices } = useApi<any>('/api/devices');
  const [selectedMicrophone, setSelectedMicrophone] = useState<string>('');
  const [selectedSpeaker, setSelectedSpeaker] = useState<string>('');

  useEffect(() => {
    if (config) {
      setMode(config.mode);
      setTriggerFreqMin(config.audio.trigger_frequency_min);
      setTriggerFreqMax(config.audio.trigger_frequency_max);
      setTriggerThreshold(config.audio.trigger_amplitude_threshold);
      setCountdownDuration(config.timing.countdown_duration);
      setActiveDuration(config.timing.active_duration);
      setResetDuration(config.timing.reset_duration);
      setScreamDelay(config.timing.scream_delay);
    }
  }, [config]);

  const handleModeChange = async (newMode: string) => {
    setMode(newMode);
    setSaving(true);
    setMessage(null);

    try {
      await apiPut('/api/mode', { mode: newMode });
      await refetch();
      setMessage({ type: 'success', text: `Mode changed to ${newMode.toUpperCase()}` });
    } catch (err) {
      setMessage({ type: 'error', text: err instanceof Error ? err.message : 'Failed to change mode' });
    } finally {
      setSaving(false);
    }
  };

  const handleStartStop = async (action: 'start' | 'stop') => {
    setSaving(true);
    setMessage(null);

    try {
      await apiPost(`/api/${action}`);
      setMessage({ type: 'success', text: `System ${action === 'start' ? 'started' : 'stopped'}` });
    } catch (err) {
      setMessage({ type: 'error', text: err instanceof Error ? err.message : `Failed to ${action}` });
    } finally {
      setSaving(false);
    }
  };

  const handleSaveConfig = async () => {
    setSaving(true);
    setMessage(null);

    try {
      await apiPut('/api/config', {
        trigger_frequency_min: triggerFreqMin,
        trigger_frequency_max: triggerFreqMax,
        trigger_amplitude_threshold: triggerThreshold,
        countdown_duration: countdownDuration,
        active_duration: activeDuration,
        reset_duration: resetDuration,
        scream_delay: screamDelay,
      });
      await refetch();
      setMessage({ type: 'success', text: 'Configuration saved successfully' });
    } catch (err) {
      setMessage({ type: 'error', text: err instanceof Error ? err.message : 'Failed to save configuration' });
    } finally {
      setSaving(false);
    }
  };

  const handleMicrophoneChange = async (deviceName: string) => {
    setSaving(true);
    setMessage(null);

    try {
      await apiPut('/api/devices/microphone', { device_name: deviceName });
      setSelectedMicrophone(deviceName);
      setMessage({ type: 'success', text: `Microphone changed to ${deviceName}` });
    } catch (err) {
      setMessage({ type: 'error', text: err instanceof Error ? err.message : 'Failed to change microphone' });
    } finally {
      setSaving(false);
    }
  };

  const handleSpeakerChange = async (deviceName: string) => {
    setSaving(true);
    setMessage(null);

    try {
      await apiPut('/api/devices/speaker', { device_name: deviceName });
      setSelectedSpeaker(deviceName);
      setMessage({ type: 'success', text: `Speaker changed to ${deviceName}` });
    } catch (err) {
      setMessage({ type: 'error', text: err instanceof Error ? err.message : 'Failed to change speaker' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Settings</h2>
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition"
        >
          Close
        </button>
      </div>

      {message && (
        <div
          className={`mb-6 px-4 py-3 rounded-lg ${
            message.type === 'success'
              ? 'bg-green-900/50 text-green-200'
              : 'bg-red-900/50 text-red-200'
          }`}
        >
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Mode Selection */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Operating Mode</h3>
          <div className="space-y-3">
            <label className="flex items-center gap-3 p-4 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-750 transition">
              <input
                type="radio"
                name="mode"
                value="child"
                checked={mode === 'child'}
                onChange={(e) => handleModeChange(e.target.value)}
                disabled={saving}
                className="w-4 h-4"
              />
              <div>
                <div className="font-medium">Child Mode</div>
                <div className="text-sm text-gray-400">
                  Softer effects, lower volume and brightness
                </div>
              </div>
            </label>

            <label className="flex items-center gap-3 p-4 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-750 transition">
              <input
                type="radio"
                name="mode"
                value="adult"
                checked={mode === 'adult'}
                onChange={(e) => handleModeChange(e.target.value)}
                disabled={saving}
                className="w-4 h-4"
              />
              <div>
                <div className="font-medium">Adult Mode</div>
                <div className="text-sm text-gray-400">
                  Full intensity effects for maximum scare
                </div>
              </div>
            </label>
          </div>
        </div>

        {/* System Control */}
        <div>
          <h3 className="text-lg font-semibold mb-4">System Control</h3>
          <div className="space-y-3">
            <button
              onClick={() => handleStartStop('start')}
              disabled={saving}
              className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:text-gray-500 rounded-lg font-medium transition"
            >
              Start System
            </button>
            <button
              onClick={() => handleStartStop('stop')}
              disabled={saving}
              className="w-full px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:text-gray-500 rounded-lg font-medium transition"
            >
              Stop System
            </button>
          </div>
        </div>

        {/* Audio Settings */}
        <div className="md:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Audio Trigger Settings</h3>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Trigger Frequency Min (Hz)
                </label>
                <input
                  type="number"
                  value={triggerFreqMin}
                  onChange={(e) => setTriggerFreqMin(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="2000"
                  step="50"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Trigger Frequency Max (Hz)
                </label>
                <input
                  type="number"
                  value={triggerFreqMax}
                  onChange={(e) => setTriggerFreqMax(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="2000"
                  step="50"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Trigger Threshold (0.0-1.0)
                </label>
                <input
                  type="number"
                  value={triggerThreshold}
                  onChange={(e) => setTriggerThreshold(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="1"
                  step="0.05"
                />
              </div>
            </div>
            {config && (
              <div className="mt-3 text-xs text-gray-500">
                Sample Rate: {config.audio.sample_rate} Hz (read-only)
              </div>
            )}
          </div>
        </div>

        {/* Timing Settings */}
        <div className="md:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Timing Settings</h3>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Countdown Duration (seconds)
                </label>
                <input
                  type="number"
                  value={countdownDuration}
                  onChange={(e) => setCountdownDuration(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="30"
                  step="0.5"
                />
                <div className="text-xs text-gray-500 mt-1">Time before scare triggers</div>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Active Duration (seconds)
                </label>
                <input
                  type="number"
                  value={activeDuration}
                  onChange={(e) => setActiveDuration(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="30"
                  step="0.5"
                />
                <div className="text-xs text-gray-500 mt-1">Duration of scare effects</div>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Reset Duration (seconds)
                </label>
                <input
                  type="number"
                  value={resetDuration}
                  onChange={(e) => setResetDuration(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="60"
                  step="1"
                />
                <div className="text-xs text-gray-500 mt-1">Time to return to normal</div>
              </div>

              {/* Scream Delay */}
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Scream Delay (seconds)
                </label>
                <input
                  type="number"
                  value={screamDelay}
                  onChange={(e) => setScreamDelay(Number(e.target.value))}
                  disabled={saving}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                  min="0"
                  max="10"
                  step="0.1"
                />
                <div className="text-xs text-gray-500 mt-1">Delay between BOO and Happy Halloween</div>
              </div>
            </div>
          </div>
        </div>

        {/* Device Selection */}
        {availableDevices && (availableDevices.microphones.length > 0 || availableDevices.speakers.length > 0) && (
          <div className="md:col-span-2">
            <h3 className="text-lg font-semibold mb-4">Device Selection</h3>
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Microphone */}
                {availableDevices.microphones.length > 0 && (
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">
                      Microphone Device
                    </label>
                    <select
                      value={selectedMicrophone || (currentDevices?.microphone ? availableDevices.microphones.find(d => d.id === currentDevices.microphone.device_id)?.name : '')}
                      onChange={(e) => handleMicrophoneChange(e.target.value)}
                      disabled={saving}
                      className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                    >
                      {availableDevices.microphones.map((mic) => (
                        <option key={mic.id} value={mic.name}>
                          {mic.name} ({mic.sample_rate} Hz, {mic.channels} ch)
                        </option>
                      ))}
                    </select>
                    {currentDevices?.microphone && (
                      <div className="text-xs text-gray-500 mt-1">
                        Currently using: Device ID {currentDevices.microphone.device_id}
                      </div>
                    )}
                  </div>
                )}

                {/* Speaker */}
                {availableDevices.speakers.length > 0 && (
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">
                      Speaker/Output Device
                    </label>
                    <select
                      value={selectedSpeaker || (currentDevices?.speaker ? availableDevices.speakers.find(d => d.id === currentDevices.speaker.device_id)?.name : '')}
                      onChange={(e) => handleSpeakerChange(e.target.value)}
                      disabled={saving}
                      className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg focus:border-orange-500 focus:outline-none disabled:opacity-50"
                    >
                      {availableDevices.speakers.map((speaker) => (
                        <option key={speaker.id} value={speaker.name}>
                          {speaker.name} ({speaker.sample_rate} Hz, {speaker.channels} ch)
                        </option>
                      ))}
                    </select>
                    {currentDevices?.speaker && (
                      <div className="text-xs text-gray-500 mt-1">
                        Currently using: Device ID {currentDevices.speaker.device_id}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Save Button */}
        <div className="md:col-span-2">
          <button
            onClick={handleSaveConfig}
            disabled={saving}
            className="w-full px-6 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-700 disabled:text-gray-500 rounded-lg font-medium transition"
          >
            {saving ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </div>
    </div>
  );
}
