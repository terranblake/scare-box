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

  useEffect(() => {
    if (config) {
      setMode(config.mode);
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

        {/* Current Configuration */}
        {config && (
          <div className="md:col-span-2">
            <h3 className="text-lg font-semibold mb-4">Current Configuration</h3>
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <div className="text-gray-400 mb-1">Trigger Frequency Range</div>
                  <div className="font-mono">
                    {config.audio.trigger_frequency_min} - {config.audio.trigger_frequency_max} Hz
                  </div>
                </div>
                <div>
                  <div className="text-gray-400 mb-1">Trigger Threshold</div>
                  <div className="font-mono">{config.audio.trigger_amplitude_threshold}</div>
                </div>
                <div>
                  <div className="text-gray-400 mb-1">Sample Rate</div>
                  <div className="font-mono">{config.audio.sample_rate} Hz</div>
                </div>
                <div>
                  <div className="text-gray-400 mb-1">Countdown Duration</div>
                  <div className="font-mono">{config.timing.countdown_duration}s</div>
                </div>
                <div>
                  <div className="text-gray-400 mb-1">Active Duration</div>
                  <div className="font-mono">{config.timing.active_duration}s</div>
                </div>
                <div>
                  <div className="text-gray-400 mb-1">Reset Duration</div>
                  <div className="font-mono">{config.timing.reset_duration}s</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
