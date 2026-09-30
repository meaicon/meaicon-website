/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './_site/**/*.html',
    './_includes/**/*.njk',
    './_includes/**/*.html',
    './*.html',
    './*.njk',
  ],
  theme: {
    extend: {
      colors: {
        // Custom palette from site-head.njk
        'accent': '#0A66C2',
        'accent-strong': '#004182',
        'accent-light': 'rgba(10, 102, 194, 0.15)',
        'warning': '#F59E0B',
        'danger': '#DC2626',
      },
      fontFamily: {
        'sans': ['Inter', 'Inter-Semantic', 'system-ui'],
      },
    },
  },
  plugins: [],
};
