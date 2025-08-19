/** @type {import('tailwindcss').Config} */
module.exports = {
  corePlugins: {
    // https://github.com/tailwindlabs/tailwindcss/discussions/9993#discussioncomment-4298069
    preflight: false,
  },
  content: [
    "./src/app/*.{html,ts,css}",
    "./src/app/**/*.{html,ts,css}",
    "./src/app/**/**/*.{html,ts,css}",
    "./src/app/**/**/**/*.{html,ts,css}",
  ],
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  theme: {
    extend: {
      colors: {
        "primary": "#329e8d",
        "secondary": "#00544c",
        "accent": "#85bed3",
        "neutral": "#22252a",
        "base-100": "#332f37",
        "info": "#8294ed",
        "success": "#60dcc5",
        "warning": "#f09c0a",
        "error": "#e7738d",
      },
    }
  },
  plugins: [
  ],
}

