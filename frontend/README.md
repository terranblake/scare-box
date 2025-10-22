# Scare Box Frontend

React + TypeScript + Tailwind CSS frontend for the Scare Box control interface.

## Setup

### Install Dependencies

```bash
cd frontend
npm install
```

## Development

### Start Development Server

```bash
npm run dev
```

Visit http://localhost:3000

The frontend will proxy API requests to the backend at http://localhost:8000.

## Building

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Features

- **Real-time Dashboard**: Live audio levels, light status, and event logs
- **WebSocket Integration**: Real-time updates for all system changes
- **Manual Trigger**: Large button to manually trigger scare sequence
- **Mode Switching**: Toggle between child and adult modes
- **Device Status**: Monitor connection status of all hardware
- **Event Timeline**: View all system events and notifications
- **Settings Panel**: Configure system parameters
- **Responsive Design**: Works on desktop, tablet, and mobile

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx      # Main dashboard
│   │   ├── AudioMeter.tsx     # Audio level display
│   │   ├── LightControl.tsx   # Light status display
│   │   ├── EventLog.tsx       # Event timeline
│   │   ├── TriggerButton.tsx  # Manual trigger button
│   │   └── ConfigPanel.tsx    # Settings panel
│   ├── hooks/
│   │   ├── useWebSocket.ts    # WebSocket hook
│   │   └── useApi.ts          # REST API hook
│   ├── types/
│   │   └── index.ts           # TypeScript definitions
│   ├── App.tsx                # Main app component
│   ├── main.tsx               # Entry point
│   └── index.css              # Global styles
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Native WebSocket** - Real-time communication

## Customization

### Colors

Edit `tailwind.config.js` to customize the Halloween color scheme:

```javascript
theme: {
  extend: {
    colors: {
      halloween: {
        orange: '#FF6B1A',
        purple: '#8B5CF6',
        green: '#10B981',
      },
    },
  },
}
```

### API Endpoint

The frontend expects the backend at `http://localhost:8000` by default. To change this, edit `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url:8000',
      changeOrigin: true,
    },
  },
}
```

## Deployment

### Static Hosting

The built frontend can be deployed to any static hosting service (Netlify, Vercel, GitHub Pages, etc.).

### Serving from Backend

Copy the `dist/` folder contents to your backend's static files directory.

### Local Network Access

To access from other devices on the same network:

```bash
npm run dev -- --host 0.0.0.0
```

Then visit `http://[your-ip]:3000` from any device.
