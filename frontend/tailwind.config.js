/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          blue: '#00d4ff',
          green: '#00ff88',
          purple: '#b800ff',
          dark: '#0a0e27',
          darker: '#050714',
          card: '#131829'
        }
      },
      fontFamily: {
        mono: ['Courier New', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      backgroundImage: {
        'cyber-grid': "linear-gradient(rgba(0, 212, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 212, 255, 0.1) 1px, transparent 1px)",
        'cyber-gradient': "linear-gradient(135deg, #0a0e27 0%, #131829 50%, #1a1f3a 100%)"
      },
      backgroundSize: {
        'grid': '50px 50px'
      },
      boxShadow: {
        'cyber': '0 0 20px rgba(0, 212, 255, 0.5)',
        'cyber-green': '0 0 20px rgba(0, 255, 136, 0.5)',
        'cyber-red': '0 0 20px rgba(255, 0, 68, 0.5)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(0, 212, 255, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 212, 255, 1)' },
        }
      }
    },
  },
  plugins: [],
}
