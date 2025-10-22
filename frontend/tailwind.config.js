/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        halloween: {
          orange: '#FF6B1A',
          purple: '#8B5CF6',
          green: '#10B981',
          dark: '#1a1a1a',
        },
      },
    },
  },
  plugins: [],
}
