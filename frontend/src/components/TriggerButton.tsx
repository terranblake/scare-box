import { useState } from 'react';
import { apiPost } from '../hooks/useApi';

interface TriggerButtonProps {
  canTrigger: boolean;
  currentState: string;
}

export default function TriggerButton({ canTrigger, currentState }: TriggerButtonProps) {
  const [triggering, setTriggering] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTrigger = async () => {
    if (!canTrigger || triggering) return;

    setTriggering(true);
    setError(null);

    try {
      await apiPost('/api/trigger');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to trigger');
    } finally {
      setTriggering(false);
    }
  };

  const getStateDisplay = (state: string) => {
    switch (state) {
      case 'non_trick':
        return 'Ready';
      case 'trick_countdown':
        return 'Counting Down...';
      case 'trick_active':
        return 'SCARING!';
      case 'trick_reset':
        return 'Resetting...';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h2 className="text-xl font-semibold mb-4">Manual Trigger</h2>

      <button
        onClick={handleTrigger}
        disabled={!canTrigger || triggering}
        className={`
          w-48 h-48 rounded-full text-2xl font-bold
          transition-all duration-200 transform
          ${
            canTrigger && !triggering
              ? 'bg-halloween-orange hover:bg-orange-600 hover:scale-105 active:scale-95 shadow-lg shadow-halloween-orange/50'
              : 'bg-gray-700 text-gray-500 cursor-not-allowed'
          }
        `}
      >
        {triggering ? (
          <span className="animate-pulse">TRIGGERING...</span>
        ) : (
          'TRIGGER'
        )}
      </button>

      <div className="mt-6 text-center">
        <div className="text-sm text-gray-400 mb-1">Current State</div>
        <div className={`text-lg font-medium ${
          currentState === 'trick_active' ? 'text-red-400 animate-pulse' : 'text-gray-200'
        }`}>
          {getStateDisplay(currentState)}
        </div>
      </div>

      {error && (
        <div className="mt-4 px-4 py-2 bg-red-900/50 text-red-200 rounded-lg text-sm">
          {error}
        </div>
      )}

      {!canTrigger && !error && (
        <div className="mt-4 px-4 py-2 bg-gray-800 text-gray-400 rounded-lg text-sm">
          Trigger disabled during sequence
        </div>
      )}
    </div>
  );
}
