import api from "./axios";

export async function loginUser(credentials) {
  const res = await api.post("/api/v1/auth/login", credentials);
  return res.data; // { access_token, refresh_token }
}

export async function registerUser(data) {
  const res = await api.post("/api/v1/auth/register", data);
  return res.data; // { id, email }
}
