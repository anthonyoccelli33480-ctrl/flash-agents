import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// base is "/flash-agents/" for production builds (GitHub Pages project site)
// and "/" in dev so the local proxy keeps working.
export default defineConfig(({ command }) => ({
  base: command === "build" ? "/flash-agents/" : "/",
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: false,
    proxy: { "/api": "http://127.0.0.1:8787" },
  },
}));
