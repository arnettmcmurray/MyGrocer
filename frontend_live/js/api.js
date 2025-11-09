export const API = {
  base: "http://127.0.0.1:5000/api/v1",
  foodfacts: "https://world.openfoodfacts.org/api/v0/product",
  getToken() {
    return localStorage.getItem("mygrocer_token");
  },
  setToken(t) {
    localStorage.setItem("mygrocer_token", t);
  },
  clearToken() {
    localStorage.removeItem("mygrocer_token");
  },

  async req(path, method = "GET", data = null, auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth && this.getToken())
      headers["Authorization"] = `Bearer ${this.getToken()}`;
    const res = await fetch(`${this.base}${path}`, {
      method,
      headers,
      body: data ? JSON.stringify(data) : null,
    });
    if (!res.ok) throw new Error(await res.text());
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
