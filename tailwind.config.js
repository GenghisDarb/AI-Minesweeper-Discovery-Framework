module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#1f60ff",
          foreground: "#ffffff",
        },
        background: {
          DEFAULT: "#ffffff",
          dark: "#1a1a1a",
        },
      },
    },
  },
  plugins: [],
};
