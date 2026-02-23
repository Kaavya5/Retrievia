export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pastel: {
          purple: '#d8b4fe',
          pink: '#fbcfe8',
          blue: '#bfdbfe',
          background: '#faf5ff',
          deep: '#8b5cf6',
          dark: '#581c87',
          gray: '#64748b',
          white: '#ffffff'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 10px 40px -10px rgba(139, 92, 246, 0.1)',
        'bubble': '0 4px 15px rgba(0,0,0,0.05)'
      }
    },
  },
  plugins: [],
}
