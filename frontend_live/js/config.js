export const CONFIG = {
  API_BASE:
    window.location.hostname.includes("vercel.app") ||
    window.location.hostname.includes("onrender.com")
      ? "https://mygrocer-backend.onrender.com/api/v1"
      : "http://127.0.0.1:5000/api/v1",

  TOKEN_KEY: "mygrocer_token",
};
