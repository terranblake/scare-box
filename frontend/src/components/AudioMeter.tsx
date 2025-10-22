import type { AudioData } from '../types';

interface AudioMeterProps {
  audioData: AudioData | null;
}

export default function AudioMeter({ audioData }: AudioMeterProps) {
  const rmsPercent = audioData ? Math.min(100, audioData.rms * 100) : 0;
  const peakPercent = audioData ? Math.min(100, audioData.peak * 100) : 0;

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Audio Level</h2>

      {/* Visual Meter */}
      <div className="mb-6">
        <div className="flex items-center justify-center h-32 mb-2">
          <div className="flex items-end gap-1 h-full">
            {Array.from({ length: 20 }).map((_, i) => {
              const barPercent = ((i + 1) / 20) * 100;
              const isActive = peakPercent >= barPercent;

              return (
                <div
                  key={i}
                  className={`w-3 transition-all duration-100 ${
                    isActive
                      ? barPercent > 80
                        ? 'bg-red-500'
                        : barPercent > 50
                        ? 'bg-halloween-orange'
                        : 'bg-green-500'
                      : 'bg-gray-700'
                  }`}
                  style={{ height: `${((i + 1) / 20) * 100}%` }}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* Numeric Values */}
      <div className="space-y-3">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-400">RMS</span>
            <span className="font-mono">{(audioData?.rms || 0).toFixed(3)}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-halloween-orange h-2 rounded-full transition-all duration-100"
              style={{ width: `${rmsPercent}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-400">Peak</span>
            <span className="font-mono">{(audioData?.peak || 0).toFixed(3)}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-red-500 h-2 rounded-full transition-all duration-100"
              style={{ width: `${peakPercent}%` }}
            />
          </div>
        </div>

        <div className="pt-2 border-t border-gray-700">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Frequency Peak</span>
            <span className="font-mono">{(audioData?.frequency_peak || 0).toFixed(1)} Hz</span>
          </div>
        </div>
      </div>
    </div>
  );
}
