import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "ample-dark": "#0a0f1e",
        "ample-card": "#111827",
        "ample-border": "#1f2937",
        "ample-accent": "#3b82f6",
        "threat-low": "#22c55e",
        "threat-medium": "#f59e0b",
        "threat-high": "#f97316",
        "threat-critical": "#ef4444",
      },
    },
  },
  plugins: [],
};
export default config;
