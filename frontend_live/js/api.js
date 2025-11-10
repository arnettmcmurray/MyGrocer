import { CONFIG } from "./config.js";

export const API = {
  base: CONFIG.API_BASE,
  foodfacts: "https://world.openfoodfacts.org/api/v0/product",

  getToken() {
    return localStorage.getItem(CONFIG.TOKEN_KEY);
  },
  setToken(t) {
    localStorage.setItem(CONFIG.TOKEN_KEY, t);
  },
  clearToken() {
    localStorage.removeItem(CONFIG.TOKEN_KEY);
  },

  async req(path, method = "GET", data = null, auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth && this.getToken())
      headers["Authorization"] = `Bearer ${this.getToken()}`;

    const res = await fetch(`${this.base}${path}`, {
      method,
      headers,
      body: data ? JSON.stringify(data) : null,
      credentials: "include", // keep session cookies consistent
    });

    if (!res.ok) {
      console.error("API request failed:", res.status, path);
      throw new Error(await res.text());
    }

    return res.json();
  },

  async login(email, password) {
    const r = await this.req("/auth/login", "POST", { email, password }, false);
    this.setToken(r.access_token);
    return r;
  },

  async register(email, password) {
    return this.req("/auth/register", "POST", { email, password }, false);
  },

  async pantryList() {
    return this.req("/pantry/");
  },

  async pantryAdd(name) {
    return this.req("/pantry/", "POST", { name });
  },

  async pantryDel(id) {
    return this.req(`/pantry/${id}`, "DELETE");
  },

  async households() {
    return this.req("/households/");
  },

  async lookupFood(barcode) {
    const r = await fetch(`${this.foodfacts}/${barcode}.json`);
    return r.json();
  },
};
