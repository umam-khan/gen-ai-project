/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        white: "#fff",
        black: "#000",
        darkslateblue: "#042455",
      },
      spacing: {},
      fontFamily: {
        inter: "Inter",
      },
    },
    fontSize: {
      "45xl": "64px",
      "19xl": "38px",
      "32xl": "51px",
      "17xl": "36px",
      "3xl": "22px",
      "10xl": "29px",
      inherit: "inherit",
    },
  },
  plugins: [],
}