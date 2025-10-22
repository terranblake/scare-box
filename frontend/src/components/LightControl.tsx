import type { LightStatus } from '../types';

interface LightControlProps {
  lightStatus: LightStatus;
}

export default function LightControl({ lightStatus }: LightControlProps) {
  const avgBrightness = lightStatus.devices.length > 0
    ? lightStatus.devices.reduce((sum, d) => sum + d.brightness, 0) / lightStatus.devices.length
    : 0;

  const brightnessPercent = Math.round(avgBrightness * 100);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Light Level</h2>

      {/* Visual Indicator */}
      <div className="mb-6">
        <div className="flex items-center justify-center h-32">
          <div className="relative w-32 h-32">
            <svg className="transform -rotate-90 w-32 h-32">
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-gray-700"
              />
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 56}`}
                strokeDashoffset={`${2 * Math.PI * 56 * (1 - avgBrightness)}`}
                className="text-halloween-orange transition-all duration-300"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-3xl font-bold">{brightnessPercent}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Device List */}
      <div className="space-y-2">
        {lightStatus.devices.length > 0 ? (
          lightStatus.devices.map((device) => (
            <div key={device.id} className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${device.power ? 'bg-green-500' : 'bg-gray-600'}`} />
                <span className="text-gray-400">{device.name}</span>
              </div>
              <span className="font-mono">{Math.round(device.brightness * 100)}%</span>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-500 py-4">
            {lightStatus.connected ? 'No devices found' : 'Not connected'}
          </div>
        )}
      </div>

      {lightStatus.connected && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Total Devices</span>
            <span className="font-medium">{lightStatus.device_count || lightStatus.devices.length}</span>
          </div>
        </div>
      )}
    </div>
  );
}
