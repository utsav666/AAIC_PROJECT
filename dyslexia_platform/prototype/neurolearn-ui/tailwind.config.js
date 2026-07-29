/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Lexend', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        brand: {
          teal: '#0d9488',
          purple: '#7c3aed',
          amber: '#d97706',
          pink: '#db2777',
        },
      },
    },
  },
  plugins: [],
}
