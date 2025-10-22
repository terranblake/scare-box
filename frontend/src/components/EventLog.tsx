import type { Event as EventType } from '../types';

interface EventLogProps {
  events: EventType[];
}

export default function EventLog({ events }: EventLogProps) {
  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'error':
        return 'text-red-400';
      case 'warning':
        return 'text-yellow-400';
      case 'info':
        return 'text-blue-400';
      default:
        return 'text-gray-400';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'system':
        return '⚙';
      case 'trigger':
        return '⚡';
      case 'state':
        return '🔄';
      case 'hardware':
        return '🔌';
      case 'config':
        return '📝';
      default:
        return '•';
    }
  };

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString();
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Event Log</h2>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {events.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            No events yet
          </div>
        ) : (
          events
            .slice()
            .reverse()
            .map((event, index) => (
              <div
                key={`${event.timestamp}-${index}`}
                className="flex items-start gap-3 p-3 bg-gray-800 rounded-lg hover:bg-gray-750 transition"
              >
                <span className="text-xl mt-0.5">
                  {getCategoryIcon(event.category)}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-gray-500 font-mono">
                      {formatTime(event.timestamp)}
                    </span>
                    <span
                      className={`text-xs font-medium uppercase ${getLevelColor(event.level)}`}
                    >
                      {event.level}
                    </span>
                    <span className="text-xs text-gray-500 uppercase">
                      {event.category}
                    </span>
                  </div>
                  <p className="text-sm">{event.message}</p>
                  {event.details && Object.keys(event.details).length > 0 && (
                    <pre className="text-xs text-gray-400 mt-1 overflow-x-auto">
                      {JSON.stringify(event.details, null, 2)}
                    </pre>
                  )}
                </div>
              </div>
            ))
        )}
      </div>
    </div>
  );
}
