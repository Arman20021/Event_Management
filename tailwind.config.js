/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",   //template at the project level
    "./**/templates/**/*.html"  //tempaltes inside apps
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

