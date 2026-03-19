import path from "path";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");

  // Cấu hình tập trung tại đây
  const API_URL = "http://localhost:55002/api/v1";
  const GOOGLE_CLIENT_ID =
    "567833204408-2bf86chhmiaj410h6fj18vpkdcn9cjce.apps.googleusercontent.com"; // Đồng bộ từ .env

  return {
    server: {
      port: 3000,
      host: "0.0.0.0",
      proxy: {
        '/api': {
          target: 'http://localhost:55002',
          changeOrigin: true,
        }
      }
    },
    define: {
      __API_URL__: JSON.stringify(API_URL),
      __GOOGLE_CLIENT_ID__: JSON.stringify(GOOGLE_CLIENT_ID),
      __TOKEN_KEY__: JSON.stringify("banner_ai_access_token"),
      __APP_ROUTES__: JSON.stringify({
        DASHBOARD: "/dashboard",
        GENERATE: "/generate",
        BILLING: "/billing",
        HISTORY: "/history",
        ADMIN: "/admin",
      }),
      __DEFAULT_BANNER_CONFIG__: JSON.stringify({
        width: 1200,
        height: 628,
        number: 1,
      }),
    },
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "."),
      },
    },
  };
});
